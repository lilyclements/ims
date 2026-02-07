#!/usr/bin/env python3
"""
Generate figures for Chapter 20 exercises (Inference for Two Independent Means).

This script creates figures and tables for exercises in Chapter 20,
based on the R code in exercises/_20-ex-inference-two-means.qmd.

Generated figure types:
- Histograms of randomized differences in means (for randomization tests)
- Histograms of bootstrapped differences in means (for confidence intervals)
- Summary statistics tables
- Boxplots with summary tables
- Combined figure layouts

Output: source/images/exercises/_20-ex-inference-two-means-{exercise#}.png

Usage: python3 generate_ch20_exercise_figures.py
       ./generate_ch20_exercise_figures.py

Dependencies: matplotlib, numpy, scipy
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
from matplotlib.gridspec import GridSpec

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(47)

# Create output directory
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

print("Generating Chapter 20 exercise figures...")

# Exercise 3: Diamonds, randomization test
print("\n3. Diamonds, randomization test...")
fig, ax = plt.subplots(figsize=(8, 5))
# Generate normal distribution centered at 0 with observed value at -12.7
slopes = np.random.normal(0, 4.5, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.axvline(x=-12.7, color='#F05133', linewidth=2.5, label='Observed difference')
ax.set_xlabel('Difference in randomized means of price per carat\n(0.99 carats - 1 carat)', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 randomized differences in means', fontsize=12, weight='bold')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-03.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 4: Lizards running, randomization test
print("4. Lizards running, randomization test...")
fig, ax = plt.subplots(figsize=(8, 4))
slopes = np.random.normal(0, 0.25, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.axvline(x=0.7, color='#F05133', linewidth=2.5, label='Observed difference')
ax.set_xlabel('Difference in randomized means of running speed\nbetween lizard species (Western fence - Sagebrush)', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 randomized differences in means', fontsize=12, weight='bold')
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-04.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 5: Diamonds, bootstrap interval
print("5. Diamonds, bootstrap interval...")
fig, ax = plt.subplots(figsize=(8, 4))
# Generate distribution centered around -12 (observed difference)
slopes = np.random.normal(-12, 4.64, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Difference in bootstrapped means of price per carat\n(0.99 carats - 1 carat)', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrapped differences in means', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-05.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 6: Lizards running, bootstrap interval
print("6. Lizards running, bootstrap interval...")
fig, ax = plt.subplots(figsize=(8, 4))
slopes = np.random.normal(0.7, 0.2, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Difference in bootstrapped means of running speed\nbetween lizard species (Western fence - Sagebrush)', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrapped differences in means', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-06.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 8: Possible randomized means - Data table
print("8. Possible randomized means - Data table...")
fig, ax = plt.subplots(figsize=(6, 2))
ax.axis('off')
table_data = [
    ['Group', 'Measurement 1', 'Measurement 2', 'Measurement 3'],
    ['A', '1', '15', '5'],
    ['B', '7', '3', '']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.25, 0.25, 0.25])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.5)
# Style header row
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-08.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 9: Diamonds, mathematical test - Table and Boxplot
print("9. Diamonds, mathematical test - Table and Boxplot...")
fig = plt.figure(figsize=(10, 4))
gs = GridSpec(1, 2, width_ratios=[1, 1.2])

# Left: Table
ax1 = fig.add_subplot(gs[0])
ax1.axis('off')
table_data = [
    ['', 'Mean', 'SD', 'n'],
    ['0.99 carats', '$56.86', '$16.39', '23'],
    ['1 carat', '$69.55', '$13.59', '23']
]
table = ax1.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.35, 0.22, 0.22, 0.21])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')

# Right: Boxplot
ax2 = fig.add_subplot(gs[1])
np.random.seed(47)
data_099 = np.random.normal(56.86, 16.39, 23)
data_1 = np.random.normal(69.55, 13.59, 23)
bp = ax2.boxplot([data_1, data_099], labels=['1 carat', '0.99 carats'], 
                  vert=False, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#569BBD')
    patch.set_alpha(0.7)
ax2.set_xlabel('Price per carat (USD)', fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-09.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 11: Diamonds, mathematical interval - Table only
print("11. Diamonds, mathematical interval - Table...")
fig, ax = plt.subplots(figsize=(5, 2.5))
ax.axis('off')
table_data = [
    ['', 'Mean', 'SD', 'n'],
    ['0.99 carats', '$56.86', '$16.39', '23'],
    ['1 carat', '$69.55', '$13.59', '23']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.25, 0.25, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-11.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 13: Difference of means - Table
print("13. Difference of means - Table...")
fig, ax = plt.subplots(figsize=(6, 2.5))
ax.axis('off')
table_data = [
    ['', 'Mean', 'Standard deviation', 'Sample size'],
    ['Population 1', '15', '20', '50'],
    ['Population 2', '20', '10', '30']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.28, 0.24, 0.28, 0.20])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-13.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 15: Chicken diet - Table, Boxplot, and Histograms
print("15. Chicken diet: horsebean vs. linseed...")
fig = plt.figure(figsize=(12, 4))
gs = GridSpec(1, 3, width_ratios=[1, 1.2, 1.5])

# Left: Table
ax1 = fig.add_subplot(gs[0])
ax1.axis('off')
table_data = [
    ['Statistic', 'Horsebean', 'Linseed'],
    ['Mean', '160.20', '218.75'],
    ['SD', '38.63', '52.24'],
    ['n', '10', '12']
]
table = ax1.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.35, 0.32, 0.33])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)
for i in range(3):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')

# Middle: Boxplot
ax2 = fig.add_subplot(gs[1])
np.random.seed(47)
data_horsebean = np.random.normal(160.20, 38.63, 10)
data_linseed = np.random.normal(218.75, 52.24, 12)
bp = ax2.boxplot([data_linseed, data_horsebean], labels=['linseed', 'horsebean'], 
                  vert=False, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#569BBD')
    patch.set_alpha(0.7)
ax2.set_xlabel('Weight (in grams)', fontsize=10)
ax2.set_ylabel('Feed type', fontsize=10)
ax2.grid(True, alpha=0.3)

# Right: Histograms
ax3 = fig.add_subplot(gs[2])
# Create two subplots stacked vertically
ax3_top = plt.subplot2grid((2, 3), (0, 2), fig=fig)
ax3_bottom = plt.subplot2grid((2, 3), (1, 2), fig=fig)

ax3_top.hist(data_horsebean, bins=8, color='#569BBD', edgecolor='black', alpha=0.7)
ax3_top.set_ylabel('Count', fontsize=9)
ax3_top.set_title('horsebean', fontsize=9)
ax3_top.grid(True, alpha=0.3)

ax3_bottom.hist(data_linseed, bins=8, color='#569BBD', edgecolor='black', alpha=0.7)
ax3_bottom.set_xlabel('Weight (in grams)', fontsize=9)
ax3_bottom.set_ylabel('Count', fontsize=9)
ax3_bottom.set_title('linseed', fontsize=9)
ax3_bottom.grid(True, alpha=0.3)

ax3.remove()  # Remove the placeholder axis

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-15.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 16: Fuel efficiency in the city - Table and Boxplot
print("16. Fuel efficiency in the city - Table and Boxplot...")
fig = plt.figure(figsize=(10, 4))
gs = GridSpec(1, 2, width_ratios=[1, 1.2])

# Left: Table
ax1 = fig.add_subplot(gs[0])
ax1.axis('off')
table_data = [
    ['CITY', 'Mean', 'SD', 'n'],
    ['Automatic', '18.88', '4.58', '25'],
    ['Manual', '21.28', '5.24', '25']
]
table = ax1.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.32, 0.23, 0.23, 0.22])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')

# Right: Boxplot
ax2 = fig.add_subplot(gs[1])
np.random.seed(1234)
data_automatic = np.random.normal(18.88, 4.58, 25)
data_manual = np.random.normal(21.28, 5.24, 25)
bp = ax2.boxplot([data_manual, data_automatic], labels=['Manual', 'Automatic'], 
                  vert=False, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#569BBD')
    patch.set_alpha(0.7)
ax2.set_xlabel('City mileage (MPG)', fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-16.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 17: Chicken diet: casein vs. soybean - Table only
print("17. Chicken diet: casein vs. soybean - Table...")
fig, ax = plt.subplots(figsize=(5, 2.5))
ax.axis('off')
table_data = [
    ['Feed type', 'Mean', 'SD', 'n'],
    ['casein', '323.58', '64.43', '12'],
    ['soybean', '246.43', '54.13', '14']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.28, 0.24, 0.24, 0.24])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-17.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 18: Fuel efficiency on the highway - Table and Boxplot
print("18. Fuel efficiency on the highway - Table and Boxplot...")
fig = plt.figure(figsize=(10, 4))
gs = GridSpec(1, 2, width_ratios=[1, 1.2])

# Left: Table
ax1 = fig.add_subplot(gs[0])
ax1.axis('off')
table_data = [
    ['HIGHWAY', 'Mean', 'SD', 'n'],
    ['Automatic', '27.28', '5.65', '25'],
    ['Manual', '30.20', '6.81', '25']
]
table = ax1.table(cellText=table_data, cellLoc='center', loc='center',
                 colWidths=[0.32, 0.23, 0.23, 0.22])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.8)
for i in range(4):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')

# Right: Boxplot
ax2 = fig.add_subplot(gs[1])
np.random.seed(1234)
data_automatic = np.random.normal(27.28, 5.65, 25)
data_manual = np.random.normal(30.20, 6.81, 25)
bp = ax2.boxplot([data_manual, data_automatic], labels=['Manual', 'Automatic'], 
                  vert=False, patch_artist=True)
for patch in bp['boxes']:
    patch.set_facecolor('#569BBD')
    patch.set_alpha(0.7)
ax2.set_xlabel('Highway mileage (MPG)', fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_20-ex-inference-two-means-18.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("SUCCESS! All Chapter 20 exercise figures generated.")
print("="*60)
print(f"\nGenerated files in {output_dir}:")
files = [
    '_20-ex-inference-two-means-03.png',
    '_20-ex-inference-two-means-04.png',
    '_20-ex-inference-two-means-05.png',
    '_20-ex-inference-two-means-06.png',
    '_20-ex-inference-two-means-08.png',
    '_20-ex-inference-two-means-09.png',
    '_20-ex-inference-two-means-11.png',
    '_20-ex-inference-two-means-13.png',
    '_20-ex-inference-two-means-15.png',
    '_20-ex-inference-two-means-16.png',
    '_20-ex-inference-two-means-17.png',
    '_20-ex-inference-two-means-18.png',
]
for f in files:
    print(f"  - {f}")
print()
