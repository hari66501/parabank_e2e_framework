# utils/excel_reader.py
import openpyxl

def read_excel(file_path, sheet_name=None):
    """
    Read Excel file and return a list of dictionaries (one dict per row)
    :param file_path: path to Excel file
    :param sheet_name: optional sheet name; defaults to first sheet
    """
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name or workbook.active.title]

    # Read headers from the first row
    headers = [cell.value for cell in sheet[1]]

    data = []
    # Iterate over rows starting from second row (skip headers)
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_dict = dict(zip(headers, row))
        data.append(row_dict)

    return data


