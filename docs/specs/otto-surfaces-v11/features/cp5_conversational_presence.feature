@cp5
Feature: Conversational presence — cross-surface continuity (spec v1.1 section 5, crew#770 H2.2 slice)
  One conversation state keyed on principal, not surface: a thread started on
  Telegram continues on the minimal HTTP surface, with per-surface rendering
  staying surface-local. Owns otto/presence/store.py, otto/presence/continuity.py.
  Scope: this checkpoint proves the presence kernel only — no companion app,
  no glasses, no push notifications.

  Background:
    Given the staging cluster only, zero production credentials in scope
    And CP1's adapter registry is live
    And the presence store rides the existing Postgres instance from v1 CP4, no second database

  Scenario: A thread started on one surface continues on another for the same principal
    Given a thread opened on Telegram by the founder's bound principal
    When an engineer runs "otto test presence --start telegram --continue http"
    Then the command exits 0
    And the HTTP continuation resolves the same presence record
    And the router's context assembly includes the Telegram turns

  Scenario: The same conversation renders differently per surface
    Given a presence record with turns from two surfaces
    When an engineer runs "otto test presence --render-shape"
    Then the command exits 0
    And Telegram renders rich cards where supported
    And the HTTP surface renders the equivalent plain response
    And the underlying state is identical on both

  Scenario: Edge case - two principals on the same surface never cross threads
    Given two distinct principals each with an open thread on Telegram
    When an engineer runs "otto test presence --isolation"
    Then the command exits 0
    And principal B's continuation call never resolves principal A's thread

  Scenario: Edge case - a stale thread reference resolves to nothing, not the wrong thread
    Given a thread_id that has expired or never existed
    When a message references it
    Then the command exits non-zero
    And a new thread is opened rather than resolving to an unrelated conversation

  Scenario: Network failure - the presence store is unreachable mid-continuation
    Given the presence store's backing Postgres instance is unreachable
    When a continuation is attempted on a second surface
    Then the continuation fails closed with a named error
    And no thread state is silently reconstructed from surface-local history alone
