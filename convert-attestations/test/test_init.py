"""Initial testing module."""

import convert_attestations


def test_version() -> None:
    version = getattr(convert_attestations, "__version__", None)
    assert version is not None
    assert isinstance(version, str)
