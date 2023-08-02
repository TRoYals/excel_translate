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

    parser_edit = subparsers.add_parser("edit", help="Edit configuration.")
    parser_edit.add_argument("--env", action="store_true", help="Edit .env file")
    parser_edit.add_argument("--config", action="store_true", help="Edit config file")

    args = parser.parse_args()

    if args.command == "edit":
        if args.env:
            edit_config_file()
        if args.config:
            edit_config_file()
    elif args.command == "process":
        excel_processor = ExcelProcessor(
            args.input_file,
            args.output_file,
            args.input_range,
            args.output_range,
            args.input_sheet_name,
            args.output_sheet_name,
        )
        excel_processor.process_excel()
    else:
        parser.print_help()

    return
