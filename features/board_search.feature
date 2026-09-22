Feature: Board index uses gh search issues --paginate
  As a board consumer
  I want the issue index to cover every issue in every repo
  So that nothing slips past the old 200-row ``gh issue list`` cap

  Scenario: index covers more than 200 issues
    Given a repo with 250 issues
    When the crew indexes it
    Then the index contains all 250 numbers
