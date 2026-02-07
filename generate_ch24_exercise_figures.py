#!/usr/bin/env python3
"""
Generate figures for Chapter 24 exercises (Inference for Simple Linear Regression).

This script creates 28 representative figures for 20 exercises in Chapter 24,
based on the R code in exercises/_24-ex-inf-model-slr.qmd.

Generated figure types:
- Regression output tables (coefficient estimates, std. errors, t-values, p-values)
- Histograms of randomized slopes (for randomization tests)
- Histograms of bootstrapped slopes (for confidence intervals)
- Scatterplots with regression lines
- Residual plots (residuals vs fitted values or predictor values)

Output: source/images/exercises/_24-ex-inf-model-slr-{exercise#}-{fig#}.png

Usage: python3 generate_ch24_exercise_figures.py
       ./generate_ch24_exercise_figures.py

Dependencies: matplotlib, numpy, scipy
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as mpatches

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
np.random.seed(47)

# Create output directory
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

print("Generating Chapter 24 exercise figures...")

# Exercise 1: Body measurements, randomization test
# Figure 0: Regression table (simulated as an image with text)
# Figure 1: Histogram of randomized slopes
print("\n1. Body measurements, randomization test...")

# Figure 1-0: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '105.832', '3.523', '30.04', '<0.0001'],
    ['sho_gi', '0.604', '0.033', '18.44', '<0.0001']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.2, 0.2, 0.15, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
# Style header row
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: hgt ~ sho_gi', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-1-0.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 1-1: Histogram of randomized slopes
fig, ax = plt.subplots(figsize=(7, 4))
slopes = np.random.normal(0, 0.04, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.axvline(x=0.604, color='red', linewidth=2, label='Observed slope')
ax.set_xlabel('Slope from randomly permuted data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 randomized slopes', fontsize=12, weight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-1-1.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 2: Baby's weight and father's age, randomization test
print("2. Baby's weight and father's age, randomization test...")

# Figure 2-2: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '7.162', '0.172', '41.59', '<0.0001'],
    ['fage', '0.005', '0.005', '0.98', '0.3253']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.2, 0.2, 0.15, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: weight ~ fage', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-2-2.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 2-3: Histogram of randomized slopes
fig, ax = plt.subplots(figsize=(7, 4))
slopes = np.random.normal(0, 0.005, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.axvline(x=0.005, color='red', linewidth=2, label='Observed slope')
ax.set_xlabel('Slope from randomly permuted data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 randomized slopes', fontsize=12, weight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-2-3.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 3: Body measurements, mathematical test
print("3. Body measurements, mathematical test...")

# Figure 3-4: Scatterplot (weight vs height)
fig, ax = plt.subplots(figsize=(6, 5))
height = np.random.normal(171, 9.4, 507)
weight = -105 + 1.02 * height + np.random.normal(0, 8, 507)
ax.scatter(height, weight, alpha=0.4, s=15)
ax.set_xlabel('Height (cm)', fontsize=11)
ax.set_ylabel('Weight (kg)', fontsize=11)
ax.set_xlim(145, 200)
ax.set_ylim(40, 120)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-3-4.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 3-5: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '-105.01', '7.54', '-13.93', '<0.0001'],
    ['hgt', '1.02', '0.04', '23.42', '<0.0001']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.2, 0.2, 0.15, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: wgt ~ hgt', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-3-5.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 4: Baby's weight and father's age, mathematical test
print("4. Baby's weight and father's age, mathematical test...")

# Figure 4-6: Scatterplot (baby weight vs father age)
fig, ax = plt.subplots(figsize=(6, 5))
fage = np.random.uniform(15, 55, 1000)
weight = 7.2 + 0.005 * fage + np.random.normal(0, 1.5, 1000)
ax.scatter(fage, weight, alpha=0.3, s=10)
ax.set_xlabel("Father's age", fontsize=11)
ax.set_ylabel('Weight (lbs)', fontsize=11)
ax.set_xlim(10, 60)
ax.set_ylim(2, 13)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-4-6.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 4-7: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '7.1622', '0.1721', '41.59', '<0.0001'],
    ['fage', '0.0050', '0.0051', '0.98', '0.3253']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.25, 0.2, 0.2, 0.15, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: weight ~ fage', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-4-7.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 5: Body measurements, bootstrap percentile interval
print("5. Body measurements, bootstrap percentile interval...")

# Figure 5-8: Histogram of bootstrap slopes
fig, ax = plt.subplots(figsize=(10, 4))
slopes = np.random.normal(0.604, 0.01, 1000)
ax.hist(slopes, bins=40, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Slope from bootstrapped data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrap slopes', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-5-8.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 6: Baby's weight and father's age, bootstrap percentile interval
print("6. Baby's weight and father's age, bootstrap percentile interval...")

# Figure 6-9: Histogram of bootstrap slopes
fig, ax = plt.subplots(figsize=(10, 4))
slopes = np.random.normal(0.005, 0.005, 1000)
ax.hist(slopes, bins=40, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Slope from bootstrapped data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrapped slopes', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-6-9.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 7: Body measurements, standard error bootstrap interval
print("7. Body measurements, standard error bootstrap interval...")

# Figure 7-10: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '105.832', '3.523', '30.04', '<0.0001'],
    ['sho_gi', '0.604', '0.033', '18.44', '<0.0001']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: hgt ~ sho_gi', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-7-10.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 7-11: Histogram of bootstrap slopes
fig, ax = plt.subplots(figsize=(7, 4))
slopes = np.random.normal(0.604, 0.01, 1000)
ax.hist(slopes, bins=40, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Slope from bootstrapped data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrapped slopes', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-7-11.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 8: Baby's weight and father's age, standard error bootstrap interval
print("8. Baby's weight and father's age, standard error bootstrap interval...")

# Figure 8-12: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '7.162', '0.172', '41.59', '<0.0001'],
    ['fage', '0.005', '0.005', '0.98', '0.3253']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: weight ~ fage', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-8-12.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 8-13: Histogram of bootstrap slopes
fig, ax = plt.subplots(figsize=(7, 4))
slopes = np.random.normal(0.005, 0.005, 1000)
ax.hist(slopes, bins=40, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Slope from bootstrapped data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrapped slopes', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-8-13.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 9: Body measurements, conditions (residual plot)
print("9. Body measurements, conditions...")

# Figure 9-14: Residual plot
fig, ax = plt.subplots(figsize=(7, 5))
fitted = np.random.uniform(50, 100, 507)
residuals = np.random.normal(0, 8, 507)
ax.scatter(fitted, residuals, alpha=0.4, s=15)
ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax.set_xlabel('Fitted values', fontsize=11)
ax.set_ylabel('Residuals', fontsize=11)
ax.set_title('Residuals vs Fitted Values', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-9-14.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 10: Baby's weight and father's age, conditions (residual plot)
print("10. Baby's weight and father's age, conditions...")

# Figure 10-15: Residual plot
fig, ax = plt.subplots(figsize=(7, 5))
fitted = np.random.uniform(5, 10, 1000)
residuals = np.random.normal(0, 1.5, 1000)
ax.scatter(fitted, residuals, alpha=0.3, s=10)
ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax.set_xlabel('Fitted values', fontsize=11)
ax.set_ylabel('Residuals', fontsize=11)
ax.set_title('Residuals vs Fitted Values', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-10-15.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 11: Murders and poverty, randomization test
print("11. Murders and poverty, randomization test...")

# Figure 11-16: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '-29.901', '14.789', '-2.02', '0.0583'],
    ['perc_pov', '2.559', '0.905', '2.83', '0.0109']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: annual_murders_per_mil ~ perc_pov', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-11-16.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 11-17: Histogram of randomized slopes
fig, ax = plt.subplots(figsize=(7, 4))
slopes = np.random.normal(0, 0.9, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.axvline(x=2.559, color='red', linewidth=2, label='Observed slope')
ax.set_xlabel('Slope from randomly permuted data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 randomized slopes', fontsize=12, weight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-11-17.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 12: Murders and poverty, mathematical test
print("12. Murders and poverty, mathematical test...")

# Figure 12-18: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '-29.9011', '14.7891', '-2.02', '0.0583'],
    ['perc_pov', '2.5593', '0.9050', '2.83', '0.0109']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: annual_murders_per_mil ~ perc_pov', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-12-18.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 13: Murders and poverty, bootstrap percentile interval
print("13. Murders and poverty, bootstrap percentile interval...")

# Figure 13-19: Histogram of bootstrap slopes
fig, ax = plt.subplots(figsize=(10, 4))
slopes = np.random.normal(2.56, 0.9, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Slope from bootstrapped data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrap slopes', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-13-19.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 14: Murders and poverty, standard error bootstrap interval
print("14. Murders and poverty, standard error bootstrap interval...")

# Figure 14-20: Regression table
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '-29.901', '14.789', '-2.02', '0.0583'],
    ['perc_pov', '2.559', '0.905', '2.83', '0.0109']
]
table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')
plt.title('Linear Model: annual_murders_per_mil ~ perc_pov', pad=20, fontsize=12, weight='bold')
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-14-20.png'), dpi=150, bbox_inches='tight')
plt.close()

# Figure 14-21: Histogram of bootstrap slopes
fig, ax = plt.subplots(figsize=(7, 4))
slopes = np.random.normal(2.56, 0.9, 1000)
ax.hist(slopes, bins=30, color='#569BBD', edgecolor='black', alpha=0.7)
ax.set_xlabel('Slope from bootstrapped data', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('1,000 bootstrapped slopes', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-14-21.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 15: Murders and poverty, conditions
print("15. Murders and poverty, conditions...")

# Figure 15-22: Scatterplot with regression line and residual plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Scatterplot with regression line
perc_pov = np.random.uniform(10, 25, 20)
murders = -29.9 + 2.56 * perc_pov + np.random.normal(0, 15, 20)
ax1.scatter(perc_pov, murders, alpha=0.6, s=50)
# Add regression line
z = np.polyfit(perc_pov, murders, 1)
p = np.poly1d(z)
x_line = np.linspace(perc_pov.min(), perc_pov.max(), 100)
ax1.plot(x_line, p(x_line), 'gray', linewidth=2)
ax1.set_xlabel('Percentage living in poverty', fontsize=11)
ax1.set_ylabel('Annual murders per million', fontsize=11)
ax1.set_title('Annual Murders vs Poverty Percentage', fontsize=12, weight='bold')

# Right plot: Residual plot
fitted = -29.9 + 2.56 * perc_pov
residuals = murders - fitted
ax2.scatter(perc_pov, residuals, alpha=0.6, s=50)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.set_xlabel('Percentage living in poverty', fontsize=11)
ax2.set_ylabel('Residuals', fontsize=11)
ax2.set_title('Residual Plot', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-15-22.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 16: I heart cats
print("16. I heart cats...")

# Figure 16-23: Scatterplot (heart weight vs body weight) with regression table
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Scatterplot
body_weight = np.random.uniform(2, 4, 144)
heart_weight = -0.357 + 4.034 * body_weight + np.random.normal(0, 1.5, 144)
ax1.scatter(body_weight, heart_weight, alpha=0.5, s=25)
# Add regression line
z = np.polyfit(body_weight, heart_weight, 1)
p = np.poly1d(z)
x_line = np.linspace(body_weight.min(), body_weight.max(), 100)
ax1.plot(x_line, p(x_line), 'gray', linewidth=2)
ax1.set_xlabel('Body weight (kg)', fontsize=11)
ax1.set_ylabel('Heart weight (g)', fontsize=11)
ax1.set_title('Cat Heart Weight vs Body Weight', fontsize=12, weight='bold')

# Right plot: Regression table
ax2.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '-0.357', '0.692', '-0.515', '0.6072'],
    ['Bwt', '4.034', '0.250', '16.119', '<0.0001']
]
table = ax2.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-16-23.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 17: Beer and blood alcohol content
print("17. Beer and blood alcohol content...")

# Figure 17-24: Scatterplot (BAC vs beers) with regression table
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Scatterplot
beers = np.random.randint(1, 10, 16)
bac = -0.0127 + 0.0180 * beers + np.random.normal(0, 0.015, 16)
bac = np.clip(bac, 0, None)
ax1.scatter(beers, bac, alpha=0.6, s=50)
# Add regression line
z = np.polyfit(beers, bac, 1)
p = np.poly1d(z)
x_line = np.linspace(beers.min(), beers.max(), 100)
ax1.plot(x_line, p(x_line), 'gray', linewidth=2)
ax1.set_xlabel('Number of cans of beer', fontsize=11)
ax1.set_ylabel('Blood Alcohol Content (BAC)', fontsize=11)
ax1.set_title('BAC vs Number of Beers', fontsize=12, weight='bold')

# Right plot: Regression table
ax2.axis('off')
table_data = [
    ['term', 'estimate', 'std.error', 't.value', 'p.value'],
    ['(Intercept)', '-0.0127', '0.0126', '-1.00', '0.332'],
    ['beers', '0.0180', '0.0024', '7.48', '<0.0001']
]
table = ax2.table(cellText=table_data, cellLoc='center', loc='center',
                colWidths=[0.3, 0.2, 0.2, 0.15, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
for i in range(5):
    table[(0, i)].set_facecolor('#E0E0E0')
    table[(0, i)].set_text_props(weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-17-24.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 18: Urban homeowners, conditions
print("18. Urban homeowners, conditions...")

# Figure 18-25: Scatterplot and residual plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Scatterplot with regression line
urban = np.random.uniform(30, 100, 50)
homeowners = 75 - 0.3 * urban + np.random.normal(0, 5, 50)
# Add DC as outlier
urban_dc = 100
homeowners_dc = 42
ax1.scatter(urban, homeowners, alpha=0.5, s=30, label='States')
ax1.scatter(urban_dc, homeowners_dc, color='blue', s=100, alpha=0.7, label='DC', marker='s')
# Add regression line (including DC)
all_urban = np.append(urban, urban_dc)
all_homeowners = np.append(homeowners, homeowners_dc)
z = np.polyfit(all_urban, all_homeowners, 1)
p = np.poly1d(z)
x_line = np.linspace(all_urban.min(), all_urban.max(), 100)
ax1.plot(x_line, p(x_line), 'gray', linewidth=2)
ax1.set_xlabel('% Urban population', fontsize=11)
ax1.set_ylabel('% Who own home', fontsize=11)
ax1.set_title('Homeownership vs Urban Population', fontsize=12, weight='bold')
ax1.legend()

# Right plot: Residual plot
fitted = p(all_urban)
residuals = all_homeowners - fitted
ax2.scatter(all_urban, residuals, alpha=0.5, s=30)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.set_xlabel('% Urban population', fontsize=11)
ax2.set_ylabel('Residuals', fontsize=11)
ax2.set_title('Residual Plot', fontsize=12, weight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-18-25.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 19: I heart cats, LINE conditions
print("19. I heart cats, LINE conditions...")

# Figure 19-26: Residual plot showing heteroscedasticity
fig, ax = plt.subplots(figsize=(7, 5))

# Generate data with increasing variance (heteroscedasticity)
body_weight = np.random.uniform(2, 4, 144)
heart_weight = -0.357 + 4.034 * body_weight + np.random.normal(0, 1.5, 144)
fitted = -0.357 + 4.034 * body_weight
# Create residuals with heteroscedasticity (variance increases with fitted values)
residuals = (heart_weight - fitted) * (0.3 + 0.7 * (fitted - fitted.min()) / (fitted.max() - fitted.min()))
ax.scatter(fitted, residuals, alpha=0.5, s=20)
ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax.set_xlabel('Predicted values', fontsize=11)
ax.set_ylabel('Residuals', fontsize=11)
ax.set_title('Residuals vs Predicted Values', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-19-26.png'), dpi=150, bbox_inches='tight')
plt.close()

# Exercise 20: Beer and blood alcohol content, LINE conditions
print("20. Beer and blood alcohol content, LINE conditions...")

# Figure 20-27: Residual plot
fig, ax = plt.subplots(figsize=(7, 5))

beers = np.random.randint(1, 10, 16)
bac = -0.0127 + 0.0180 * beers + np.random.normal(0, 0.015, 16)
fitted = -0.0127 + 0.0180 * beers
residuals = bac - fitted
ax.scatter(fitted, residuals, alpha=0.6, s=40)
ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax.set_xlabel('Predicted values', fontsize=11)
ax.set_ylabel('Residuals', fontsize=11)
ax.set_title('Residuals vs Predicted Values', fontsize=12, weight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_24-ex-inf-model-slr-20-27.png'), dpi=150, bbox_inches='tight')
plt.close()

print("\n✓ All exercise figures generated successfully!")
print(f"✓ Figures saved to {output_dir}/")
print(f"✓ Generated 28 figures (0-27) for 20 exercises")
