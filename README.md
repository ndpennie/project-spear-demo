# Project Spear — Threat-Triage Dashboard (Public Demo)

**Anticipatory, multi-modal, human-in-the-loop detection of coordinated harmful activity across social platforms.**

Project Spear is the operational core of the **GIPEC AI²** Anticipatory Intelligence platform: AI finds and scores potentially harmful content, and trained humans verify, grade, and report it — every finding explainable, evidence-graded, and auditable.

> **This repository is a demonstration only.** It runs entirely in your browser on **synthetic sample data** — no live platform access, no real accounts, no private data. The production backend, detection models, codebook, and connectors are in a **private repository**.
>
> **Patent pending** — U.S. Provisional Patent Application filed August 2026 (inventors Eric Feinberg & Demetrick Pennie). Proprietary and confidential.

**▶ Live demo:** https://ndpennie.github.io/project-spear-demo/

## Threat domains detected

Each item is scored 1–10, tiered (CRITICAL / HIGH / MEDIUM / LOW / MINIMAL), evidence-graded, and human-reviewed. Predictions are leads, never verdicts — nothing is auto-reported or auto-actioned.

- **Violent extremism** — propaganda, recruitment, glorification, incitement, financing, operational planning (the seven-layer Anticipatory Intelligence framework)
- **Domestic terrorism** — militia mobilization, accelerationist / "2A solution" slogans, targeting of officials or critical infrastructure
- **Narcotics** — illegal online drug sales (coded product/price/"menu" language, drug-sale emoji codes, illicit payment rails)
- **Counterfeit & dangerous medications** — fake M30/oxycodone, Adderall, Xanax, and fentanyl / "pressed-pill" indicators (treated as life-safety)
- **Public-safety threats** — targeted or mass-casualty threats, bomb / school / venue threats, swatting and doxxing of officials, and imminent self-harm (routed to wellbeing resources, not enforcement)
- **Child safety** — detected and routed only, to NCMEC CyberTipline / PhotoDNA hash-matching by cleared personnel; media is never stored, reproduced, or described
- **Self-harm / suicide promotion** — pro-suicide content and dangerous viral "challenges," distinguished from support and recovery content, which is not flagged

The taxonomy is **living**: content using dangerous vocabulary not yet in the codebook is flagged **⚡ EMERGING** and the novel indicators are surfaced for analyst review, so the system learns new patterns rather than only known ones.

## What the demo shows

- **Intake** — submit URLs, or upload a screenshot/photo (in-browser OCR + perceptual fingerprint + visible-element labels)
- **Explainable scoring** — per item: what you're seeing, why it's threatening, why the score, and what would change the verdict
- **Codebook & Teach** — the living dictionary of codes, symbols, and coded handles; analysts propose new terms, owners approve
- **Library** — upload context documents and reference images to inform the AI
- **Active Hunt** — an autonomous discovery crawler (synthetic connector in the demo) with an operator allowlist so investigators' own accounts are never flagged
- **Platform takedown reports** — human-approved report packets mapped to each platform's policy clause, with evidence and chain-of-custody
- **BrandGuard™** — advertiser brand-safety adjacency: flags where a monitored brand appears beside harmful content
- **Network view** — posters, URLs, shared links, and reposted media, connected

## Safeguards

Human-in-the-loop before any report · no autonomous takedown · ToS-compliant collection of public content only · bias controls (context over religious/ethnic imagery alone) · moderator wellbeing (blur-by-default, exposure rotation) · full audit trail.

---
GIPEC AI² · Project Spear — patent pending. For access to the production platform, contact GIPEC AI².
