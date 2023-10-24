import threading
import openpyxl
from concurrent.futures import ThreadPoolExecutor
from excel_translate.ai_utils import AI_chat
import os
import shutil


class ExcelProcessor:
    def __init__(
        self,
        input_file,
        input_range,
        output_range,
        input_sheet=None,
        output_sheet=None,
        max_workers=40,
    ):
        self.input_file = input_file
        self.input_range = input_range
        self.output_range = output_range
        self.input_sheet = input_sheet
        self.output_sheet = output_sheet
        self.max_workers = max_workers

    def translate_row(self, in_row, out_row):
        input_col_start, input_row_start = self.input_range.split(":")[0][0], int(
            self.input_range.split(":")[0][1:]
        )
        input_col_end, input_row_end = self.input_range.split(":")[1][0], int(
            self.input_range.split(":")[1][1:]
        )
        translated_row = [self.translate_cell(cell.value) for cell in in_row]
        for cell, translated_value in zip(out_row, translated_row):
            cell.value = translated_value

    def translate_cell(self, cell_value):
        return AI_chat().chat_translate(cell_value)

    def process_excel(self):
        wb_input = openpyxl.load_workbook(self.input_file)
        ws_input = self.input_sheet or wb_input.active
        if not os.path.exists(self.output_file):
            shutil.copy(self.input_file, self.output_file)
            if os.name == "nt":  # Windows
                # 移除文件的只读属性
                os.chmod(self.output_file, 0o777)
            elif os.name == "posix":  # Mac/Linux
                # 设置文件权限为可编辑
                os.chmod(self.output_file, 0o644)
        wb_output = openpyxl.load_workbook(self.output_file)
        ws_output = self.output_sheet or wb_output.active
        input_cells = list(ws_input[self.input_range])
        output_cells = list(ws_output[self.output_range])
        try:
            with ThreadPoolExecutor(self.max_workers) as executor:
                futures = []
                for in_row, out_row in zip(input_cells, output_cells):
                    future = executor.submit(self.translate_row, in_row, out_row)
                    futures.append(future)
                for future in futures:
                    try:
                        future.result()  # 获取任务结果，会抛出异常
                    except Exception as e:
                        print("An exception occurred in a thread:", e)
            wb_output.save(self.output_file)
        except Exception as e:
            print(e)
            wb_output.save(self.output_file)


if __name__ == "__main__":
    input_file = (
        "/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/333.xlsx"
    )
    input_range = "G800:G1001"
    output_range = "H800:H1001"
    output_file = (
        "/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/334.xlsx"
    )
    excel_processor = ExcelProcessor(
        input_file,
        output_file,
        input_range=input_range,
        output_range=output_range,
    )

    excel_processor.process_excel()
