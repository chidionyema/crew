from tenant_sweep.idp_client import IdpClient, IdpClaims


def make_client(**calls):
    calls["n"] = 0

    def http_get(path):
        calls["n"] += 1
        if path == "/auth/token":
            return "tok"
        if path == "/schema/version":
            return "v2"
        return {"id": path.rsplit("/", 2)[-2]}

    return IdpClient(http_get=http_get), calls


def test_auth_token_and_schema_probed_once():
    client, calls = make_client()
    assert client.get_auth_token() == "tok"
    assert client.get_schema_version() == "v2"
    client.get_auth_token()
    client.get_schema_version()
    assert calls["n"] == 2


def test_claims_are_memoised_per_tenant():
    client, _ = make_client()
    a = client.get_claims("t1")
    b = client.get_claims("t1")
    assert a is b
    c = client.get_claims("t2")
    assert c.tenant_id == "t2"


def test_idp_claims_is_hashable():
    c = IdpClaims("t1", (("a", "1"), ("b", "2")))
    assert hash(c) == hash(c)


def test_post_onboarding_empty_is_noop():
    client, _ = make_client()
    client.post_onboarding(())
    # no exception, no state change needed
