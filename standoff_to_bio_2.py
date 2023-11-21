# ADD BIO TAGS

import csv
import os

def process_file(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        previous_tag = None
        for row in reader:
            if len(row) != 2:
                continue  # Skip empty lines or lines with incorrect format

            word, tag = row
            if tag in ['Claim', 'Majorclaim','Premise']:
                if tag != previous_tag:
                    # First occurrence: use 'B-' prefix
                    new_tag = f'B-{tag}'
                else:
                    # Subsequent occurrence: use 'I-' prefix
                    new_tag = f'I-{tag}'
                writer.writerow([word, new_tag])
                previous_tag = tag
            else:
                writer.writerow([word, tag])
                previous_tag = None

input_dir = 'output_bio1/'
# create output directory if not exists
output_dir = 'output_bio2/'

if not os.path.exists('output_bio2'):
    os.makedirs('output_bio2')

for file in os.listdir(input_dir):
    if file.endswith(".tsv"):
        print(file)
        # Modify these file paths as needed
        input_csv = input_dir + file  # Path to your input CSV file
        output_csv = output_dir+file  # Path to the output CSV file
        process_file(input_csv, output_csv)
