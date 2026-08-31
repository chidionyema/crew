@cp1
Feature: Channel plane — adapter registry and capability negotiation (spec v1.1 section 1)
  Every surface's adapter registers a capability set at boot; the router asks the
  registry, never a per-request guess, what a responding surface can carry, and
  degrades explicitly when it cannot. Extends the day-0 SurfaceAdapter contract
  (crew#768) that already ships inside the v1 build. Owns otto/surface/registry.py,
  otto/surface/negotiate.py, otto/surface/render_degrade.py.

  Background:
    Given the staging cluster only, zero production credentials in scope
    And the day-0 SurfaceAdapter contract is live from the v1 build

  Scenario: Every registered adapter carries a distinct, non-empty capability set
    Given the Telegram adapter and the minimal HTTP adapter are both registered
    When an engineer runs "otto surface list-adapters"
    Then the command exits 0
    And Telegram and HTTP each show a non-empty capability set

  Scenario: A response requiring a missing capability degrades loudly, never silently
    Given a rendered response that requires voice_out
    And the Telegram adapter has not declared voice_out
    When an engineer runs "otto test render-degrade --surface telegram --response voice_out"
    Then the command exits 0
    And the rendered message states the degradation in an explicit line
    And no modality of the response is silently dropped

  Scenario: The same content produces the same task envelope across two surfaces
    Given identical message content submitted through Telegram and through the HTTP adapter
    When an engineer runs "otto test envelope-parity --surface telegram --surface http"
    Then the command exits 0
    And the two task envelopes differ only in "surface" and "principal"

  Scenario: Edge case - an unregistered adapter cannot receive a rendered response
    Given a surface identifier that never called "register"
    When an engineer runs "otto test render --surface unregistered"
    Then the command exits non-zero
    And the failure names the missing registration, never a default text fallback

  Scenario: Network failure - the registry lookup during a partition never invents a capability set
    Given the registry's backing store is unreachable
    When a response is rendered for any surface during the partition
    Then the render fails closed with a named error
    And no capability is assumed present that was never confirmed
