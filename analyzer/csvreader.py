import csv
import helper

def read(filename, indices):
    """
    Reads a CSV file and returns a list of tuples (Each tuple represents a row
    in the CSV file).
    """
    if not filename or not indices:
        raise ValueError("Invalid input arguments")

    rows = []
    with open(filename, 'rb') as csv_file:
        file_reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for row in file_reader:
            row_data = _parse_row(row)
            if row_data:
                rows.append(row_data)
    return helper.get_rows(rows, indices)

def _parse_row(row):
    if row and len(row) == 1:
        return tuple(row[0].split(','))
