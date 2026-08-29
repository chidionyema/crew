Feature: the probe is taken by infrastructure, never by the session that cites it
  crew#628 phase 1, founder spec §3. The founder's flag: the prober lives on the
  production cluster, which only holds together if the prober is infrastructure
  rather than crew. §3.4 takes that position and this feature encodes it.

  Scenario: the probe performs the full authenticated round trip
    Given a service probe for the catalogue
    When the probe runs on its schedule
    Then it authenticates, requests the service, and records the result

  Scenario: an identifier that only exists after sign-in is what proves the check
    Given a probe asserting on an identifier that cannot appear before sign-in
    When the service returns a sign-in page carrying a success code
    Then the identifier assertion does not pass
    And the published state is a failure

  Scenario: a redirect is never a pass
    Given a probe receives a redirect at the door
    When the result is published
    Then the published state is a failure
    And nothing behind the sign-in gate is recorded as observed

  Scenario: a partial pass is a failure
    Given a probe whose status assertion passes and whose identifier assertion does not
    When the result is published
    Then the published state is a failure
    And the failing assertion is named in the probe log

  Scenario: a session can read the result and cannot take the measurement
    Given a crew session holding its own credentials
    When it tries to read the probe's credentials
    Then it cannot
    And it can still read the published probe result

  Scenario: the probe's own credentials cannot change what it probes
    Given the probe's client is scoped to read-only endpoints
    When the probe runs
    Then it cannot alter the service it measures

  Scenario: a result older than the freshness window is not a result
    Given the freshness window for a service
    And the last probe result is older than that window
    When a session reads the state
    Then it reads "UNKNOWN" regardless of the last recorded value
