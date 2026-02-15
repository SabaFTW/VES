import matplotlib.pyplot as plt
import json
import os

# Define the absolute path for the evidence directory
evidence_dir = '/home/saba/VES/TROJAN_HORSE/evidence/realpage_yieldstar'

# Naloži podatke
report_path = os.path.join(evidence_dir, 'consistency_report.json')
with open(report_path, 'r') as f:
    report = json.load(f)

# Pripravi podatke za graf
clusters = report['top_duplicate_clusters']
prices = list(clusters.keys())
counts = [clusters[price]['count'] for price in prices]
sources = [len(clusters[price]['sources']) for price in prices]

# Ustrei graf
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('YieldStar Algorithmic Pricing Analysis', fontsize=16)

# Graf 1: Pogostost cen
ax1.bar(prices, counts, color=['#ff4136' if count > 1 else '#0074D9' for count in counts])
ax1.set_title('PONAVLJAJOČE SE CENE ČEZ MESTA')
ax1.set_ylabel('Število pojavitev')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Graf 2: Število virov
ax2.bar(prices, sources, color='#2ECC40')
ax2.set_title('ŠTEVILO MEST PO CENAH')
ax2.set_ylabel('Število mest')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
output_path = os.path.join(evidence_dir, 'consistency_visualization.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Visualization saved to {output_path}")
