import numpy as np

from excel_translate.excel_opreations import ExcelProcessor
from excel_translate.ai_utils import AI_chat


class Test_Cases:
    def test_translate_data(self):
        input_file = [
            ["test", "test2"],
            ["test3", "test4"],
            ["test3", "test4"],
            ["test3", "test4"],
        ]
        returned_file = ExcelProcessor.translate_data(input_file)
        print(returned_file)
        expected_output = np.array(
            [
                ["tests", "test2s"],
                ["test3s", "test4s"],
                ["test3s", "test4s"],
                ["test3s", "test4s"],
            ]
        )
        np.testing.assert_array_equal(returned_file, expected_output)

    def test_extract(self):
        text = """{
  "项目组织ID": "Project Organization ID",
  "品牌主色色值请使用16进制!": "Please use hexadecimal for the main color value of the brand!",
  "${label}是必填项!": "${label} is a required field!",
  "单据转换规则 {0} 使用了特征 {1}": "Document conversion rule {0} uses feature {1}",
  "业务流 {0} 使用了特征 {1}": "Business flow {0} uses feature {1}",
  "物料档案导入": "Material file import",
  "填写系统已存在的费用项目编码，当物料类型为费用类物料时，必填！": "Fill in the existing expense item code in the system, it is required when the material type is expense material!",
  "当存在编码相同，主成员对系统中对应成员属性进行更新，以主成员为Y的行为准;Y:是,N:否;": "When there are identical codes, the main member updates the corresponding member attributes in the system. The behavior is based on the main member being Y; Y: Yes, N: No;",
  "数据月份": "Data month",
  "检测用户开启密级失败，请检查": "Failed to check user's security level, please check"
}"""
        returned_text = AI_chat().extract_json_from_str(text)
        print(returned_text)


if __name__ == "__main__":
    Test_Cases().test_extract()
