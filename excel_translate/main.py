import argparse
from excel_translate.ai_utils import AI_chat
from excel_translate.excel_opreations import ExcelProcessor


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
        ai_chat = AI_chat()
        if args.env:
            ai_chat.edit_env_file()
        if args.config:
            ai_chat.edit_config_file()
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
