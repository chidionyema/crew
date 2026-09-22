Feature: Board index covers repos with more than 200 issues

  The board index must paginate past GitHub's default 100-issue window,
  produce the full ordered list of issue numbers, and reach a steady state
  on subsequent runs via the --updated-at watermark.

  Background:
    Given a repository "acme/widgets" with 250 open issues
    And the board index is empty

  Scenario: index covers more than 200 issues
    Given a 250-issue repo
    When I run the board indexer with page size 100
    Then I see 250 rows
    And the numbers 1 through 250 each appear once in order
    And at least 3 gh calls were made

  Scenario Outline: watermark re-run is steady state
    Given a 250-issue repo that was indexed at "<watermark>"
    When I re-run the board indexer with --updated-at ">=<watermark>"
    Then I see 0 new rows
    And every gh call carried "--updated-at >=<watermark>"

    Examples:
      | watermark              |
      | 2025-01-02T03:04:05Z   |
      | 2025-06-30T00:00:00Z   |
      | 2025-12-31T23:59:59Z   |
