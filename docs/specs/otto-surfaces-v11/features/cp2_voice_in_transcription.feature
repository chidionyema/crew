@cp2
Feature: Voice in — transcription pipeline, Telegram voice notes as first binding (spec v1.1 section 2)
  A Telegram voice note normalises into the same task envelope as a typed
  message; transcription rides the capability interface (provider chosen by
  OTTO_STT_PROVIDER, never named in core) so the gateway sees one code path
  for voice and text alike. Owns otto/voice/transcribe.py, otto/voice/stt_provider.py.

  Background:
    Given the staging cluster only, zero production credentials in scope
    And CP1's adapter registry is live

  Scenario: A Telegram voice note becomes a task envelope with a matching transcript
    Given a Telegram voice message fixture with known text
    When an engineer runs "otto test voice-in --fixture telegram-voice-note"
    Then the command exits 0
    And the task envelope shows modality_in "voice"
    And the transcript text matches the fixture's known text

  Scenario: A low-confidence transcript asks for confirmation before becoming a task
    Given a transcript scored below OTTO_STT_MIN_CONFIDENCE
    When an engineer runs "otto test voice-in --fixture low-confidence"
    Then the command exits 0
    And the founder is asked to confirm before the transcript proceeds as a task

  Scenario: The trust class of a voice note comes from the channel binding, not the audio
    Given a voice note arriving on the founder's bound Telegram account
    When the task envelope is built
    Then its trust class is "operator"
    And the trust class would be identical for a typed message from the same account

  Scenario: Edge case - a voice note with silence produces an empty transcript, not an error
    Given a voice message fixture containing only silence
    When an engineer runs "otto test voice-in --fixture silence"
    Then the command exits 0
    And the transcript is empty text, not a raised exception

  Scenario: Network failure - the transcription provider times out mid-call
    Given the configured STT provider is unreachable
    When a voice note is submitted
    Then the task fails closed with state "TRANSCRIPTION_UNAVAILABLE"
    And the message is never silently treated as empty
