from excel_translate import excel_opreations


class Test_Cases:
    def test_translate_data(self):
        input_file = [
            ["test", "test2"],
            ["test3", "test4"],
            ["test3", "test4"],
            ["test3", "test4"],
        ]
        returned_file = excel_opreations.ExcelProcessor.translate_data(input_file)
        print(returned_file)
