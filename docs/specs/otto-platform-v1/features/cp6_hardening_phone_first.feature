@cp6
Feature: Hardening and phone-first polish (spec section 17 Phase 5, section 13, 14)
  A chaos pass proves daemons are stateless and NATS-partition-tolerant, and a
  full representative week of Otto usage is operable from Telegram alone. This
  checkpoint uses the NEW Telegram bot/channel for the new build; the
  currently running Otto and its existing bot are untouched.

  Background:
    Given the staging cluster only, zero production credentials in scope
    And a new Telegram bot and channel distinct from the currently running Otto's

  Scenario: Happy path - a full representative week runs from Telegram alone
    Given a scripted week of tasks, one per class from research, code, ops_read, comms,
      schedule and memory
    When an engineer runs "otto drill telegram-only-week"
    Then every task completes end to end through the Telegram surface only
    And no direct CLI or database touch was required to reach completion

  Scenario: Edge case - a daemon is killed mid task and loses nothing
    Given a task mid-execution on a stateless daemon
    When that daemon process is killed
    Then a fresh daemon resumes the task from the stream
    And "otto replay <task_id>" shows no lost tool call and no duplicate side effect

  Scenario: Network failure - NATS partitions mid task
    Given a task publishing tool req/res events
    When NATS JetStream is partitioned mid task
    Then the task retries once the partition heals
    And Nats-Msg-Id dedupe ensures no event is duplicated or lost across the partition

  Scenario: Mandatory - Telegram API flaps during an approval card send
    Given a T2 action awaiting an approval card
    When the Telegram Bot API is unavailable at send time
    Then the send is retried until the API recovers
    And the card is delivered exactly once, the action is not executed twice from a retried send

  Scenario: Weekly digest and skill promotion fire on schedule
    Given a week of completed tasks and at least one procedure repeated 3 or more times with
      pass verdicts
    Then the weekly digest reaches Telegram with tasks by class, verdict pass rate, ungrounded
      claim rate, cost by lane, and incidents with their class-level fixes
    And a card proposing promotion of the repeated procedure to a skill is posted for Chidi's
      approval, never auto-promoted
