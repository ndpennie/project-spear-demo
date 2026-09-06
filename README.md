# Project Spear — Threat-Triage Dashboard (Public Demo)

**Anticipatory, multi-modal, human-in-the-loop detection of coordinated harmful activity across social platforms.**

Project Spear is the operational core of the **GIPEC AI²** Anticipatory Intelligence platform: AI finds and scores potentially harmful content, and a trained analyst verifies, grades and reports it — every finding explainable, evidence-graded, and auditable.

**The analyst decides. The system never reports anything on its own.**

> **What this demo is.** The dashboard is real and connected to a live backend. It performs genuine searches, runs real vision and audio analysis, and cites real platform policies. It does **not** ship with anyone's private data, and it no longer loads invented sample incidents — the queue starts empty and fills only with what an analyst actually captures. The detection codebook, the validated case corpus and the production connectors live in a **private repository**.

**Patent pending** — U.S. Provisional Patent Application filed August 2026 (inventors Eric Feinberg & Demetrick Pennie).

---

## What it does

**One box.** Paste a link, type a `#hashtag` or an `@handle`, or ask a question — the app works out what you meant.

**Sees images.** Upload, drag or paste a screenshot and a vision model describes what it actually shows: corner watermarks, flags, disguised logos, symbols hidden in negative space, foreign-language text with an English translation. Analysis starts on drop; the plain-language verdict appears immediately.

**Hears video and audio.** Video is scanned frame-by-frame *and* the soundtrack is transcribed and translated — a clip with innocuous pictures and a jihadi nasheed on the audio track is caught by the audio alone. Standalone recordings can be interpreted the same way, in any language.

**Reads Arabic and other scripts.** In-browser OCR runs English and Arabic; the vision model handles the rest and translates.

**Searches real sources.** Telegram public channels, Bluesky, Mastodon/fediverse, 8kun (text only) and Odysee, plus open-web account discovery — merged into one result list, unscored until captured.

**Cites the actual policy.** A verified index of platform policies maps each finding to the real policy it engages, by its published name, with a link. Meta, YouTube and X were read directly from those companies' own policy pages.

**Explains itself.** On any accepted incident the analyst can ask why it is happening, why it breaks the platform's rules, **why the platform's own AI missed it**, and what to do next — with the full finding handed to the model as context.

**Keeps a record.** Every image, video and recording analysed is logged with its verdict and kept between sessions, filterable by date and exportable.

---

## Scoring happens on capture, not on search

Search results arrive **unscored**. Running a detection codebook over search-engine snippets produces false positives — an early build scored a chocolate retailer as a narcotics hit — so scoring is deliberately deferred until the system has the real content. This matters: a queue full of false positives destroys an analyst's credibility with the platforms they report to.

## What it cannot do, and why

- **Facebook and Instagram posts cannot be searched.** Meta blocks crawlers. There is no workaround at any price without Meta Content Library access (which is limited to academic and non-profit research). Those posts enter the system by analyst capture.
- **X/Twitter post search** requires a paid API tier. Accounts still surface through open-web discovery; their individual posts do not.
- **Snapchat** has no public search API at all.
- **Gab and Rumble** refuse automated access.
- **Imageboards are read text-only.** No image, thumbnail or filename is ever fetched or stored from 4chan or 8kun.

The dashboard states all of this on-screen, so an empty result is never mistaken for an all-clear.

## Child safety

Suspected child sexual exploitation is routed, never triaged. The media is not stored, hashed, described or placed in the normal queue — the system produces a provenance-only referral for the CyberTipline. Programmatic submission is reserved to registered Electronic Service Providers under 18 U.S.C. §2258A.

## Threat domains

Violent extremism · domestic terrorism · recruitment & glorification · incitement · financing · operational planning · narcotics · counterfeit & dangerous medicines · public-safety threats · child safety · self-harm promotion · inauthentic AI accounts

---

*Proprietary and confidential. The codebook, validated corpus, production connectors and detection models are not in this repository.*
