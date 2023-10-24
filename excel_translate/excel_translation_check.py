"""
为了检测翻译质量, 我们需要一个验收程序来确认程序翻译的结果是可以被程序接受的
该部分主要是为了完成这部分业务需求.
"""


import pandas as pd
import re
import os


def col_letter_to_index(col_letter):
    """Convert a column letter (like 'G') to its numeric index (like 6)."""
    return (
        sum([(ord(char) - 64) * (26**i) for i, char in enumerate(col_letter[::-1])])
        - 1
    )


class ExcelChecker:
    def __init__(
        self,
        input_file,
        input_range,
        output_range,
        input_sheet=None,
    ):
        self.input_file = input_file
        self.input_range = input_range
        self.output_range = output_range
        self.input_sheet = input_sheet if input_sheet else 0

    def process_translations(self):
        issues = []
        # Define columns to read based on input and output range
        cols_to_read = [
            col_letter_to_index(self.input_range.split(":")[0][0]),
            col_letter_to_index(self.output_range.split(":")[0][0]),
        ]

        # Define rows to read based on input range
        row_start = int(self.input_range.split(":")[0][1:]) - 1
        row_end = int(self.input_range.split(":")[1][1:])

        # Read specific columns and rows from the sheet
        df = pd.read_excel(
            self.input_file,
            engine="openpyxl",
            usecols=cols_to_read,
            skiprows=range(0, row_start),
            nrows=row_end - row_start + 1,
            sheet_name=self.input_sheet,
        )
        for index, row in df.iterrows():
            original_text = str(row.iloc[0])
            translated_text = str(row.iloc[1])
            # 1. 检测翻译后的文件是否有汉字
            if re.search(r"[\u4e00-\u9fff]", translated_text):
                issues.append(
                    f"Row {index + 2}: Translated text contains Chinese characters."
                )

            # 2. 检测<% XXX %>这样的字符
            original_tags = re.findall(r"<%\s*(\w+)\s*%>", original_text)
            translated_tags = re.findall(r"<%\s*(\w+)\s*%>", translated_text)
            if set(original_tags) != set(translated_tags):
                issues.append(
                    f"Row {index + 2}: Mismatched tags between original and translated texts."
                )

            # 3. 检测%d这样的通配符
            if original_text.count("%d") != translated_text.count("%d"):
                issues.append(
                    f"Row {index + 2}: Mismatched '%d' between original and translated texts."
                )

            # 4. 检测%s这样的通配符
            if original_text.count("%s") != translated_text.count("%s"):
                issues.append(
                    f"Row {index + 2}: Mismatched '%s' between original and translated texts."
                )

            # 5. 检测{counts}这样的字符
            original_counts = re.findall(r"{(\w+)}", original_text)
            translated_counts = re.findall(r"{(\w+)}", translated_text)
            if set(original_counts) != set(translated_counts):
                issues.append(
                    f"Row {index + 2}: Mismatched contents inside {{}} between original and translated texts."
                )

            # 6. 检测原文是否包含中文字符
            if not re.search(r"[\u4e00-\u9fff]", original_text):
                # 如果原文没有中文字符并且翻译后的文本与原文不同
                if original_text != translated_text:
                    issues.append(
                        f"Row {index + 2}: Original text without Chinese characters should remain unchanged in translation but it's different."
                    )
        output_file_path = os.path.join(os.path.dirname(self.input_file), "issues.txt")
        with open(output_file_path, "w", encoding="utf-8") as f:
            for issue in issues:
                f.write(issue + "\n")
        for issue in issues:
            print(issue)
        return issues


def main():
    test = ExcelChecker(
        input_file="/Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/未翻译内容_23_0914_0949增量-英文.xlsx",
        input_range="G2:G50000",
        output_range="H2:H5000",
    )
    issues = test.process_translations()
    for issue in issues:
        print(issue)


if __name__ == "__main__":
    main()
