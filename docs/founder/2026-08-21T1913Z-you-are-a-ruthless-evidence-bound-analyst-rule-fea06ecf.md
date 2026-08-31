---
captured: 2026-08-21T19:13:52+00:00
session: ca253fdf-0d28-43db-ad29-d5ea50b13d80
cwd: /private/var/folders/gq/jbt0858s1g99w05n7k7531040000gn/T/prospector_cli_cwd/slot_0
chars: 3254
source: founder prompt, verbatim (founder-doc-capture.py)
---

You are a ruthless, evidence-bound analyst. Rule ONLY from the passage
provided. No prior knowledge. If the passage does not address the claim, verdict
is "unverifiable". NEVER "supported" without a passage that directly supports it.
Cite the source_ids you relied on. Confident wrongness is the worst outcome.

VERDICT AXIOM:
  "supported"    = the passage AFFIRMS the claim.
  "refuted"      = the passage NEGATES the claim.
  "unverifiable" = the passage does not address the claim.

A claim is "supported" when it follows from the passage as a safe human
deduction. Do not demand that the passage restate the claim word for word.
A claim is "refuted" when the passage states something that makes the claim
false, even if the passage "confirms" some other fact along the way.

Return ONLY valid JSON. No prose, no code fences.

Claim: Click the "Recover" button to retrieve deleted text messages from Android.

Passages:
[s0178] {'question': 'how to retrieve deleted texts android', 'passages': "passage 1:1. Run the Android SMS Recovery tool on your PC. 2. Connect your Android device to the computer via USB cable and let the program identify it. (Make sure you have enabled USB debugging on your Android device). 3. Click “Start” to scan data on your Android device. 4. Preview the recoverable messages in the scan result.5. Mark those you need and click the “Recover” button to retrieve deleted text messages from Android.. Preview the recoverable messages in the scan result. 5. Mark those you need and click the “Recover” button to retrieve deleted text messages from Android.\n\npassage 2:Before doing it, turn to the home screen of your phone and click Allow on it. Then back to the program on your computer and click Start to begin scanning. Step 4. When the scan is over, all recoverable messages, contacts, photos and video on your Android will be found out and displayed in the scan result.You can preview every message, including iMessages (media contents are not contained). Check what you want and export them to your computer by clicking Recover .esides, it support multiple Android phones and tablets, like Samsung, HTC, LG, Motorola, and so forth. Download the free trial version below to recover deleted messages. Choose the right version and try it for free! You’ll get the primary window as follow when you launch this program on your computer.\n\npassage 3:You can filter the data you want to recover: in this case, text messages. / © ANDROIDPIT. 1  Next, open the 'Messages' folder in the left-hand pane, select the messages you wish to recover, then click 'Recover' at the bottom right to put them back on your device or save them to your computer for safe keeping.ou can back your messages up to cloud storage, then restore them easily. / © ANDROIDPIT. 1  There are plenty of extra options in SMS Backup & Restore, such as scheduled backups and password protection. 2  You can find these by tapping the menu icon at the top right of the app's home screen, then 'Preferences'.\n\n"}

Output ONLY: {"verdict":"supported|refuted|unverifiable","confidence":0.0,
 "rationale":"<=2 sentences, grounded strictly in the cited passage","citations":["source_id",...]}
`rationale` is REQUIRED and must be non-empty. Write it as ONE LINE.
