import argparse
from excel_translate.ai_utils import AI_chat

parser = argparse.ArgumentParser(description="Process some integers.")


parser.add_argument("edit", help="edit .env file")

args = parser.parse_args()
if args.edit == "edit":
    AI_chat().edit_env_file()
