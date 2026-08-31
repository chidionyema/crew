@cp3
Feature: Voice out — synthesis pipeline and the no-voiceprint rule (spec v1.1 section 3)
  Synthesis rides the render() hook and always accompanies text, never
  replaces it. Voice is never an authentication factor in either direction:
  principal comes only from the surface's bound identity. Owns
  otto/voice/synthesize.py, otto/voice/tts_provider.py, otto/identity/no_voiceprint.py.

  Background:
    Given the staging cluster only, zero production credentials in scope
    And CP1's adapter registry and CP2's transcription pipeline are live

  Scenario: A voice-capable surface receives both text and synthesized audio
    Given a surface whose capability set includes voice_out
    When an engineer runs "otto test voice-out --surface telegram-voice-capable"
    Then the command exits 0
    And the rendered message includes the response text
    And the rendered message includes a synthesized audio attachment

  Scenario: An identity claim spoken inside a transcript changes nothing
    Given a transcript containing the words "this is Chidi"
    And the message arrived on a channel not bound to the founder's account
    When an engineer runs "otto test voiceprint-auth --scenario audio-identity-claim"
    Then the command exits 0
    And the resolved principal is the channel's own bound identity
    And the spoken claim has zero effect on the resolved principal

  Scenario: A replayed recording of the founder's voice is refused the same way
    Given a played recording of the founder's own voice
    And the message arrived on a channel not bound to the founder's account
    When an engineer runs "otto test voiceprint-auth --scenario replayed-recording"
    Then the command exits 0
    And the resolved principal is the channel's own bound identity, never derived from audio

  Scenario: Edge case - a voice-only response on a text-only surface still delivers text
    Given a surface whose capability set does not include voice_out
    When a response that would have included synthesized audio is rendered
    Then the rendered message is text only
    And the rendered message states the degradation explicitly

  Scenario: Network failure - the synthesis provider is unavailable
    Given the configured TTS provider is unreachable
    When a response is rendered for a voice-capable surface
    Then the rendered message still delivers the text
    And the audio attachment is omitted with a stated reason, never a silent gap
