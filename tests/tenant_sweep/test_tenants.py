from tenant_sweep.tenants import TenantList, unique_ordered


def test_unique_ordered_keeps_first_occurrence():
    assert unique_ordered(["a", "b", "a", "c", "b"]) == ("a", "b", "c")


def test_tenant_list_uses_provided_raw():
    tl = TenantList(raw=["x", "y", "x"])
    assert tl.unique() == ("x", "y")


def test_tenant_list_loader_runs_once():
    calls = {"n": 0}

    def load():
        calls["n"] += 1
        return ("p", "q", "p")

    tl = TenantList(loader=load)
    tl.all()
    tl.all()
    assert calls["n"] == 1
    assert tl.unique() == ("p", "q")


def test_concurrent_all_only_loads_once():
    import threading

    calls = {"n": 0}

    def load():
        calls["n"] += 1
        return ("a", "b")

    tl = TenantList(loader=load)
    threads = [threading.Thread(target=tl.all) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert calls["n"] == 1
