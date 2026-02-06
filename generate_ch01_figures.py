#!/usr/bin/env python3
"""
Generate placeholder figures for Chapter 1 exercises.
Since we don't have access to the actual R datasets, we'll create representative
placeholder images based on the exercise descriptions.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')

# Create output directory if it doesn't exist
output_dir = "source/images/exercises"
os.makedirs(output_dir, exist_ok=True)

# Exercise 13: US Airports map
print("Generating figure for Exercise 13: US Airports...")
fig, ax = plt.subplots(figsize=(12, 6))
# Simulate US map outline
us_x = [0, 0, 10, 10, 0]
us_y = [0, 5, 5, 0, 0]
ax.plot(us_x, us_y, 'k-', linewidth=2)
ax.fill(us_x, us_y, color='lightgray', alpha=0.3)

# Simulate airport points in different regions
np.random.seed(42)
regions = {
    'Eastern': ([1, 3], [1, 4], 'red'),
    'Central': ([3, 5], [1, 4], 'blue'),
    'Western': ([7, 9], [1, 4], 'green'),
    'Southern': ([2, 8], [0.5, 2], 'orange')
}

for region, (x_range, y_range, color) in regions.items():
    n_points = np.random.randint(80, 150)
    x = np.random.uniform(x_range[0], x_range[1], n_points)
    y = np.random.uniform(y_range[0], y_range[1], n_points)
    ax.scatter(x, y, alpha=0.4, s=10, c=color, label=region)

ax.set_xlim(-0.5, 10.5)
ax.set_ylim(-0.5, 5.5)
ax.set_title('Geographical Distribution of Airports in the Contiguous United States', fontsize=12)
ax.legend(loc='upper left', fontsize=9)
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_01-ex-us-airports.png'), dpi=150, bbox_inches='tight')
print(f"✓ Saved {os.path.join(output_dir, '_01-ex-us-airports.png')}")
plt.close()

# Exercise 14: UN Votes
print("\nGenerating figure for Exercise 14: UN Votes...")
fig, axes = plt.subplots(2, 3, figsize=(12, 7))
axes = axes.flatten()
issues = ['Arms control', 'Colonialism', 'Economic dev.', 
          'Human rights', 'Nuclear', 'Palestinian conflict']
countries = ['United States', 'Canada', 'Mexico']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

for idx, issue in enumerate(issues):
    ax = axes[idx]
    years = np.linspace(1946, 2019, 50)
    
    for i, country in enumerate(countries):
        # Simulate voting patterns
        if country == 'United States':
            base = 0.5 - 0.1 * idx/6
            trend = 0.0002 * (years - 1946)
        elif country == 'Canada':
            base = 0.55 - 0.05 * idx/6
            trend = 0.0001 * (years - 1946)
        else:  # Mexico
            base = 0.60 - 0.08 * idx/6
            trend = 0.00015 * (years - 1946)
        
        percent_yes = base + trend + np.random.normal(0, 0.05, len(years))
        percent_yes = np.clip(percent_yes, 0, 1)
        
        ax.scatter(years, percent_yes, alpha=0.3, s=15, c=colors[i])
        # Smooth line
        from scipy.ndimage import gaussian_filter1d
        smoothed = gaussian_filter1d(percent_yes, sigma=3)
        ax.plot(years, smoothed, linewidth=2, c=colors[i], label=country if idx == 0 else "")
    
    ax.set_title(issue, fontsize=10)
    ax.set_ylim(-0.05, 1.05)
    ax.set_yticks([0, 0.5, 1])
    ax.set_yticklabels(['0%', '50%', '100%'])
    ax.set_xticks([1960, 1990, 2020])
    ax.grid(True, alpha=0.3)

fig.text(0.5, 0.02, 'Year', ha='center', fontsize=11)
fig.text(0.02, 0.5, '% Yes', va='center', rotation='vertical', fontsize=11)
if len(countries) > 0:
    fig.legend(countries, loc='upper center', ncol=3, fontsize=10, 
               bbox_to_anchor=(0.5, 0.98))
plt.tight_layout(rect=[0.03, 0.03, 1, 0.96])
plt.savefig(os.path.join(output_dir, '_01-ex-un-votes.png'), dpi=150, bbox_inches='tight')
print(f"✓ Saved {os.path.join(output_dir, '_01-ex-un-votes.png')}")
plt.close()

# Exercise 15: UK baby names
print("\nGenerating figure for Exercise 15: UK baby names...")
fig, ax = plt.subplots(figsize=(10, 5))
years = np.arange(2000, 2022)
nations = ['England & Wales', 'Northern Ireland', 'Scotland']
colors_uk = ['#1f77b4', '#ff7f0e', '#2ca02c']
linestyles = ['-', '--', '-.']

for i, nation in enumerate(nations):
    # Simulate trends for name "Fiona"
    if nation == 'England & Wales':
        base = 200 - (years - 2000) * 8
    elif nation == 'Northern Ireland':
        base = 15 - (years - 2000) * 0.5
    else:  # Scotland
        base = 80 - (years - 2000) * 3
    
    n = base + np.random.normal(0, 10, len(years))
    n = np.clip(n, 5, None)
    
    ax.plot(years, n, linewidth=2.5, color=colors_uk[i], 
            linestyle=linestyles[i], label=nation, marker='o', markersize=4)

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('Number of babies named Fiona', fontsize=11)
ax.set_title('Number of Baby Girls Named "Fiona" in the United Kingdom', fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_01-ex-uk-baby-names.png'), dpi=150, bbox_inches='tight')
print(f"✓ Saved {os.path.join(output_dir, '_01-ex-uk-baby-names.png')}")
plt.close()

# Exercise 16: Netflix shows
print("\nGenerating figure for Exercise 16: Netflix shows...")
fig, ax = plt.subplots(figsize=(10, 6))
decades = ['<1990', '1990s', '2000s', '2010s', '2020+']
countries = ['United Kingdom', 'United States', 'Other']
ratings = ['TV-MA', 'TV-14', 'TV-PG', 'TV-Y', 'TV-G']
colors_ratings = plt.cm.Set3(np.linspace(0, 1, len(ratings)))

x = np.arange(len(decades))
width = 0.25

for i, country in enumerate(countries):
    # Create stacked bars for each country
    bottom = np.zeros(len(decades))
    for j, rating in enumerate(ratings):
        # Simulate distribution
        if country == 'United States':
            heights = np.array([5, 20, 40, 60, 25]) * (1 + 0.3 * j/len(ratings))
        elif country == 'United Kingdom':
            heights = np.array([2, 8, 15, 25, 10]) * (1 + 0.2 * j/len(ratings))
        else:  # Other
            heights = np.array([3, 10, 20, 30, 15]) * (1 + 0.25 * j/len(ratings))
        
        heights = heights * np.random.uniform(0.8, 1.2, len(decades))
        
        ax.bar(x + i * width - width, heights, width, bottom=bottom, 
               color=colors_ratings[j], label=rating if i == 0 else "", 
               edgecolor='white', linewidth=0.5)
        bottom += heights

ax.set_xlabel('Decade', fontsize=11)
ax.set_ylabel('Count', fontsize=11)
ax.set_title('Distribution of Netflix TV Show Ratings by Decade and Country', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(decades)
ax.legend(title='Rating', loc='upper left', fontsize=9)

# Add country labels
for i, country in enumerate(countries):
    ax.text(i * width - width + len(decades)/2, -30, country, 
            ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_01-ex-netflix-shows.png'), dpi=150, bbox_inches='tight')
print(f"✓ Saved {os.path.join(output_dir, '_01-ex-netflix-shows.png')}")
plt.close()

# Exercise 19: Pet names
print("\nGenerating figure for Exercise 19: Pet names...")
fig, ax = plt.subplots(figsize=(10, 6))

# Top pet names with counts
names = ['Lucy', 'Charlie', 'Luna', 'Bella', 'Max', 'Daisy', 'Cooper', 'Lily', 
         'Buddy', 'Molly', 'Bailey', 'Sadie', 'Jack', 'Sophie', 'Rocky']
counts = [450, 420, 380, 360, 340, 320, 300, 285, 270, 255, 240, 230, 220, 210, 200]

y_pos = np.arange(len(names))
colors_pets = plt.cm.Paired(np.linspace(0, 1, len(names)))

bars = ax.barh(y_pos, counts, color=colors_pets, edgecolor='gray', linewidth=0.5)
ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.invert_yaxis()
ax.set_xlabel('Number of Pets', fontsize=11)
ax.set_title('Top 15 Pet Names in Seattle', fontsize=12)
ax.grid(axis='x', alpha=0.3)

# Add count labels
for i, (bar, count) in enumerate(zip(bars, counts)):
    ax.text(count + 10, bar.get_y() + bar.get_height()/2, 
            str(count), va='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, '_01-ex-pet-names.png'), dpi=150, bbox_inches='tight')
print(f"✓ Saved {os.path.join(output_dir, '_01-ex-pet-names.png')}")
plt.close()

print("\n✓ All 5 exercise figures generated successfully!")
print(f"\nFiles created in {output_dir}:")
for f in sorted(os.listdir(output_dir)):
    if f.startswith('_01-ex'):
        size = os.path.getsize(os.path.join(output_dir, f)) / 1024
        print(f"  - {f} ({size:.1f} KB)")
