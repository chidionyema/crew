---
captured: 2026-08-29T16:55:59+00:00
session: 80471694-3138-4645-a870-868210b81120
cwd: /Users/chidionyema/dev/code/crew
chars: 3429
source: founder prompt, verbatim (founder-doc-capture.py)
---

Short version: you can't remove the human step, but you can make it O(1) per organisation instead of O(n) per resource, and you can make it a single click instead of a form. Every product that does this well is applying one of about four patterns.

1. Turn the credential ceremony into a consent screen. The reason connecting Stripe or Slack feels frictionless isn't that no trust is established — it's that the trust step is an OAuth redirect. User clicks "Connect", sees "X wants to do Y", clicks Approve, lands back in your app with tokens. No form, no transcription, no ID. The provider has to support a third-party app model for this, and Tailscale's OAuth clients are self-issued rather than third-party-app-issued, so you don't get it here. But when you're the one building the product, this is the shape to aim for.

2. If you can't avoid the console, prefill it. AWS's version is the "Launch Stack" link — one URL with every parameter baked in, the customer clicks through a wizard they never type into, and the ARN comes back to you. Datadog, Wiz and Snyk all onboard this way. Applied here: your tooling computes the subject from the GitHub API, builds a deep link into the Tailscale credential form with issuer and subject prefilled, and the human's entire job is pressing Save. That's a 5-second ceremony instead of a 5-minute one, and the transcription error class disappears entirely.

3. Never make a human carry a value between two systems. Repo ID, owner ID, audience, client ID — all of these are derivable by code. The moment a person is copying a string from one tab to another, you've designed it wrong. This is the specific thing that went wrong in your case: the agent asked you to hand-type a 60-character subject it could have computed itself.

4. Bootstrap from a trust anchor you already have, not from zero. The chicken-and-egg only bites if you're starting cold. If any machine is already on the tailnet, or any credential already exists with key-write scope, that becomes the seed and everything else is minted from it. Enterprise onboarding is exactly this: one ceremony at contract signing, machine-issued forever after. Your agent's mistake was treating "needs a credential" as "needs the CEO" rather than "needs a seed, which we may already have."

Then the operational half, which matters as much:

Preflight, don't discover. The failure here wasn't that a human step existed. It was that the agent hit it at minute forty, after ten feature files and four PRs. A doctor/preflight step that verifies every trust prerequisite before dependent work starts, and fails with one consolidated ask, turns "you interrupted me five times" into "approve these two things once."

Close the loop automatically. After the human acts, poll until the exchange succeeds. If it fails, show the diff between expected and received — which is exactly what Tailscale's error panel gives you — and offer the corrected value as a one-click apply rather than prose telling them what to type.

If you were productising this for other people, the pitch writes itself: everyone integrating GitHub OIDC with anything broke on 15 July, most of them are still hand-editing trust policies, and the fix is mechanical. A tool that reads your workflows, resolves the real subjects from the GitHub API, and rewrites the trust config on the relying-party side is a genuinely useful thing that doesn't currently exist in one piece.
