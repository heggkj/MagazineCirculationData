import os, argparse, xlrd
from utilities import database_utilities


def find_titles(database_path: str):
    os.chdir(os.path.dirname(__file__))
    path = os.path.join(os.getcwd(), "spreadsheets")
    files = os.listdir(path)
    for name in files:
        if name[-5:] == '.xlsx':
            spreadsheet_path = os.path.join(path, name)
            wb = xlrd.open_workbook(spreadsheet_path)
            sheet = wb.sheet_by_index(0)
            mag_title = sheet.cell_value(1, 6)
            if isinstance(mag_title, str):
                mag_title = mag_title.strip()
                if mag_title[4:5] == '1':
                    title_code = name[:5]
                else:
                    title_code = name[:4]
                if len(mag_title) > 0:
                    database_utilities.add_row_to_magazines(database_path=database_path, title_code=title_code,
                                                        reported_title=mag_title)
            else:
                print("ERROR: " + name)


def audit_titles(database_path: str):
    os.chdir(os.path.dirname(__file__))
    path = os.path.join(os.getcwd(), "spreadsheets")
    files = os.listdir(path)
    for name in files:
        if name[-5:] == '.xlsx':
            spreadsheet_path = os.path.join(path, name)
            wb = xlrd.open_workbook(spreadsheet_path)
            sheet = wb.sheet_by_index(0)
            mag_title = sheet.cell_value(1, 6)
            if isinstance(mag_title, str):
                mag_title = mag_title.strip()
                if mag_title[4:5] == '1':
                    title_code = name[:5]
                else:
                    title_code = name[:4]
                if len(mag_title) < 1:
                    mag_title = "NO TITLE PROVIDED"
                database_utilities.add_row_to_title_audit(database_path=database_path, title_code=title_code,
                                                        reported_title=mag_title, file_name=name)
            else:
                print("ERROR: " + name)


def process_sheets(database_path: str):
    os.chdir(os.path.dirname(__file__))
    ta_wb = xlrd.open_workbook(os.path.join(os.getcwd(), "title_audit.xlsx"))
    ta_sheet = ta_wb.sheet_by_index(0)
    ta_dict = {}
    for row in range (1, ta_sheet.nrows):
        cell_value_title = ta_sheet.cell(row, 3).value
        cell_value_filename = ta_sheet.cell(row, 1).value
        ta_dict[cell_value_filename] = cell_value_title

    mt_wb = xlrd.open_workbook(os.path.join(os.getcwd(), "magazine_titles.xlsx"))
    mt_sheet = mt_wb.sheet_by_index(0)
    mt_dict = {}
    for row in range(1, mt_sheet.nrows):
        cell_value_reported_title = mt_sheet.cell(row, 2).value
        cell_value_canonical_title = mt_sheet.cell(row, 1).value
        mt_dict[cell_value_reported_title] = cell_value_canonical_title

    path = os.path.join(os.getcwd(), "spreadsheets")
    files = os.listdir(path)
    for name in files:
        if name[-5:] == '.xlsx':
            spreadsheet_path = os.path.join(path, name)
            wb = xlrd.open_workbook(spreadsheet_path)
            sheet = wb.sheet_by_index(0)
            reported_title = ""
            print(ta_dict[name])
        else:
            print("ERROR: " + name)



def main(my_function: str):
    database_path = os.path.join(os.getcwd(), "circulation.db")
    if my_function == "preprocess":
        print('preprocess')
        audit_titles(database_path=database_path)
    else:
        print('aggregate data')
        process_sheets(database_path=database_path)
    os.chdir(os.path.dirname(__file__))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--function", help="preprocess or aggregate")
    args = parser.parse_args()
    main(my_function=args.function)
