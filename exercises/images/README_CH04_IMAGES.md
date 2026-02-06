# Chapter 4 Exercise Images

This directory contains images for Chapter 4 exercises. Some images need to be downloaded from external sources.

## Required Images

The following images are required for Chapter 4 exercises:

### Q1 - Antibiotic Use in Children
- **File**: `04-ex-q1-antibiotic-conditions.png`
- **Source**: https://github.com/user-attachments/assets/c7d22aad-bb23-4c90-b26d-4c50c81c00e6
- **Description**: Bar plot and pie chart showing the distribution of medical conditions (Prematurity, Cardiovascular, Respiratory, Neuromuscular, Trauma, Genetic/metabolic, Gastrointestinal, and Immunocompromised)

### Q3 - George Floyd Protests
- **File**: `04-ex-q3-george-floyd-protests.png`
- **Source**: https://github.com/user-attachments/assets/40efecfa-6d65-4d50-9989-1086df91dc42
- **Description**: Stacked bar plot showing support for protests following George Floyd's killing by age group (18-29, 30-39, 40-49, 50-64, 65+)

### Q7 - Meat Consumption and Life Expectancy
- **File**: `04-ex-q7-meat-life-expectancy.png`
- **Source**: https://github.com/user-attachments/assets/cd16fad0-5190-4c28-aa96-f4f62c7049ae
- **Description**: Two ridge plots showing meat consumption (kg per capita) and life expectancy (years) by income level (Low/Middle/High income)

## How to Download

### Option 1: Using the Python script
Run the provided download script:
```bash
python3 download_ch04_images.py
```

### Option 2: Manual download
1. Open each URL in a web browser
2. Right-click on the image and select "Save image as..."
3. Save the image with the corresponding filename in this directory

### Option 3: Using curl
```bash
cd exercises/images
curl -L -o "04-ex-q1-antibiotic-conditions.png" "https://github.com/user-attachments/assets/c7d22aad-bb23-4c90-b26d-4c50c81c00e6"
curl -L -o "04-ex-q3-george-floyd-protests.png" "https://github.com/user-attachments/assets/40efecfa-6d65-4d50-9989-1086df91dc42"
curl -L -o "04-ex-q7-meat-life-expectancy.png" "https://github.com/user-attachments/assets/cd16fad0-5190-4c28-aa96-f4f62c7049ae"
```
