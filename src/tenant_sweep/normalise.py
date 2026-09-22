"""Lazy validation/normalisation. Skipped when the payload is empty."""
from __future__ import annotations

from .idp_client import IdpClaims


def is_empty_payload(claims: IdpClaims) -> bool:
    return not claims.payload


def validate_and_normalise(claims: IdpClaims, schema_version: str) -> dict[str, str]:
    """Returns a flat dict ready to POST. No-op if the payload was empty."""
    if is_empty_payload(claims):
        return {}
    out = {k: v for k, v in claims.payload}
    # schema_version is intentionally unused for now; kept for future branching.
    assert schema_version, "schema_version must be probed before normalising"
    return out
