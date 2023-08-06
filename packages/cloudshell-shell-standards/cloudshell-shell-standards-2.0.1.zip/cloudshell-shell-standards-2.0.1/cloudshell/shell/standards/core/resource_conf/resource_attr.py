from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Sequence, TypeVar, Union

from attrs import field, frozen, setters

from cloudshell.shell.standards.core.namespace_type import NameSpaceType

if TYPE_CHECKING:
    # used for TypeVar
    from attrs import Attribute  # noqa: F401

    from cloudshell.shell.standards.core.resource_conf import BaseConfig  # noqa: F401


CONFIG_TYPE = TypeVar("CONFIG_TYPE", bound="BaseConfig")
VALUE_TYPE = TypeVar("VALUE_TYPE")
VALIDATOR_TYPE = Callable[[CONFIG_TYPE, "Attribute[VALUE_TYPE]", VALUE_TYPE], None]
VALIDATOR_ARG = Union[VALIDATOR_TYPE, Sequence[VALIDATOR_TYPE]]


class _Raise(enum.Enum):
    RAISE = enum.auto()


RAISE = _Raise.RAISE


@frozen
class AttrMeta:
    DICT_KEY: ClassVar[str] = "_standard"
    name: str
    namespace_type: NameSpaceType
    is_password: bool


def attr(
    name: str,
    namespace: NameSpaceType = NameSpaceType.SHELL_NAME,
    is_password: bool = False,
    default: Any = RAISE,
    converter: Callable[[Any], Any] | None = None,
    validator: VALIDATOR_ARG | None = None,
) -> Any:
    return field(
        metadata={AttrMeta.DICT_KEY: AttrMeta(name, namespace, is_password)},
        default=default,
        kw_only=True,
        on_setattr=setters.frozen,
        converter=converter,
        validator=validator,
        repr=not is_password,
    )
