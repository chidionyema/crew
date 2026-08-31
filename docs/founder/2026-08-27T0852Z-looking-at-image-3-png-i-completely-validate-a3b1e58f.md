---
captured: 2026-08-27T08:52:21+00:00
session: a0d64ea4-d03d-4d1f-84e1-e1739e05c615
cwd: /Users/chidionyema/dev/code/idp/.claude/worktrees/crew459-portal-polish
chars: 2657
source: founder prompt, verbatim (founder-doc-capture.py)
---

Looking at image_3.png, I completely validate your frustration. That mobile view is practically brokenâ€”the search bar is colliding with the title, and the table columns are squeezed so tightly the text is forced to wrap awkwardly.

Backstage is notoriously optimized for desktop because it assumes developers are at their primary workstations. However, a catalog alone is just a glorified spreadsheet; it won't 100x your team's velocity on its own.

Here is how to fix the immediate UI pain and unlock the actual systemic value of Backstage as an Internal Developer Portal (IDP).

Fixing the Mobile UI

Responsive Table Overrides: Backstage is built on Material-UI (MUI). You can customize the CatalogTable component using MUI breakpoints to hide secondary columns (like "System," "Owner," and "Type") on mobile screens. Just show the "Name" and let users tap into the component for details.
Theme Adjustments: Supply a custom app theme in your Backstage codebase to fix the header margins and flexbox behaviors, preventing the search bar from overlapping the layout.
Embrace Desktop-First: Candidly, most heavy operational work isn't done from a phone. Dedicate 90% of your UI/UX effort to the desktop experience where your engineers actually spend their day.
How to 100x Backstage as a System

To get the most out of Backstage, you have to transition it from a passive directory to an active operational hub.

Pave "Golden Paths" with Software Templates: This is the single highest-value feature. Use the Scaffolder plugin to let developers spin up new projects in minutes. A developer fills out a form, and Backstage generates the boilerplate code, sets up the GitHub repo, and configures the CI/CD pipeline based on your organization's exact standards.
Kill Knowledge Silos with TechDocs: Implement "Docs Like Code." Engineers write Markdown documentation directly inside their repositories, and Backstage automatically aggregates, renders, and makes it searchable globally.
Eliminate Context Switching (Plugins): Stop making developers open ten different browser tabs. Bring the context to them by integrating plugins for Kubernetes (to view pod health), GitHub Actions (to trigger/view builds), and PagerDuty (to see who is on call for a specific service).
Gamify Engineering Quality: Use plugins like Tech Insights or Soundcheck to grade your services. Create a scorecard that checks if a service has a runbook, meets test coverage minimums, or is using deprecated libraries, pushing teams to improve their own components.
Are you currently using the Scaffolder for templates, or is your Backstage instance strictly acting as a directory right now?
