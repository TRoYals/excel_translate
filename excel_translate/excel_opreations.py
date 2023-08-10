import threading
import openpyxl
from concurrent.futures import ThreadPoolExecutor
from excel_translate.ai_utils import AI_chat
import os
import shutil


class ExcelProcessor:

    def __init__(self, input_file, output_file=None, input_range=None, output_range=None,input_sheet=None,output_sheet=None,max_workers=40):
        self.input_file = input_file
        self.output_file = output_file or input_file.replace('.xlsx', '_output.xlsx')
        self.input_range = input_range
        self.output_range = output_range
        self.input_sheet = input_sheet
        self.output_sheet = output_sheet
        self.max_workers = max_workers
        self.lock = threading.Lock()

    def translate_row(self, in_row, out_row):
        translated_row = [self.translate_cell(cell.value) for cell in in_row]
        
        with self.lock:
            for cell, translated_value in zip(out_row, translated_row):
                cell.value = translated_value

    def translate_cell(self, cell_value):
        return AI_chat().chat_translate(cell_value)

    def process_excel(self):
        wb_input = openpyxl.load_workbook(self.input_file)
        ws_input = self.input_sheet or wb_input.active
        if not os.path.exists(self.output_file):
            shutil.copy(self.input_file, self.output_file)

        wb_output = openpyxl.load_workbook(self.output_file)
        ws_output = self.output_sheet or wb_output.active
            
        input_cells = list(ws_input[self.input_range])
        output_cells = list(ws_output[self.output_range])

        with ThreadPoolExecutor(self.max_workers) as executor:
            for in_row, out_row in zip(input_cells, output_cells):
                executor.submit(self.translate_row, in_row, out_row)

        wb_output.save(self.output_file)

if __name__ == "__main__":
    input_file = (
        "/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/test_1.xlsx"
    )
    input_range = "D1:D40"
    output_range = "E1:E40"
    output_file = (
        "/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/output.xlsx"
    )
    excel_processor = ExcelProcessor(
        input_file,
        output_file,
        input_range=input_range,
        output_range=output_range,
    )

    excel_processor.process_excel()
