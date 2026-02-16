# ⚙️ ENGINE NOTES: Visualizing the Drift

**Status:** CONCEPTUAL
**Goal:** Transform static JSON datasets into interactive "Drift Graphs."

## 1. The Visualization Concept

We do not want a standard linear timeline. We want a **Drift Graph**.

* **X-Axis:** Time (T0 to T9).
* **Y-Axis:** Narrative Certainty (0 = Ridicule, 100 = Consensus).
* **The Curve:** Should visually demonstrate the "Lag."

## 2. Recommended Stack

To keep the project lightweight and GitHub Pages compatible:

* **Library:** `Vis.js` or `Chart.js`.
* **Data Source:** Fetch directly from the `/timeline_examples/*.json` files.
* **Logic:**
    1. Parse `t0_date` and `t9_date` to set the X-range.
    2. Plot `drift_points` as nodes on the curve.
    3. Color code the curve based on `t9_status` (Red = Too Late, Green = Timely).

## 3. Future Features (v0.2)

* **Overlay Mode:** Compare "ManBearPig" drift vs. "Lab Leak" drift on the same graph.
* **Source Preview:** Hover over a node to see the `evidence` source URL.
* **The "Apology Gap" Metric:** Automatically calculate the time difference between T0 and T9 in days.

> "Data without visualization is just a database. Visualization without data is just art. We need both."
