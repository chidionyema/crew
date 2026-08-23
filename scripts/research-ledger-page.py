#!/usr/bin/env python3
"""Render science/RESEARCH-LEDGER.jsonl as one page the founder can read on a phone.

LAW 31: he reads the state, he does not run the query. LAW 28: a ledger nobody
reads is not a ledger. This turns the JSONL into the thing he actually opens.

    research-ledger-page.py [--out PATH]

Reads the ledger beside it, writes HTML. Regenerate and republish to the same
artifact URL whenever a research pass lands.
"""
import argparse, html, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, "science", "RESEARCH-LEDGER.jsonl")

CSS = """
:root{
  --ground:#F3F4F6; --surface:#FFFFFF; --ink:#14181D; --ink-soft:#535C67;
  --rule:#DCE0E6; --accent:#15655A; --accent-soft:#E2EFEC;
  --warn:#8C5214; --warn-soft:#F6EBDD; --code:#F1F3F5;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0D1014; --surface:#151A20; --ink:#E3E7EB; --ink-soft:#96A1AD;
    --rule:#252C34; --accent:#59B6A5; --accent-soft:#152A27;
    --warn:#D89A52; --warn-soft:#2A2116; --code:#1B2128;
  }
}
:root[data-theme="dark"]{
  --ground:#0D1014; --surface:#151A20; --ink:#E3E7EB; --ink-soft:#96A1AD;
  --rule:#252C34; --accent:#59B6A5; --accent-soft:#152A27;
  --warn:#D89A52; --warn-soft:#2A2116; --code:#1B2128;
}
*{box-sizing:border-box}
body{
  background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:16.5px; line-height:1.62; margin:0;
  -webkit-text-size-adjust:100%;
}
.wrap{max-width:50rem;margin:0 auto;padding:2.6rem 1.25rem 5rem;display:flex;flex-direction:column;gap:2rem}
header{display:flex;flex-direction:column;gap:.85rem;padding-bottom:1.6rem;border-bottom:2px solid var(--ink)}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:.68rem;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft);
}
h1{
  font-family:"Newsreader",Georgia,serif; font-weight:500; font-size:clamp(2rem,6vw,2.9rem);
  line-height:1.1; margin:0; letter-spacing:-.015em; text-wrap:balance;
}
.lede{color:var(--ink-soft);margin:0;max-width:46ch}
.counts{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.3rem}
.count{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
  border:1px solid var(--rule);border-radius:2px;padding:.28rem .55rem;
  color:var(--ink-soft);background:var(--surface);
  font-variant-numeric:tabular-nums;
}
.count b{color:var(--ink);font-weight:600}
article{
  background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  padding:1.5rem 1.35rem;display:flex;flex-direction:column;gap:1.05rem;
}
.head{display:flex;flex-direction:column;gap:.5rem}
.meta{display:flex;flex-wrap:wrap;gap:.55rem;align-items:center}
.date{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.74rem;
  color:var(--accent);font-weight:600;letter-spacing:.04em;
}
.owner{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.7rem;color:var(--ink-soft)}
h2{
  font-family:"Newsreader",Georgia,serif;font-weight:500;font-size:1.42rem;
  line-height:1.25;margin:0;letter-spacing:-.008em;text-wrap:balance;
}
.block{display:flex;flex-direction:column;gap:.34rem}
.label{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.66rem;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft);
}
.block p{margin:0}
.refused{color:var(--warn);font-weight:600}
.metric{
  background:var(--code);border-left:2px solid var(--accent);
  padding:.75rem .9rem;display:flex;flex-direction:column;gap:.5rem;border-radius:0 2px 2px 0;
}
.metric .row{display:flex;flex-direction:column;gap:.15rem}
.metric .k{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.66rem;
  letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft);
}
.metric .v{font-size:.92rem}
.pending{
  display:inline-block;background:var(--warn-soft);color:var(--warn);
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.72rem;
  padding:.14rem .45rem;border-radius:2px;font-weight:600;
}
details{border-top:1px solid var(--rule);padding-top:.85rem}
summary{
  cursor:pointer;font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent);
  list-style:none;
}
summary::-webkit-details-marker{display:none}
summary::before{content:"▸ ";display:inline-block;transition:transform .15s}
details[open] summary::before{content:"▾ "}
summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px}
ol.sources{
  margin:.8rem 0 0;padding-left:1.5rem;display:flex;flex-direction:column;gap:.4rem;
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.76rem;
}
ol.sources li{overflow-wrap:anywhere}
a{color:var(--accent)}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
footer{
  border-top:1px solid var(--rule);padding-top:1.2rem;color:var(--ink-soft);
  font-size:.84rem;display:flex;flex-direction:column;gap:.5rem;
}
footer code{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.8rem;background:var(--code);padding:.1rem .3rem;border-radius:2px}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
"""

def esc(s): return html.escape(str(s), quote=False)

def render(entries):
    n_sources = sum(len(e["sources"]) for e in entries)
    n_open = sum(1 for e in entries if e.get("metric_after") is None and not e.get("abandoned"))
    parts = [
        '<title>Estate Research Ledger</title>',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Newsreader:opsz,wght@6..72,400;6..72,500&'
        'family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;600&display=swap">',
        f'<style>{CSS}</style>',
        '<div class="wrap">',
        '<header>',
        '<div class="eyebrow">crew · science/RESEARCH-LEDGER.jsonl</div>',
        '<h1>Estate Research Ledger</h1>',
        '<p class="lede">Every research pass the estate has run, what it read, '
        'what it decided, and the number that will say whether the decision worked.</p>',
        '<div class="counts">'
        f'<span class="count"><b>{len(entries)}</b> entries</span>'
        f'<span class="count"><b>{n_sources}</b> sources read</span>'
        f'<span class="count"><b>{n_open}</b> awaiting a measurement</span>'
        '</div>',
        '</header>',
    ]
    for e in sorted(entries, key=lambda x: x["date"], reverse=True):
        after = e.get("metric_after")
        parts.append('<article>')
        parts.append('<div class="head"><div class="meta">'
                     f'<span class="date">{esc(e["date"])}</span>'
                     f'<span class="owner">owner: {esc(e["owner"])}</span></div>'
                     f'<h2>{esc(e["question"])}</h2></div>')
        dec = esc(e["decision_fed"]).replace(
            "REFUSED:", '<span class="refused">REFUSED:</span>')
        parts.append(f'<div class="block"><div class="label">Decision it fed</div><p>{dec}</p></div>')
        parts.append('<div class="block"><div class="label">Findings</div>'
                     f'<p>{esc(e["findings"])}</p></div>')
        parts.append(
            '<div class="metric">'
            f'<div class="row"><span class="k">Metric</span><span class="v">{esc(e["metric"])}</span></div>'
            f'<div class="row"><span class="k">Before</span><span class="v">{esc(e["metric_before"])}</span></div>'
            '<div class="row"><span class="k">After</span><span class="v">'
            + (esc(after) if after else '<span class="pending">not yet measured</span>')
            + '</span></div></div>')
        srcs = "".join(
            f'<li><a href="{html.escape(s, quote=True)}" target="_blank" rel="noopener">{esc(s)}</a></li>'
            for s in e["sources"])
        parts.append(f'<details><summary>{len(e["sources"])} sources</summary>'
                     f'<ol class="sources">{srcs}</ol></details>')
        parts.append('</article>')
    parts.append(
        '<footer>'
        '<div>An entry with no measurement after 14 days fails '
        '<code>scripts/verify.d/80-research-ledger.sh</code>, and so does a ledger '
        'whose newest entry is over 7 days old. That check is what stops this page '
        'becoming a museum.</div>'
        '<div>Rebuilt from the ledger by <code>scripts/research-ledger-page.py</code>.</div>'
        '</footer></div>')
    return "\n".join(parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "science", "research-ledger.html"))
    a = ap.parse_args()
    entries = [json.loads(l) for l in open(LEDGER, encoding="utf-8") if l.strip()]
    if not entries:
        print("FAIL: ledger is empty", file=sys.stderr); return 1
    open(a.out, "w", encoding="utf-8").write(render(entries))
    print(f"{a.out}  {os.path.getsize(a.out)} bytes  {len(entries)} entries")
    return 0

if __name__ == "__main__":
    sys.exit(main())
