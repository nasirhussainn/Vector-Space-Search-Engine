import csv
import calendar

def convert_month_to_number(month):
    return list(calendar.month_abbr).index(month[:3])

def load_inverted_index(file_path):
    inverted_index = {}
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            keyword = row[0]
            frequency = int(row[1])
            posting_list = [int(doc_id) if doc_id.isdigit() else convert_month_to_number(doc_id) for doc_id in row[2].split('-')]
            inverted_index[keyword] = {'frequency': frequency, 'posting_list': posting_list}
    return inverted_index
def load_meta_file(filename):
    meta_data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['ID'].strip():  # Check if ID field is not empty
                doc_id = int(row['ID'])
                meta_data[doc_id] = {
                    'URI': row['URI'],
                    'Title': row['Title'],
                    'Description': row['Description'],
                    'Keywords': row['Keywords'],
                    'Images': row.get('Images', '')
                }
    return meta_data

