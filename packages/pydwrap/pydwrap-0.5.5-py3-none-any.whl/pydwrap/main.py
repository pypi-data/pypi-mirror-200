from __future__ import annotations

from typing import Any, Generic, Type, TypeVar, cast, get_origin

from pydantic import BaseModel as OriginalBaseModel
from pydantic import create_model, root_validator
from pydantic.fields import ModelField
from pydantic.typing import is_none_type

_T = TypeVar("_T")
_V = TypeVar("_V")


class Option(Generic[_T]):
    """Type Option in order to correctly handle optional value."""

    __value: _T | None

    def __init__(self, value: _T | None = None):
        self.__value = value

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "%s(%s)" % (
            self.__class__.__name__,
            repr(self.__value),
        )

    @classmethod
    def __get_validators__(cls):
        yield cls.option_validator

    @classmethod
    def option_validator(cls, v: Any, field: ModelField) -> Option[_T]:
        field_name = field.name.removeprefix("_").removesuffix("_")
        if field.outer_type_ is Option:
            raise TypeError(
                "To type an Option, it is necessary to specify a parameter in its generic."
            )
        if v is None:
            return cls(v)
        if isinstance(v, cls) and v.is_none:
            return v
        validator = _create_validator_option_value(
            field_name,
            v.unwrap() if isinstance(v, cls) else v,
            field.outer_type_.__args__[0],
        )
        return cls(getattr(validator, field_name))

    @property
    def is_none(self) -> bool:
        """Return True if value is None."""
        return self.__value is None

    def unwrap(self, *, error_msg: str = None) -> _T:
        """Unwrap the optional value if it's not None, otherwise a
        ValueError will be raised with the appropriate error_msg.
        """
        if self.__value is None:
            raise ValueError(error_msg if error_msg is not None else "Value is None.")
        return self.__value

    def unwrap_or(self, variant: _V, /) -> _T | _V:
        """Unwrap the optional value if it's not None,
        otherwise it will return the variant you passed.
        """
        if variant is None:
            raise TypeError("Variant should not be type NoneType.")
        return self.__value if self.__value is not None else variant


class BaseModel(OriginalBaseModel):
    @root_validator(pre=True)
    @classmethod
    def _pre_root_validator(cls, values: dict[str, Any]) -> dict[str, Any]:
        model_schema = cls.schema()
        fields = _get_default_fields(model_schema)
        fields.update(_get_required_option_fields(cls.__annotations__, model_schema))
        fields.update(values)
        return {
            field: Option(value)
            if _is_option_type(cls.__annotations__.get(field, None))
            and not isinstance(value, Option)
            else value
            for field, value in fields.items()
        }


def _is_option_type(type_: Type[Any]) -> bool:
    if is_none_type(type_):
        return False
    origin = get_origin(type_)
    if is_none_type(origin):
        return False
    return origin is Option


def _get_default_fields(schema: dict[str, Any]) -> dict[str, Any]:
    properties = cast(dict[str, Any], schema.get("properties", {}))
    return {
        k: properties[k]["default"] for k in properties if "default" in properties[k]
    }


def _get_required_option_fields(
    annotations_model: dict[str, Any], schema: dict[str, Any]
) -> dict[str, Option]:
    properties = cast(dict[str, Any], schema.get("properties", {}))
    return {
        k: Option()
        for k in properties
        if k in schema.get("required", [])
        or "default" not in properties[k]
        and _is_option_type(annotations_model[k])
    }


def _create_validator_option_value(
    field_name: str, field_value: Any, field_type: Type[Any]
) -> BaseModel:
    return create_model(
        "ValidatorOptionValue",
        __base__=BaseModel,
        **{
            field_name: (
                field_type,
                field_value,
            )
        },
    )()
