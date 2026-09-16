#!/usr/bin/env python3
"""
Project Spear — scheduled sweep.

Runs on a GitHub Actions cron. For every tag on the watchlist it calls the same
/api/search endpoint the dashboard uses, merges the results, and writes sweep.json
next to index.html. The dashboard's "Watch" button reads that file and shows the
analyst only what is new since they last looked.

Three rules this script does not break:

  1. It never invents a result. Every row comes back from the live endpoint with a
     real URL, or it does not exist. There is no demo path and no placeholder row.
  2. It never invents a poster. The account is derived from the URL itself, exactly
     the way the dashboard does it, and when the URL does not identify a poster the
     row says so instead of guessing.
  3. It never scores anything. Search snippets are not evidence — scoring a snippet
     is how a chocolate retailer once came back as a counterfeit stimulant sale.
     These are unscored leads. A human captures and scores the ones that matter.

It also separates content OF a movement from reporting ABOUT it, because a hashtag
match cannot tell those apart and reporting a researcher to a platform is both wrong
and self-defeating.
"""

import json
import os
import pathlib
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import urllib.request
import urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = os.environ.get("SPEAR_API", "https://project-spear-backend.onrender.com").rstrip("/")
WATCHLIST = ROOT / "watchlist.json"
OUT = ROOT / "sweep.json"
MAX_RESULTS = 400
TIMEOUT = 240

# Research, monitoring, news, government and academic domains. Content here is
# reporting ABOUT the movement. It is kept (it is useful context) but marked, and
# the dashboard holds it out of anything destined for a platform takedown queue.
REFERENCE_SOURCES = {
    "adl.org", "globalextremism.org", "counterextremism.com", "splcenter.org",
    "isdglobal.org", "gnet-research.org", "start.umd.edu", "icct.nl", "ctc.westpoint.edu",
    "memri.org", "siteintelgroup.com", "bellingcat.com", "extremism.gwu.edu",
    "politicalresearch.org", "hopenothate.org.uk", "canadianantihate.ca",
    "moonshotteam.com", "techagainstterrorism.org", "radicalisationresearch.org",
    "nytimes.com", "washingtonpost.com", "wsj.com", "reuters.com", "apnews.com",
    "bbc.com", "bbc.co.uk", "theguardian.com", "npr.org", "pbs.org", "cnn.com",
    "nbcnews.com", "abcnews.go.com", "cbsnews.com", "rollingstone.com", "vice.com",
    "wired.com", "theatlantic.com", "propublica.org", "motherjones.com",
    "thedailybeast.com", "newsweek.com", "time.com", "usatoday.com", "latimes.com",
    "politico.com", "axios.com", "ctvnews.ca", "cbc.ca", "globalnews.ca",
    "thestar.com", "nationalpost.com", "justice.gov", "fbi.gov", "dhs.gov",
    "courtlistener.com", "wikipedia.org",
}

PLATFORM_HOSTS = {
    "instagram.com", "facebook.com", "fb.com", "threads.net", "threads.com",
    "x.com", "twitter.com", "tiktok.com", "t.me", "telegram.org", "bsky.app",
    "youtube.com", "reddit.com", "mastodon.social",
}

CHROME_PATHS = {
    "features", "about", "help", "legal", "privacy", "terms", "policies", "business",
    "ads", "download", "accounts", "login", "signup", "explore", "directory", "safety",
    "support", "press", "careers", "brand",
}


def host_of(url: str) -> str:
    try:
        return (urllib.parse.urlparse(url).hostname or "").replace("www.", "", 1).lower()
    except Exception:
        return ""


def is_platform_chrome(url: str) -> bool:
    """A site: search for a platform returns that platform's own corporate pages.
    instagram.com/about is not a finding. Drop those before a human ever sees them."""
    h = host_of(url)
    if not h:
        return True
    path = (urllib.parse.urlparse(url).path or "").rstrip("/")
    if h.split(".")[0] in {"about", "help", "business", "developers", "newsroom",
                           "engineering", "investor", "transparency"}:
        return True
    is_plat = any(h == p or h.endswith("." + p) for p in PLATFORM_HOSTS)
    if not is_plat:
        return False
    if path == "":
        return True
    first = path.lstrip("/").split("/")[0].lower()
    return first in CHROME_PATHS


def source_kind(url: str) -> str:
    h = host_of(url)
    if not h:
        return "primary"
    if any(h == d or h.endswith("." + d) for d in REFERENCE_SOURCES):
        return "reference"
    if h.endswith(".gov") or h.endswith(".edu"):
        return "reference"
    return "primary"


def poster_from_url(url: str) -> str:
    """The account, derived from the real URL. Never invented. Mirrors posterFromUrl()
    in index.html — if you change one, change the other."""
    try:
        x = urllib.parse.urlparse((url or "").split(" ")[0])
    except Exception:
        return "Unknown — not established"
    h = (x.hostname or "").replace("www.", "", 1).lower()
    seg = [s for s in (x.path or "").split("/") if s]
    if not h:
        return "Unknown — not established"
    if h == "bsky.app" and len(seg) >= 2 and seg[0] == "profile":
        return seg[1]
    if seg and seg[0].startswith("@"):
        return f"{seg[0]}@{h}"
    if h in ("x.com", "twitter.com") and seg and seg[0] not in ("i", "home", "search", "hashtag", "explore"):
        return "@" + seg[0]
    if h in ("t.me", "telegram.me"):
        c = seg[1] if (seg and seg[0] == "s" and len(seg) > 1) else (seg[0] if seg else "")
        if c:
            return "t.me/" + c
    if h.endswith("reddit.com") and len(seg) >= 2 and seg[0] == "r":
        return "r/" + seg[1]
    if h.endswith("youtube.com"):
        if seg and seg[0].startswith("@"):
            return seg[0]
        if len(seg) >= 2 and seg[0] == "channel":
            return "youtube.com/channel/" + seg[1]
    if h.endswith("tiktok.com") and seg and seg[0].startswith("@"):
        return seg[0]
    if h in ("instagram.com", "facebook.com") and seg and seg[0] not in ("p", "reel", "explore", "groups", "watch", "share"):
        return "@" + seg[0]
    return f"{h} (site — poster not identified)"


def search(tag: str, cfg: dict) -> list:
    body = json.dumps({
        "tag": tag,
        "terms": cfg.get("terms", []),
        "channels": cfg.get("channels", []),
        "platforms": cfg.get("platforms", []),
    }).encode()
    req = urllib.request.Request(
        f"{API}/api/search",
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "project-spear-sweep/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  ! {tag}: HTTP {e.code}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"  ! {tag}: {e}", file=sys.stderr)
        return []
    out = data.get("results") or []
    print(f"  {tag}: {len(out)} result(s) · sources={data.get('sources')}")
    return out


def main() -> int:
    cfg = json.loads(WATCHLIST.read_text())
    tags = cfg.get("tags") or []
    if not tags:
        print("watchlist.json has no tags — nothing to sweep", file=sys.stderr)
        return 1

    seen, rows = set(), []
    for tag in tags:
        for r in search(tag, cfg):
            url = (r.get("url") or "").strip()
            if not url or not url.startswith("http"):
                continue
            key = url.split("?")[0].split("#")[0].rstrip("/").lower()
            if key in seen:
                continue
            if is_platform_chrome(url):
                continue
            seen.add(key)
            kind = source_kind(url)
            rows.append({
                "url": url,
                "title": (r.get("title") or "")[:300],
                "snippet": (r.get("snippet") or "")[:600],
                "platform": r.get("platform") or "web",
                "poster": poster_from_url(url),
                "found_for": "#" + tag,
                "source_kind": kind,
                "before_you_report": (
                    "REFERENCE — reporting ABOUT the movement. Do not submit to a platform."
                    if kind == "reference" else
                    "Stance NOT verified. Open the link and confirm the poster is promoting "
                    "this, not documenting or opposing it, before reporting."
                ),
                "scored": False,
            })
            if len(rows) >= MAX_RESULTS:
                break
        time.sleep(2)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tags": tags,
        "count": len(rows),
        "reportable": sum(1 for r in rows if r["source_kind"] == "primary"),
        "reference": sum(1 for r in rows if r["source_kind"] == "reference"),
        "note": ("Unscored leads from the scheduled sweep. Nothing here has been scored, "
                 "verified for stance, or reported. A human captures and rules on each one."),
        "results": rows,
    }
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False))
    print(f"wrote {OUT} — {len(rows)} lead(s) "
          f"({payload['reportable']} primary, {payload['reference']} reference)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
