Feature: every founder-facing surface is measured the same way, not just the first one
  crew#628 phase 3, founder spec §7. Phase 1 proves the shape on one service.
  This phase is the shape applied to the rest, so that "no probe exists" stops
  being the reason a session takes its own measurement.

  Scenario: each founder-facing surface has a probe
    Given the founder-facing surfaces named in the spec
    Then each one has a probe definition of its own

  Scenario: a surface with no probe reports UNKNOWN rather than being measured by hand
    Given a surface with no probe definition
    When a session is asked whether it is reachable
    Then it answers "UNKNOWN"
    And it does not substitute its own request for a probe

  Scenario: each probe asserts on an identifier that proves sign-in was passed
    Given every probe definition in the estate
    Then each asserts on a value that an unauthenticated response cannot produce

  Scenario: a probe definition is reviewed like a production change
    Given a change to a probe definition
    When it is proposed
    Then it is reviewed as a production manifest is reviewed
