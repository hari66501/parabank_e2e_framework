import csv


def read_csv(file_path):
    """Return list of dicts from a CSV file"""
    with open(file_path, newline="") as csvfile:
        return list(csv.DictReader(csvfile))