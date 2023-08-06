from __future__ import annotations

from collections.abc import Callable
from typing import ClassVar

from attrs import define
from typing_extensions import Self

from cloudshell.api.cloudshell_api import CloudShellAPISession

from cloudshell.shell.standards.core.resource_conf.attrs_converter import (
    RESOURCE_CONTEXT_TYPES,
    AbsResourceAttrsConverter,
    ResourceAttrsConverter,
)


@define(slots=False, str=False)
class BaseConfig:
    """Base class for creating resource configs.

    Attributes types should be accessible from the module where a Config defined

    @define(slots=False, str=False)
    class Config(BaseConfig):
        str_res_attr: str = attr("Str Attribute")
        int_res_attr: int = attr("Int Attribute")
        enum_res_attr: EnumSubClass = attr("Enum Attribute")
    """

    _CONVERTER: ClassVar[type[AbsResourceAttrsConverter]] = ResourceAttrsConverter
    name: str
    shell_name: str
    family_name: str
    address: str
    api: CloudShellAPISession

    def __str__(self) -> str:
        cls_name = type(self).__name__
        return f"{cls_name}({self.name})"

    @classmethod
    def from_context(
        cls, context: RESOURCE_CONTEXT_TYPES, api: CloudShellAPISession
    ) -> Self:
        converter = cls._CONVERTER(context, cls, _password_decryptor(api))

        return cls(
            name=context.resource.name,
            shell_name=context.resource.model,
            family_name=context.resource.family,
            address=context.resource.address,
            api=api,
            # this should return kwargs but BaseConfig doesn't have any
            **converter.get_attrs(),  # noqa
        )


def _password_decryptor(api: CloudShellAPISession) -> Callable[[str], str]:
    def wrapped(val: str) -> str:
        return api.DecryptPassword(val).Value

    return wrapped
