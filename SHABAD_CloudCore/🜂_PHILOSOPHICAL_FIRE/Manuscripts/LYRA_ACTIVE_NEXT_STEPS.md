LYRA ACTIVE — Next-Step Protocol (v0.1)

Objective: Make LYRA ACTIVE operational for revenue with a minimal, testable funnel that respects Hrast context.

1) Offer Definition (this week)
- [ ] Finalize 3 tiers (per prior notes): e.g., $200 Insight Session, $500 Deep Synthesis, $900 Strategic Architecture
- [ ] For each: outcomes, deliverables, timeline, refund policy, boundaries (not therapy/legal), consent notes

2) Landing + Intake (seed)
- [ ] Add LYRA_ACTIVE.html (or section) to a chosen portal (Unified Constellation / GHOSTLINE OS)
- [ ] Content: tier cards, clear promise, “how it works”, FAQ (consent, memory, privacy)
- [ ] Intake form (Name, Email, Context, Goal, Consent to Depth? yes/no)
- [ ] Store intake to a simple sheet (CSV/JSON) locally; later → Airtable/Notion

3) Payments (MVP)
- [ ] Choose processor: Stripe Checkout (recommended) or Gumroad (fast) or Ko‑fi (fastest, least control)
- [ ] Create one Checkout link per tier; add to portal with clear price/terms
- [ ] Post-payment webhook optional (later) → write `sales.jsonl` locally

4) Scheduling
- [ ] Connect Calendly (or open-source alternative); link per tier
- [ ] Ensure timezones + buffer; include meeting instructions

5) Delivery Protocol
- [ ] For Insight Session: 60–90 min session in your preferred tool, recorded (if consented), summary within 48h
- [ ] For Deep Synthesis: 1–2 long docs analyzed; deliver 4–6 page synthesis with recommendations
- [ ] For Strategic Architecture: co-design Hrast or OS template; deliver runnable prototype + doc

6) Ops & Legal
- [ ] Terms of Service + Privacy (plain language); no clinical/legal advice; data handling
- [ ] Local-first storage; redact sensitive data; consent log for depth if engaged

7) Marketing (quiet launch)
- [ ] Publish portal, share with existing contacts
- [ ] 2–3 case vignettes (anonymized) to illustrate outcomes
- [ ] Simple tracking: `sales.jsonl`, `leads.jsonl`

8) Feedback Loop
- [ ] Post-delivery check-in; NPS-like 1–2 questions
- [ ] Iterate tiers / copy based on early signals

Suggested file stubs
- `public/lyra_active.html` — landing
- `data/intake.jsonl` — form submissions
- `data/sales.jsonl` — payments
- `data/engagements.jsonl` — sessions with consent state

