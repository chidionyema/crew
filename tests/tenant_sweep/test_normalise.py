from tenant_sweep.idp_client import IdpClaims
from tenant_sweep.normalise import is_empty_payload, validate_and_normalise


def test_empty_payload_short_circuits():
    c = IdpClaims("t1", ())
    assert is_empty_payload(c)
    assert validate_and_normalise(c, "v1") == {}


def test_non_empty_payload_validates():
    c = IdpClaims("t1", (("email", "a@b.c"), ("role", "admin")))
    out = validate_and_normalise(c, "v1")
    assert out == {"email": "a@b.c", "role": "admin"}


def test_validate_requires_schema_version():
    c = IdpClaims("t1", (("email", "a@b.c"),))
    try:
        validate_and_normalise(c, "")
    except AssertionError:
        return
    raise AssertionError("expected AssertionError on empty schema_version")
