# 📉 T0-T9 TIMELINE SPECIFICATION

**Purpose:** To visualize the drift of narrative over time (The "ManBearPig" Effect).

## The Axis of Drift

We track stories not by "Truth/Falsehood" (which is subjective in the moment), but by **Evolution over Time**.

* **T0 (The Spark):** The initial claim, leak, or event. Often dismissed or ridiculed.
* **T1-T3 (The Denial):** The "Immune Response" of the system. Mockery, censorship, "Debunking."
* **T4-T6 (The Shift):** Silent edits. Changing headlines. "It was never a conspiracy theory."
* **T7-T8 (The Integration):** The claim becomes normalized, but the origin is forgotten.
* **T9 (The History):** The full arc is visible. The "Apology" (or lack thereof).

## Data Structure (JSON)

Every entry in Manifest Orion must follow this schema:

```json
{
  "narrative_id": "string (unique-slug)",
  "title": "string",
  "t0_event": {
    "date": "ISO8601",
    "claim": "string",
    "source_url": "string (archive.org link preferred)"
  },
  "drift_points": [
    {
      "phase": "T3",
      "action": "Denial",
      "actor": "Media/Institution",
      "evidence": "string"
    }
  ],
  "t9_status": "Unresolved | Vindicated | Debunked | Forgotten"
}
```
