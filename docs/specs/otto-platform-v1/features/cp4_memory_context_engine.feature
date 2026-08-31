@cp4
Feature: Memory and context engine (spec section 17 Phase 3, section 8, 12)
  Facts require provenance, retrieval is hybrid dense plus lexical plus a
  reranker, context is budgeted and compacted without silent loss, and
  subtasks get fresh isolated context.

  Background:
    Given the staging Postgres instance with pgvector, backed up nightly

  Scenario: Happy path - a provenanced fact is written and retrieved
    Given a fact with entity, attribute, value and a tool_call_id as provenance
    When mem_write commits it
    And mem_search is later called for that entity
    Then the fact is returned within the top 8 fused results

  Scenario: Retrieval precision meets the bar
    When an engineer runs "otto eval run --suite retrieval"
    Then precision at 8 on the retrieval slice is at least 0.8

  Scenario: Edge case - a fact with no provenance is rejected, not silently dropped
    When an insert into facts is attempted with provenance NULL
    Then the database constraint rejects the insert with a non-zero exit
    And "select count(*) from facts where provenance is null" against the live table returns 0

  Scenario: Hygiene job surfaces stale and contradictory facts
    Given a fact past its stale_after date and a contradiction pair with no supersession
    When the nightly hygiene job runs with "otto memory hygiene --dry-run"
    Then a stale-fact card and a contradiction-pair card are posted to a test Telegram chat
    And both cards are readable back via the Bot API

  Scenario: Context compaction writes an episode, nothing is silently lost
    Given a task context at 70 percent of its token budget
    When compaction runs
    Then a summarise-and-swap occurs
    And the summary is written as an episode row, not discarded

  Scenario: A subtask never inherits the parent's raw transcript
    Given a parent task that dispatches a subtask
    Then the subtask's context is fresh and isolated, with an explicit input and output-schema
      contract and a ceiling no higher than the parent's
    And trust tags on any untrusted content survive into the subtask's context

  Scenario: Network failure - Postgres connection drops mid write
    Given a mem_write in progress when the Postgres connection is dropped
    Then no partial fact row is persisted
    And the write is retried or surfaced as a failed tool call, never a half-written fact

  Scenario: Bandwidth degradation - hosted embedding and reranker APIs both degrade
    Given the hosted embedding API and the hosted reranker are both unreachable or slow
    When mem_search is called within the task's deadline_s
    Then it falls back to Postgres full-text search alone
    And it returns within deadline_s rather than hanging on the degraded dependency
