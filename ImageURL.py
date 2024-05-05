import csv

# Function to fill empty lines in the text file with the content of the previous non-empty line
def fill_empty_lines(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        previous_line = ''
        for line in infile:
            if line.strip():  # If the line is not empty
                previous_line = line.strip()
                outfile.write(line)
            else:  # If the line is empty
                outfile.write(previous_line + '\n')

# Function to convert the filled .txt file to a .csv file with ID and Image URL columns
def txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as infile, open(csv_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        for idx, line in enumerate(infile, start=1):
            urls = line.strip().split(',')
            writer.writerow([idx, ' '.join(urls).strip()])  # Concatenate all URLs on the line into one cell

# Input and output file paths
input_txt_file = 'image_urls.txt'
filled_txt_file = 'filled_input.txt'
output_csv_file = 'output.csv'

# Fill empty lines in the text file
fill_empty_lines(input_txt_file, filled_txt_file)

# Convert filled .txt file to .csv with ID and Image URL columns
txt_to_csv(filled_txt_file, output_csv_file)

print("Conversion completed successfully!")
