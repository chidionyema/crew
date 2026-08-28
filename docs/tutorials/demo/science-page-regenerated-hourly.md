# Demo: the science page is regenerated every hour from the live checkout

    python3 science/showcase.py            # from ~/dev/code/crew: 2 BLIND of 10 (foresight untrained, crew#71)
    grep -c '/Users/\|/private/' docs/science/SHOWCASE.md   # 0: no checkout bakes itself into the page
    python3 -m pytest -q tests/test_incident_crew403_science_page_generated_from_the_live_checkout.py

Every hour `scripts/estate-snapshot` runs the generator in the live checkout before it copies
anything, and publishes `docs/science/SHOWCASE.md` with STATE.md. The page on main is never older
than the last snapshot, and a BLIND row names `science/<store>` relative to the repo.
