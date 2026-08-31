---
captured: 2026-08-24T21:37:22+00:00
session: a6b4167c-c8f2-43e2-9d31-d26e66f642c9
cwd: /Users/chidionyema/dev/code/idp
chars: 1708
source: founder prompt, verbatim (founder-doc-capture.py)
---

To create a ruleset that applies across all repositories in your GitHub organization at once, you can define your ruleset in a JSON file and apply it using a single gh api command.  To target every repository, you need to use the ~ALL keyword in the repository_name condition.  Here is how you can do it in one go:1. Create your ruleset.json fileCreate a JSON file with your desired rules. This example protects the default branch (e.g., main) across all repositories in the organization by preventing branch deletions and force pushes:JSON{
  "name": "Org-Wide Default Branch Protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "repository_name": {
      "include": [
        "~ALL"
      ],
      "exclude": []
    },
    "ref_name": {
      "include": [
        "~DEFAULT_BRANCH"
      ],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "deletion"
    },
    {
      "type": "non_fast_forward"
    }
  ]
}
2. Apply it with a single gh commandOnce your JSON file is saved, run the following GitHub CLI command, replacing YOUR_ORG_NAME with your actual organization name:  Bashgh api /orgs/YOUR_ORG_NAME/rulesets --method POST --input ruleset.json
Key details:--input ruleset.json: This flag reads the JSON payload directly from your file and formats it appropriately for the API request.  "repository_name": { "include": ["~ALL"] }: This specific condition tells GitHub to apply this ruleset to every current and future repository within the organization.  "enforcement": "active": This ensures the rule is enforced immediately. If you want to test it silently first to see what it would block, you can change this to "evaluate" (requires GitHub Enterprise).
