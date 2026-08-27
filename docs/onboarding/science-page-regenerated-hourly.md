# Onboarding: generated pages are regenerated where their stores live

A generator that resolves its stores from `__file__` must run in the checkout that holds them.
`docs/science/SHOWCASE.md` is written only by `science/showcase.py` inside the hourly snapshot
(`scripts/estate-snapshot`, step "regenerate the science page"); do not commit a copy generated in a
worktree, it will read BLIND on main. `rel()` prints every store path relative to the repo, and
`tests/test_incident_crew403_science_page_generated_from_the_live_checkout.py` fails on any absolute
path in the committed page. Same class, same fix as the hazard page (crew#495 CP2).
