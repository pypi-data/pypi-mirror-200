from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum
from importlib import import_module
from itertools import chain
from typing import TYPE_CHECKING, Any, Collection

from attrs import Attribute, define, field, fields

from cloudshell.shell.standards.core.namespace_type import NameSpaceType
from cloudshell.shell.standards.core.resource_conf.attrs_converters import (
    AbsCollectionConverter,
    AbsConverter,
    BoolConverter,
    IntConverter,
    ListConverter,
    SetConverter,
    StrConverter,
    TupleConverter,
)
from cloudshell.shell.standards.core.resource_conf.resource_attr import RAISE, AttrMeta
from cloudshell.shell.standards.exceptions import ResourceConfigException

if TYPE_CHECKING:
    from cloudshell.shell.standards.core.resource_conf import BaseConfig

from typing import Union

from cloudshell.shell.core.driver_context import (
    AutoLoadCommandContext,
    InitCommandContext,
    ResourceCommandContext,
    ResourceRemoteCommandContext,
    UnreservedResourceCommandContext,
)

RESOURCE_CONTEXT_TYPES = Union[
    ResourceCommandContext,
    InitCommandContext,
    AutoLoadCommandContext,
    UnreservedResourceCommandContext,
    ResourceRemoteCommandContext,
]


class WithoutMeta(ResourceConfigException):
    pass


@define
class InitializeClassError(ResourceConfigException):
    name: str
    type_: type
    val: str

    def __str__(self) -> str:
        msg = f"'{self.name}' receive not valid value '{self.val}'"
        if issubclass(self.type_, Enum):
            values = ", ".join([f"'{v.value}'" for v in self.type_])
            msg += f". Possible values are: {values}"
        return msg


class AbsResourceAttrsConverter(ABC):
    def __init__(
        self,
        context: RESOURCE_CONTEXT_TYPES,
        config_cls: type[BaseConfig],
        decrypt_password: Callable[[str], str],
    ):
        self.context = context
        self.config_cls = config_cls
        self._decrypt_password = decrypt_password

    @abstractmethod
    def get_attrs(self) -> dict[str, Any]:
        ...


@define
class ResourceAttrsConverter(AbsResourceAttrsConverter):
    context: RESOURCE_CONTEXT_TYPES
    config_cls: type[BaseConfig]
    _decrypt_password: Callable[[str], str]
    _collection_converters: Collection[type[AbsCollectionConverter]] = (
        ListConverter,
        TupleConverter,
        SetConverter,
    )
    _converters: Collection[type[AbsConverter]] = (
        StrConverter,
        BoolConverter,
        IntConverter,
    )
    shell_name: str = field(init=False)
    family_name: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.shell_name = self.context.resource.model
        self.family_name = self.context.resource.family

    def get_attrs(self) -> dict[str, Any]:
        cls_attrs = {}
        for f in fields(self.config_cls):
            try:
                val = self._convert_attr(f)
            except WithoutMeta:
                continue
            else:
                cls_attrs[f.name] = val
        return cls_attrs

    def _convert_attr(self, f: Attribute) -> Any:
        str_type = self._get_str_type(f)
        meta = self._get_meta(f)
        key = self._get_key(meta)
        try:
            val = self.context.resource.attributes[key]
        except KeyError:
            val = self._get_default(f, meta, str_type, attr_present=False)
        else:
            if val == "":
                val = self._get_default(f, meta, str_type, attr_present=True)
            else:
                if meta.is_password:
                    val = self._decrypt_password(val)
                if f.converter is None:
                    val = self._convert_by_type(val, str_type, meta)
        return val

    @staticmethod
    def _get_default(
        f: Attribute, meta: AttrMeta, str_type: str, attr_present: bool
    ) -> Any:
        error = ValueError(f"Resource attribute {meta.name} is missing")
        default = f.default

        if default is RAISE:
            if not attr_present:
                raise error
            elif str_type != "str":
                # empty string is not valid value for non-str types
                raise error
            else:
                # empty string is valid value for str types
                default = ""

        return default

    @staticmethod
    def _get_str_type(f: Attribute) -> str:
        return f.type if isinstance(f.type, str) else f.type.__name__

    @staticmethod
    def _get_meta(f: Attribute) -> AttrMeta:
        meta = f.metadata.get(AttrMeta.DICT_KEY)
        if not meta:
            raise WithoutMeta
        return meta

    def _get_key(self, meta: AttrMeta) -> str:
        namespace = self._get_namespace(meta.namespace_type)
        return f"{namespace}.{meta.name}"

    def _get_namespace(self, namespace_type: NameSpaceType) -> str:
        if namespace_type is NameSpaceType.SHELL_NAME:
            namespace = self.shell_name
        elif namespace_type is NameSpaceType.FAMILY_NAME:
            namespace = self.family_name
        else:
            raise ValueError(f"Unknown namespace: {namespace_type}")
        return namespace

    def _convert_by_type(self, val: str, str_type: str, meta: AttrMeta) -> Any:
        for converter_cls in chain(self._collection_converters, self._converters):
            if converter_cls.is_supported_type(str_type):
                if issubclass(converter_cls, AbsCollectionConverter):
                    new = self._convert_collection(converter_cls, val, str_type, meta)
                else:
                    new = self._convert_single(converter_cls, val, str_type, meta)
                break
        else:
            new = self._initialize_class(val, str_type, meta)
        return new

    def _convert_collection(
        self,
        converter_cls: type[AbsCollectionConverter],
        val: str,
        str_type: str,
        meta: AttrMeta,
    ) -> Any:
        converter = converter_cls(val, meta)
        collection_type = converter.type_
        child_str_type = converter.get_str_child_type(str_type)
        child_values = converter.child_values

        converted_val = collection_type(
            self._convert_by_type(child_val, child_str_type, meta)
            for child_val in child_values
        )
        return converted_val

    @staticmethod
    def _convert_single(
        converter_cls: type[AbsConverter], val: str, str_type: str, meta: AttrMeta
    ) -> Any:
        converter = converter_cls(val, meta)
        return converter.convert()

    def _initialize_class(self, val: str, str_type: str, meta: AttrMeta):
        type_ = self._import_type(str_type)
        try:
            converted_val = type_(val)
        except Exception:
            raise InitializeClassError(meta.name, type_, val)
        return converted_val

    def _import_type(self, type_name: str) -> type:
        for cls in self.config_cls.mro():
            module = import_module(cls.__module__)
            type_ = getattr(module, type_name, None)
            if type_ is not None:
                return type_
        raise TypeError(f"Can't find type {type_name}")
