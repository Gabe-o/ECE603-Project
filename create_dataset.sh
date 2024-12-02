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

# Verify the ZIP file
echo "Verifying the combined zip file..."
if unzip -t secmatv1_2006_04_0809.zip; then
    echo "Verification successful!"
else
    echo "Verification failed. Check the downloaded parts."
    exit 1
fi

# Extract the dataset
echo "Extracting the dataset..."
unzip secmatv1_2006_04_0809.zip -d secmatv1_2006_04_0809

# Convert to CSV
mkdir -p secmatv1_csv
total_files=$(find secmatv1_2006_04_0809 -name "*.bin" | wc -l)
processed=0

find secmatv1_2006_04_0809 -name "*.bin" | while read bin_file; do
    csv_file="secmatv1_csv/$(basename "${bin_file}" .bin).csv"
    ./bin_to_csv "$bin_file" "$csv_file"
    processed=$((processed + 1))
    echo "Processed $processed/$total_files files"
done

# Cleanup temporary files
echo "Cleaning up temporary files..."
rm -f secmatv1_2006_04_0809.zip.part*
rm -f secmatv1_2006_04_0809.zip
rm -rf secmatv1_2006_04_0809

echo "All temporary files removed. Final CSV dataset is in 'secmatv1_csv'."
