import openpyxl
from openpyxl.utils import (
    get_column_letter,
    column_index_from_string,
)
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string
import numpy as np
import os


class ExcelProcessor:
    def __init__(
        self,
        input_file,
        output_file,
        input_range,
        output_range,
        input_sheet_name=None,
        output_sheet_name=None,
    ):
        self.input_file = input_file
        self.output_file = output_file
        self.input_range = input_range
        self.output_range = output_range
        self.input_sheet_name = input_sheet_name
        self.output_sheet_name = output_sheet_name

    def process_excel(self):
        # Check if output file exists
        if not os.path.isfile(self.input_file):
            raise Exception(f"Input file {self.input_file} does not exist.")
            # Load the input workbook
        wb_input = openpyxl.load_workbook(self.input_file)

        # Check if input sheet exists
        if self.input_sheet_name and self.input_sheet_name not in wb_input.sheetnames:
            raise Exception(
                f"Input sheet {self.input_sheet_name} does not exist in the input file."
            )
        # Modify range processing to handle a single letter

        def convert_range(r):
            if ":" in r:
                return r
            else:
                max_row = str(wb_input.active.max_row)
                return r + "1:" + r + max_row

        self.input_range = convert_range(self.input_range)
        self.output_range = convert_range(self.output_range)
        # Check if input range equals output range
        start_cell_input, end_cell_input = self.input_range.split(":")
        start_cell_output, end_cell_output = self.output_range.split(":")

        col_input_start, row_input_start = coordinate_from_string(start_cell_input)
        col_input_end, row_input_end = coordinate_from_string(end_cell_input)
        col_output_start, row_output_start = coordinate_from_string(start_cell_output)
        col_output_end, row_output_end = coordinate_from_string(end_cell_output)

        if (
            column_index_from_string(col_input_end)
            - column_index_from_string(col_input_start)
            != column_index_from_string(col_output_end)
            - column_index_from_string(col_output_start)
        ) or (
            int(row_input_end) - int(row_input_start)
            != int(row_output_end) - int(row_output_start)
        ):
            raise Exception("The input range and output range are not equal.")

        if os.path.isfile(self.output_file):
            wb = openpyxl.load_workbook(self.output_file)
        else:
            # Load the input workbook and save as a new output file if the output file does not exist
            wb = openpyxl.load_workbook(self.input_file)
            wb.save(self.output_file)

        # Get the selected output sheet or the first sheet if not specified
        if self.output_sheet_name is None:
            sheet = wb.active
        else:
            sheet = wb[self.output_sheet_name]

        # Read the input range data
        input_data = []
        for row in sheet[self.input_range]:
            row_data = [cell.value for cell in row]
            input_data.append(row_data)
        print(input_data)
        # Write the output range data
        for output_row, input_row in zip(sheet[self.output_range], input_data):
            print(output_row, input_row)
            for output_cell, input_value in zip(output_row, input_row):
                output_cell.value = input_value

        # Save the modified workbook
        wb.save(self.output_file)

    @staticmethod
    def translate_data(input_data, batch_size=10):
        num_rows, num_cols = input_data.shape
        translated_data = []
        for i in range(0, num_rows, batch_size):
            batch = input_data[i : i + batch_size]
            batch_list = batch.ravel().tolist()
            translated_batch_list = [x + "s" for x in batch_list]
            translated_batch = np.array(translated_batch_list).reshape(batch.shape)
            translated_data.append(translated_batch)
        translated_data = np.concatenate(translated_data)
        return translated_data


if __name__ == "__main__":
    # Example usage
    input_file = (
        "/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/test_1.xlsx"
    )
    output_file = (
        "/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/output.xlsx"
    )
    input_range = "G1:H10"
    output_range = "I1:J10"

    excel_processor = ExcelProcessor(
        input_file,
        output_file,
        input_range,
        output_range,
    )

    excel_processor.process_excel()
