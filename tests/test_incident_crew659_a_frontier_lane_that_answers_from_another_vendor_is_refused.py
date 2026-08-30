"""crew#659 incident, 2026-08-30 05:3xZ: the science key asked the router for `claude` and
`gemini` and every answer came back `MiniMax-M2`. Both vendor accounts were empty (Anthropic
"credit balance is too low", Google "prepayment credits are depleted") and the router's fallback
chain walked each frontier lane to a local-class model and answered 200. The worker would have
automated unverified claims on the very model the founder's blueprint refuses.

Guard: the worker probes each lane with fallbacks off before any run, and a lane that cannot
answer from its own vendor is refused with the vendor's words, so the founder reads the
action (top up) and never a green run on the wrong model.
"""

import pytest

from science import research_worker as rw


def test_a_lane_whose_vendor_refuses_is_refused_with_the_vendor_words():
    def ask(lane):
        raise RuntimeError("AnthropicException - Your credit balance is too low")

    with pytest.raises(rw.Refused) as e:
        rw.probe_lane("claude", "worker", ask=ask)
    assert "credit balance is too low" in str(e.value)
    assert "worker lane 'claude'" in str(e.value)


def test_a_lane_that_answers_from_its_vendor_passes_and_names_the_model():
    assert (
        rw.probe_lane("claude", "worker", ask=lambda lane: "claude-sonnet-5") == "claude-sonnet-5"
    )


def test_every_router_call_the_worker_makes_has_fallbacks_off():
    import inspect

    src = inspect.getsource(rw)
    assert src.count("extra_body=NO_FALLBACK") >= 2, (
        "probe_lane and _chat both ask the router with fallbacks off; a 200 from another "
        "vendor is the incident"
    )
    assert rw.NO_FALLBACK == {"fallbacks": []}


def test_the_probe_asks_for_a_real_run_worth_of_tokens_so_an_empty_balance_shows_up_front():
    """2026-08-30 05:5xZ: the 1-token probe passed on OpenRouter and the run died nine retries
    later on `402 ... You requested up to 4000 tokens, but can only afford 2272`."""
    import inspect

    assert rw.PROBE_MAX_TOKENS >= 4000
    assert "max_tokens=PROBE_MAX_TOKENS" in inspect.getsource(rw.probe_lane)
