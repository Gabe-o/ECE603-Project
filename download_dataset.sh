#!/bin/bash

# Base URL for the dataset parts
BASE_URL="https://cloud.telecom-paris.fr/s/8KWK5PnApP4DNy7/download?path=%2F&files="

# Dataset part filenames
PARTS=(
    "secmatv1_2006_04_0809.zip.part0"
    "secmatv1_2006_04_0809.zip.part1"
    "secmatv1_2006_04_0809.zip.part2"
    "secmatv1_2006_04_0809.zip.part3"
)

# Download each part
echo "Downloading dataset parts..."
for PART in "${PARTS[@]}"; do
    echo "Downloading $PART..."
    wget -O "$PART" "${BASE_URL}${PART}"
done

# Combine parts into a single ZIP file
echo "Combining parts into a single zip file..."
cat secmatv1_2006_04_0809.zip.part* > secmatv1_2006_04_0809.zip

# Extract the dataset
echo "Extracting the dataset..."
unzip secmatv1_2006_04_0809.zip

echo "Dataset is in 'secmatv1_2006_04_0809'."
