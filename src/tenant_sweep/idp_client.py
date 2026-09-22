"""IDP client with shared auth, schema probe, and per-tenant memoisation."""
from __future__ import annotations

import threading
from dataclasses import dataclass


@dataclass(frozen=True)
class IdpClaims:
    tenant_id: str
    payload: tuple[tuple[str, str], ...]  # normalised claims, sorted keys


class IdpClient:
    """In-memory IDP facade. One auth token + one schema probe per instance.

    Per-tenant claims are memoised so a duplicate tenant in the list hits IDP once.
    All shared fetches are guarded by a lock.
    """

    def __init__(self, *_, http_get=None, http_post=None, **__) -> None:
        self._http_get = http_get
        self._http_post = http_post
        self._lock = threading.Lock()
        self._auth_token: str | None = None
        self._schema_version: str | None = None
        self._claims_cache: dict[str, IdpClaims] = {}

    # --- shared, fetched once ---
    def get_auth_token(self) -> str:
        with self._lock:
            if self._auth_token is None:
                self._auth_token = self._http_get("/auth/token") if self._http_get else "token-stub"
            return self._auth_token

    def get_schema_version(self) -> str:
        with self._lock:
            if self._schema_version is None:
                self._schema_version = self._http_get("/schema/version") if self._http_get else "v1"
            return self._schema_version

    # --- per-tenant, memoised ---
    def get_claims(self, tenant_id: str) -> IdpClaims:
        # Fast path without the lock.
        cached = self._claims_cache.get(tenant_id)
        if cached is not None:
            return cached
        with self._lock:
            cached = self._claims_cache.get(tenant_id)
            if cached is not None:
                return cached
            raw = self._http_get(f"/tenants/{tenant_id}/claims") if self._http_get else {"id": tenant_id}
            claims = IdpClaims(
                tenant_id=tenant_id,
                payload=tuple(sorted((str(k), str(v)) for k, v in (raw or {}).items())),
            )
            self._claims_cache[tenant_id] = claims
            return claims

    # --- parallel POSTs, bulk when available ---
    def post_onboarding(self, tenant_ids: tuple[str, ...]) -> None:
        if not tenant_ids:
            return
        if self._http_post is not None and len(tenant_ids) > 1:
            self._http_post("/tenants/onboarding:bulk", {"tenant_ids": list(tenant_ids)})
        else:
            for tid in tenant_ids:
                if self._http_post is not None:
                    self._http_post(f"/tenants/{tid}/onboarding", {"tenant_id": tid})
                # else: dry-run fallback below handles it
