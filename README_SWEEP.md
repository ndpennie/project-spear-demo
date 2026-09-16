# Always-on searching — how to switch it on

Three files. They go in `ndpennie/project-spear-demo`, the same repo as `index.html`.

```
.github/workflows/sweep.yml     <- the timer
scripts/sweep.py                <- the search
watchlist.json                  <- what it searches
```

GitHub runs the timer for free on public repos. There is no server to keep awake and
nothing to pay for beyond the Render backend already running.

## What happens once it is on

Every 6 hours GitHub calls the same `/api/search` the dashboard uses, once per tag on
the watchlist, merges the results, and commits `sweep.json` back into the site. When
Eric opens the dashboard and turns **Watch** on, it reads that file and shows him only
what is new since the last time he looked. He captures the ones worth capturing.

First run, live, just now: **93 leads across 5 tags** — 90 primary, 3 reference.

## Switching it on

1. Upload the three files to the repo (keep the folder structure).
2. Repo → **Settings → Actions → General → Workflow permissions** → set
   **Read and write permissions**. Without this the commit step fails.
3. Repo → **Actions** tab → **Scheduled sweep** → **Run workflow**, to prove it works
   before waiting six hours.
4. Check that `sweep.json` appeared at the top level of the repo.

## Changing what it watches

Edit `watchlist.json` in GitHub's web editor and commit. Currently:

| | |
|---|---|
| **tags** | Will2Rise, ActiveClub, Diagalon, SecondSons, NS13 |
| **terms** | narrow each tag toward the nefarious end |
| **channels** | Telegram channels read directly |

Diagalon, SecondSons and NS13 came out of the adjacent-tag mining on the live
`#Will2Rise` search — they are where the network actually travels.

## What this deliberately does not do

- **It does not score.** Search snippets are not evidence. Scoring a snippet is how a
  chocolate retailer once came back as a counterfeit stimulant sale. Everything in
  `sweep.json` is an unscored lead until a human captures it.
- **It does not invent.** Every row has a real URL from the live endpoint. The account
  is derived from that URL, and when the URL does not identify a poster the row says
  so rather than guessing a name.
- **It does not report.** Nothing is sent anywhere. A human rules on every item.
- **It does not confuse coverage with content.** ADL, the Global Extremism Registry,
  Rolling Stone and anything on a `.gov` or `.edu` are marked `reference` and carry
  *"reporting ABOUT the movement — do not submit to a platform."*

## Why not the backend crawler

`/api/hunt/sweep` on the Render service still returns three fabricated `.example`
targets alongside the real ones. Until that ships fixed, do not call
`/api/hunt/start` — an unattended crawler that invents URLs will quietly fill the
review queue overnight, and an invented URL in a Meta report is the one mistake that
costs an analyst their standing. The work order for that fix is in
`specs/HUNT_CONNECTOR_FIX.md`.

This sweep uses the search path instead — the one that returned the 30 real results.
