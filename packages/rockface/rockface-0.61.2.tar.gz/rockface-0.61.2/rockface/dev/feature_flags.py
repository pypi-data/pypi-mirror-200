import json
import os

FlagSet = frozenset[str]


_SUPPORTED_FLAGS = FlagSet()

_DEFAULT_FLAGS = FlagSet()


class InvalidFeatureFlag(Exception):
    "An invalid feature name flag was provided"


def _load_feature_flags() -> set[str]:
    flags = json.loads(os.getenv("ROCKFACE_FEATURE_FLAGS", default="[]"))

    if not isinstance(flags, list):
        raise ValueError("Malformed feature flag environment variable")

    for flag in flags:
        if flag not in _SUPPORTED_FLAGS:
            raise InvalidFeatureFlag(
                f"Unknown feature flag in environment variable: '{flag}'"
            )

    return set(flags) | _DEFAULT_FLAGS


FEATURE_FLAGS = _load_feature_flags()


def flag_enabled(flag_name: str) -> bool:
    "Determine if the named feature flag is enabled"

    if flag_name not in _SUPPORTED_FLAGS:
        raise InvalidFeatureFlag(f"{flag_name} is not a known flag")

    return flag_name in FEATURE_FLAGS
