# excel_translate

使用 ChatGPT 翻译 excel 文件至任何语言

## 安装

首先需要有 python 环境 (3.10+)

然后安装本项目包
pip install excel_translate-0.1.8-py3-none-any.whl (这个文件你可以在 release 界面下载)

安装成功后, 即可使用

## 使用方法

安装成功后你可以通过 `excel_translate` 来使用本项目, 你可以通过 `excel_translate --help` 来查看帮助

在使用之前, 首先确保你输入了可以使用的 OPENAI_API_KEY, 你可以在系统的环境变量中配置该字段
也可以通过使用 `excel_translate edit --config` 在本地配置该字段, 同时你也可以配置其他的字段(如: 翻译的语言, 翻译的规则等)

配置完成后, 通过以下方式进行文件的翻译

```
excel_translate process -i /Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/test_1.xlsx -o /Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/output.xlsx -i_range G1:G30 -o_range I1:I30

```

-i: 输入文件的路径
-o: 输出文件的路径
-i_range: 输入文件的翻译范围 (excel 的单元格范围)
-o_range: 输出文件的翻译范围 (excel 的单元格范围)

## 使用的 prompt:

"""Here is a list of text you need translate from {translate_from} to {translate_to}, your translation should followed the rules below:{translate_rules},
Here is the word list you need to translate:{translate_test} .Your response must be in JSON format, not in a list object,and the JSON must have the same length with the list. eg: ["中国","美国"] must be in the format {{{{'中国': 'Chinese'}},{{'美国': 'America}}}}
{extract_text}"""

translate_from 字段: 你需要翻译的语言
translate_to 字段: 你需要翻译成的语言
translate_rules 字段: 你需要 ChatGPT 遵守的翻译规则
extra_text 字段: 额外的指令

你可以通过这个指令编辑以上的字段: `excel_translate edit --config`

输入这个指令后, 你可以使用`vim`来编辑 config.json
