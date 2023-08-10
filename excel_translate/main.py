import argparse
from excel_translate.ai_utils import AI_chat
from excel_translate.excel_opreations import ExcelProcessor
import os
import platform
import subprocess


def edit_config_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config.json")
    if platform.system() == "Windows":
        subprocess.run(["notepad", config_path])
    else:
        subprocess.run(["vim", config_path])


def main():
    parser = argparse.ArgumentParser(description="Excel processing tool")

    subparsers = parser.add_subparsers(dest="command")

    parser_process = subparsers.add_parser("process", help="Process excel file.")
    parser_process.add_argument(
        "-i", "--input_file", type=str, required=True, help="Input file path"
    )
    parser_process.add_argument(
        "-o", "--output_file", type=str, required=True, help="Output file path"
    )
    parser_process.add_argument(
        "-i_range",
        "--input_range",
        type=str,
        required=True,
        help="Input range in excel",
    )
    parser_process.add_argument(
        "-o_range",
        "--output_range",
        type=str,
        required=True,
        help="Output range in excel",
    )
    parser_process.add_argument("--input_sheet_name", type=str, help="Input sheet name")
    parser_process.add_argument(
        "--output_sheet_name", type=str, help="Output sheet name"
    )
    parser_process.add_argument("--max_workers", type=int, help="max work threads")
    parser_edit = subparsers.add_parser("edit", help="Edit configuration.")
    parser_edit.add_argument("--preview", action="store_true", help="preview your prompt")
    parser_edit.add_argument("--config", action="store_true", help="Edit config file")

    args = parser.parse_args()

    if args.command == "edit":
        if args.config:
            edit_config_file()
        if args.preview:
            AI_chat().chat_translate(text="{{text to be translated}}", preview=True)
    elif args.command == "process":
        excel_processor = ExcelProcessor(
            input_file=args.input_file,
            output_file=args.output_file,
            input_range=args.input_range,
            output_range=args.output_range,
            input_sheet=args.input_sheet_name,
            output_sheet=args.output_sheet_name,
            max_workers=args.max_workers
        )
        excel_processor.process_excel()
    else:
        parser.print_help()

    return
