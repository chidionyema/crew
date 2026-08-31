@cp6
Feature: Observability — voice, vision and presence spans reach the collector (spec v1.1 section 6, LAW 50)
  Every voice, vision and cross-surface envelope carries the same task ULID
  the spine mints; the otto-obs-coverage gate refuses launch if any of the
  three new components is absent from the backend, exactly as it already does
  for spine, gateway, verify, memory, router and obs. No second collector.
  Owns otto/obs/components/voice.py, vision.py, presence.py.

  Background:
    Given the staging cluster only, zero production credentials in scope
    And CP2, CP3, CP4 and CP5 each call otto/obs's instrument() directly
    And the estate's existing SigNoz and Langfuse backends, no second collector

  Scenario: The coverage gate sees spans from all three new components
    Given a fresh test task that exercises voice, vision and a surface switch
    When an engineer runs "otto-obs-coverage --components voice,vision,presence"
    Then the command exits 0
    And SigNoz shows a span from each of voice, vision and presence
    And Langfuse shows at least one model-call trace carrying the same task ULID

  Scenario: A component absent from the backend is a red gate, not a warning
    Given the vision component's spans are missing from SigNoz for the test window
    When an engineer runs "otto-obs-coverage --components voice,vision,presence"
    Then the command exits non-zero
    And the missing component is named in the failure, not summarised away

  Scenario: A task crossing voice, vision and a surface switch fully replays
    Given a task that transcribed a voice note, described an image and switched surfaces
    When an engineer runs "otto replay <task_id>"
    Then the command exits 0
    And the replay shows the transcription call, the description call and the presence resolution
    And no step is reconstructed from anything outside the streams and the collector

  Scenario: Edge case - a component started without instrumentation fails its own boot
    Given a voice-pipeline process that omits the instrument() call
    When that process starts
    Then it fails its own boot contract
    And it never runs unobserved

  Scenario: Network failure - the OTLP exporter endpoint is unreachable at boot
    Given OTEL_EXPORTER_OTLP_ENDPOINT points at an unreachable collector
    When a voice, vision or presence component starts
    Then it retries per its configured backoff
    And it does not silently fall back to running without emitting spans
