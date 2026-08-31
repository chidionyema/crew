---
captured: 2026-08-25T19:53:27+00:00
session: 70d8226b-20ff-4038-b968-16726278985d
cwd: /Users/chidionyema/dev/code
chars: 2000
source: founder prompt, verbatim (founder-doc-capture.py)
---

updte fron genini, what do you think A retail storefront treats the company like a vendor selling static reports, when the actual requirement is a **unified platform console**—a single front door for an AI research and tooling company that exposes APIs, interactive workbenches, and research artifacts alongside product offerings.

**The Platform Console vs. The Storefront**

* **Commerce as Background Infrastructure:** Medusa and Stripe belong strictly in the platform layer (`idp`) as headless utilities handling billing, tiering, and API key entitlements. They should never dictate the company's front-end architecture or product identity.
* **Unified Workspace UI:** The front door must be an enterprise platform console where users manage API keys, deploy agents, review real-time telemetry, and interact with tooling across all products (Prospector, Hermes, and future research engines).

**Essential Front-End Platform Capabilities**

* **Interactive Artifact Viewer:** Web-based surfaces for research outputs that render live data, interactive evaluation suites, and Brier-score calibration metrics directly in the browser instead of static files.
* **Developer & API Surface:** A self-serve developer portal with interactive API documentation, usage analytics, webhook management, and trace logging integration.
* **Modular Product Shell:** A high-performance web architecture (e.g., Next.js platform shell) designed with a unified design system so new research tools can be mounted as sub-apps or routes without rebuilding the core front end.

**Immediate Strategic Pivot**

* **Reframe the Storefront Work:** Encapsulate the Medusa storefront as an isolated checkout component within the platform, rather than making it the primary identity of the codebase.
* **Specify the Platform Shell (`Platform.Web`):** Shift focus from a retail shop to building a platform shell that authenticates users, exposes API management, and routes to individual AI product interfaces., i like ur idea also
