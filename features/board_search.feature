Feature: Board search
  As an agent workforce manager
  I want to search open tickets across every plan by free-text query
  So that I can find the right ticket to work on without scrolling the board

  Scenario: Searching for a single keyword in titles
    Given plans "alpha" and "beta" each contain a ticket titled "Add login flow"
    When I run `crew search --plan alpha.json --plan beta.json --query login`
    Then both tickets appear in the output

  Scenario: Searching with multiple tokens
    Given plan "alpha" has ticket "Add login flow" with body "supports oauth and saml"
    And plan "alpha" has ticket "Add login flow" with body "only oauth"
    When I run `crew search --plan alpha.json --query "oauth saml"`
    Then only the ticket mentioning saml appears in the output

  Scenario: Empty query returns no tickets
    Given plan "alpha" has ticket "Add login flow"
    When I run `crew search --plan alpha.json --query ""`
    Then no tickets appear in the output

  Scenario: Case-insensitive matching
    Given plan "alpha" has ticket "Add LOGIN Flow"
    When I run `crew search --plan alpha.json --query login`
    Then the ticket appears in the output

  Scenario: No matches
    Given plan "alpha" has ticket "Add login flow"
    When I run `crew search --plan alpha.json --query logout`
    Then no tickets appear in the output
