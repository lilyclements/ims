#!/usr/bin/env python3
"""
Generate figures for Chapter 17 exercises.
Creates histograms and bar charts for inference on two proportions exercises.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(47)

# Create output directory
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

# Define IMSCOL green color (similar to what's used in the R code)
IMSCOL_GREEN = '#569BBD'  # A teal/blue-green color

print("Generating Chapter 17 exercise figures...")

# Exercise 1: Asian American tobacco use - randomization distribution
print("\n1. Asian American tobacco use (hypothesis test)...")
# Data: Asian-Indian (n=4373, smokers=223), Chinese (n=4736, smokers=279)
# Observed difference: 223/4373 - 279/4736 = 0.051 - 0.059 = -0.008
# Generate randomization distribution centered at 0
fig, ax = plt.subplots(figsize=(8, 5))
differences = np.random.normal(0, 0.0045, 1000)  # SE ≈ 0.0045 based on pooled proportion
ax.hist(differences, bins=30, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax.axvline(-0.008, color='red', linestyle='--', linewidth=2, alpha=0.7)
ax.set_title('1,000 randomized differences', fontsize=12, fontweight='bold')
ax.set_xlabel('Difference in randomized proportions\n(Indian - Chinese)', fontsize=10)
ax.set_ylabel('Count', fontsize=10)
ax.set_xlim(-0.02, 0.02)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-01.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 2: Malaria vaccine - randomization distribution
print("2. Malaria vaccine (hypothesis test)...")
# Data: malaria vaccine (n=292, sick=89), control (n=147, sick=106)
# Observed difference: 89/292 - 106/147 = 0.305 - 0.721 = -0.416
fig, ax = plt.subplots(figsize=(8, 5))
differences = np.random.normal(0, 0.045, 1000)  # SE ≈ 0.045
ax.hist(differences, bins=25, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax.axvline(-0.416, color='red', linestyle='--', linewidth=2, alpha=0.7)
ax.set_title('1,000 randomized differences', fontsize=12, fontweight='bold')
ax.set_xlabel('Difference in randomized proportions\n(malaria - control)', fontsize=10)
ax.set_ylabel('Count', fontsize=10)
ax.set_xlim(-0.15, 0.15)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-02.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 3: Asian American tobacco use - bootstrap distribution
print("3. Asian American tobacco use (confidence interval)...")
# Data: Filipino (n=4912, smokers=609), Chinese (n=4736, smokers=279)
# Observed difference: 609/4912 - 279/4736 = 0.124 - 0.059 = 0.065
fig, ax = plt.subplots(figsize=(8, 4))
differences = np.random.normal(0.065, 0.006, 1000)  # Centered at observed difference
ax.hist(differences, bins=30, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax.set_title('1,000 bootstrapped differences', fontsize=12, fontweight='bold')
ax.set_xlabel('Difference in bootstrapped proportions (Filipino - Chinese)', fontsize=10)
ax.set_ylabel('Count', fontsize=10)
ax.set_xlim(0.04, 0.09)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-03.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 4: Malaria vaccine - bootstrap distribution
print("4. Malaria vaccine (confidence interval)...")
# Observed difference: 89/292 - 106/147 = -0.416
fig, ax = plt.subplots(figsize=(8, 4))
differences = np.random.normal(-0.416, 0.048, 1000)  # Centered at observed difference
ax.hist(differences, bins=25, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax.set_title('1,000 bootstrapped differences', fontsize=12, fontweight='bold')
ax.set_xlabel('Difference in bootstrapped proportions (malaria - control)', fontsize=10)
ax.set_ylabel('Count', fontsize=10)
ax.set_xlim(-0.56, -0.27)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-04.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 5: COVID-19 and degree completion - two histograms
print("5. COVID-19 and degree completion (two methods)...")
# Data: BA (n=3941, impact=2010, 51%), AA (n=2064, impact=908, 44%)
# Observed difference: 0.51 - 0.44 = 0.07
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Method A: Bootstrap (centered at observed difference)
differences_A = np.random.normal(0.07, 0.015, 1000)
ax1.hist(differences_A, bins=20, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax1.set_title('Computational method A', fontsize=12, fontweight='bold')
ax1.set_xlabel('Difference in simulated proportions\n(BA - AA)', fontsize=10)
ax1.set_ylabel('Count', fontsize=10)
ax1.set_xlim(0.01, 0.13)

# Method B: Permutation (centered at 0)
differences_B = np.random.normal(0, 0.015, 1000)
ax2.hist(differences_B, bins=20, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax2.set_title('Computational method B', fontsize=12, fontweight='bold')
ax2.set_xlabel('Difference in simulated proportions\n(BA - AA)', fontsize=10)
ax2.set_ylabel('Count', fontsize=10)
ax2.set_xlim(-0.06, 0.06)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-05.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 6: Renewable energy - two histograms
print("6. Renewable energy (two methods)...")
# Data: Republican (n=5447, yes=1689, 31%), Democrat (n=7962, yes=6449, 81%)
# Observed difference: 0.31 - 0.81 = -0.50
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Method A: Permutation (centered at 0)
differences_A = np.random.normal(0, 0.009, 1000)
ax1.hist(differences_A, bins=20, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax1.set_title('Computational Method A', fontsize=12, fontweight='bold')
ax1.set_xlabel('Difference in simulated proportions\n(Republican - Democrat)', fontsize=10)
ax1.set_ylabel('Count', fontsize=10)
ax1.set_xlim(-0.04, 0.04)

# Method B: Bootstrap (centered at observed difference)
differences_B = np.random.normal(-0.50, 0.009, 1000)
ax2.hist(differences_B, bins=20, color=IMSCOL_GREEN, edgecolor='white', linewidth=0.5)
ax2.set_title('Computational Method B', fontsize=12, fontweight='bold')
ax2.set_xlabel('Difference in simulated proportions\n(Republican - Democrat)', fontsize=10)
ax2.set_ylabel('Count', fontsize=10)
ax2.set_xlim(-0.54, -0.46)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-06.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 13: Yawning experiment - stacked bar chart
print("13. Is yawning contagious (bar chart)...")
# Data: Treatment (n=34, yawned=10), Control (n=16, yawned=4)
fig, ax = plt.subplots(figsize=(8, 4))

groups = ['Control', 'Treatment']
yawned = [4, 10]
not_yawned = [12, 24]

# Create stacked horizontal bar chart
bar_width = 0.6
y_pos = np.arange(len(groups))

# Plot bars
p1 = ax.barh(y_pos, not_yawned, bar_width, label='not yawn', color='#569BBD')
p2 = ax.barh(y_pos, yawned, bar_width, left=not_yawned, label='yawn', color='#E8927C')

ax.set_xlabel('Count', fontsize=11)
ax.set_ylabel('Group', fontsize=11)
ax.set_yticks(y_pos)
ax.set_yticklabels(groups)
ax.set_xlim(0, 35)
ax.set_xticks(range(0, 36, 5))
ax.legend(title='Outcome', loc='center right', frameon=True, facecolor='white', edgecolor='white')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-13.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 14: Heart transplant - stacked bar chart
print("14. Heart transplant success (bar chart)...")
# Data from openintro heart_transplant dataset
# Control: alive=4, deceased=30; Treatment: alive=24, deceased=45
fig, ax = plt.subplots(figsize=(8, 4))

groups = ['control', 'treatment']
alive = [4, 24]
deceased = [30, 45]

# Create stacked horizontal bar chart
bar_width = 0.6
y_pos = np.arange(len(groups))

# Plot bars (deceased first, then alive on top)
p1 = ax.barh(y_pos, deceased, bar_width, label='deceased', color='#569BBD')
p2 = ax.barh(y_pos, alive, bar_width, left=deceased, label='alive', color='#E8927C')

ax.set_xlabel('Count', fontsize=11)
ax.set_ylabel('Group', fontsize=11)
ax.set_yticks(y_pos)
ax.set_yticklabels(groups)
ax.legend(title='Outcome', loc='center right', frameon=True, facecolor='white', edgecolor='white')
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_17-ex-inference-two-props-14.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n✓ All Chapter 17 exercise figures generated successfully!")
print(f"✓ Figures saved to {output_dir}/")
print("\nGenerated files:")
for i in [1, 2, 3, 4, 5, 6, 13, 14]:
    filename = f"_17-ex-inference-two-props-{i:02d}.png"
    print(f"  - {filename}")
