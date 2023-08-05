"""Dataclass serialization"""
__docformat__ = "google"

from typing import Any

from turbo_broccoli.environment import (
    get_registered_dataclass_type,
    is_nodecode,
)


def _json_to_dataclass_v2(dct: dict) -> Any:
    """
    Converts a JSON document following the v2 specification to a dataclass
    object.
    """
    if is_nodecode("dataclass." + dct["class"]):
        return None
    return get_registered_dataclass_type(dct["class"])(**dct["data"])


def from_json(dct: dict) -> Any:
    """
    Deserializes a dict into a dataclass object. See `to_json` for the
    specification `dct` is expected to follow, and
    `turbo_broccoli.environment.register_dataclass_type`.
    """
    DECODERS = {
        2: _json_to_dataclass_v2,
    }
    try:
        return DECODERS[dct["__dataclass__"]["__version__"]](
            dct["__dataclass__"]
        )
    except KeyError as exc:
        raise TypeError("Not a valid dataclass document") from exc


def to_json(obj: Any) -> dict:
    """
    Serializes a dataclass into JSON by cases. The return dict has the
    following structure

        {
            "__dataclass__": {
                "__version__": 2,
                "class": <str>,
                "data": {...},
            },
        }

    where the `{...}` is `obj.__dict__`.
    """
    if hasattr(obj, "__dataclass_fields__"):
        return {
            "__dataclass__": {
                "__version__": 2,
                "class": obj.__class__.__name__,
                "data": obj.__dict__,
            },
        }
    raise TypeError("Not a supported type")
