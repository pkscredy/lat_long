import csv
import os
from address.constants import UPLOADED_FILE
from xlrd import open_workbook
from xlsxwriter import Workbook


class CSVHandler:
    def __init__(self):
        pass

    def csv_from_excel(self, doc_obj):
        wb = open_workbook(doc_obj.document.path)
        os.makedirs(os.path.dirname(UPLOADED_FILE), exist_ok=True)
        with open(UPLOADED_FILE, 'w+') as csv_file:
            for s in wb.sheet_names():
                sh = wb.sheet_by_name(s)
                wr = csv.writer(csv_file, delimiter=',')
                for row_idx in range(sh.nrows):
                    row = [int(cell.value) if isinstance(cell.value, float)
                           else cell.value for cell in sh.row(row_idx)]
                    wr.writerow(row)

    def generate_excel_file(self, doc_obj, city_info_data):
        ordered_list = ['address', 'latitude', 'longitude']
        file_path = '/tmp/prashant/{}.xlsx'.format(doc_obj.file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        wb = Workbook(file_path)
        ws = wb.add_worksheet('New Sheet')

        first_row = 0
        for header in ordered_list:
            col = ordered_list.index(header)
            ws.write(first_row, col, header)

        row = 1
        for data in city_info_data:
            for _key, _value in data.items():
                col = ordered_list.index(_key)
                ws.write(row, col, _value)
            row += 1
        wb.close()
