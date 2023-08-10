# excel_translate

使用 ChatGPT 翻译 excel 文件至任何语言

## TODO:

- [x] 使用并发来加快翻译速度

## 步骤

1.  安装 python 环境
2.  进入 cmd
3.  安装本项目包
4.  配置 OPENAI_API_KEY
5.  配置 你需要自定义的翻译规则
6.  开始使用

## 详细步骤

### 1. 安装 python 环境

略

### 2. 进入 cmd/terminal

win 搜索 cmd, mac 搜索 terminal

### 3. 安装本项目包

首先下载 abcde.whl,然后复制你下载下来的文件路径, 然后在 cmd/terminal 中输入以下指令

pip install {你的路径}

如
`pip install /xxx/xxx/excel_translate-0.1.10-py3-none-any.whl`

### 4. 配置 OPENAI_API_KEY

在命令行输入以下指令
excel_translate edit --config

然后在 config.json 中配置 OPENAI_API_KEY

### 5. 配置 你需要自定义的翻译规则

在 config.json 中配置其他命令规则

通过 excel_translate edit --preview 预览 prompt

### 6.开始使用

`excel_translate process -i {需要翻译的 xlsx 文件} -o {翻译出来的结果路径(文件可以存在)} -i_range {需要翻译的范围如"G1:G30"} -o_range {翻译的结果输出的范围如:"I1:I30"}`

一个参考例子:
`excel_translate process -i /Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/test_1.xlsx -o /Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/output.xlsx -i_range G1:G30 -o_range I1:I30`

## 使用方法

安装成功后你可以通过 `excel_translate` 来使用本项目, 你可以通过 `excel_translate --help` 来查看帮助

在使用之前, 首先确保你输入了可以使用的 OPENAI_API_KEY, 你可以在系统的环境变量中配置该字段
也可以通过使用 `excel_translate edit --config` 在本地配置该字段, 同时你也可以配置其他的字段(如: 翻译的语言, 翻译的规则等)

配置完成后, 通过以下方式进行文件的翻译

`excel_translate process -i /Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/test_1.xlsx -o /Users/fuqixuan/Documents/vscode/excel_translate/tests/test_files/output.xlsx -i_range G1:G30 -o_range I1:I30`

-i: 输入文件的路径

-o: 输出文件的路径

-i_range: 输入文件的翻译范围 (excel 的单元格范围)

-o_range: 输出文件的翻译范围 (excel 的单元格范围)

-max_workers: 最大的并发数, 默认为 40

## 使用的 prompt:

"Here is a list of text you need translate from {translate_from} to {translate_to}, your translation should followed the rules below:{translate_rules},
And you must only return the sentence that have been translated, here is the sentence you need to translate:
{translate_test}

{extra_text}

translate_from 字段: 你需要翻译的语言
translate_to 字段: 你需要翻译成的语言
translate_rules 字段: 你需要 ChatGPT 遵守的翻译规则
extra_text 字段: 额外的指令(可以放一些翻译示例)

你可以通过这个指令编辑以上的字段: `excel_translate edit --config`

输入这个指令后, 你可以使用`vim`来编辑 config.json(mac\linux), `notepad` 来编辑 config.json(win)
