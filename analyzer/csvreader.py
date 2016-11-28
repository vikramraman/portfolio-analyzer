import csv

def read(filename):
    """
    Reads a CSV file and returns a list of tuples (Each tuple represents a row
    in the CSV file).
    """
    if not filename:
        raise "Invalid CSV filename"

    out = []
    with open(filename, 'rb') as csvFile:
        fileReader = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in fileReader:
            rowData = _parseRow(row)
            if rowData:
                out.append(rowData)
    return out

def _parseRow(row):
    if row and len(row) == 1:
        return tuple(row[0].split(','))
