import json
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
from dotenv import load_dotenv
import subprocess
import re
from typing import List
import platform


class AI_chat:
    """where we chat"""

    load_dotenv()

    def __init__(self) -> None:
        self.translate_rules = None
        self.translate_to = None
        self.translate_from = None
        self.extra_text = None
        self.openai_api_key = None
        self.read_config()
        self.model = ChatOpenAI(
            openai_api_key=self.openai_api_key,
            temperature=0,
        )  # type: ignore

    def read_config(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "config.json")

        try:
            with open(config_path, "r") as config_file:
                config_data = json.load(config_file)
            self.translate_rules = config_data.get("rules")
            self.translate_to = config_data.get("translate_to")
            self.translate_from = config_data.get("translate_from")
            self.extra_text = config_data.get("extra_text")
            self.openai_api_key = config_data.get("OPENAI_API_KEY")
        except FileNotFoundError:
            print("config.json not found.")
        except json.JSONDecodeError:
            print("Invalid JSON format in config.json.")
        except Exception as e:
            print(f"Error while reading config.json: {e}")

    def edit_env_file(self):
        env_file = ".env"
        if platform.system() == "Windows":
            subprocess.run(["notepad", env_file])
        else:
            subprocess.run(["vim", env_file])

    def edit_config_file(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, "config.json")
        if platform.system() == "Windows":
            subprocess.run(["notepad", config_path])
        else:
            subprocess.run(["vim", config_path])

    # FIXME: may add some feature to this
    def chat_translate(
        self,
        text,
    ):
        content = """Here is a list of text you need translate from {translate_from} to {translate_to}, your translation should followed the rules below:{translate_rules},
        Here is the word list you need to translate:{translate_test} .Your response must be in JSON format, not in a list object,and the JSON must have the same length with the list. eg: ["中国","美国"] must be in the format {{{{'中国': 'Chinese'}},{{'美国': 'America}}}}
        {extra_text}"""

        content = content.format(
            translate_test=text,
            translate_from=self.translate_from,
            translate_to=self.translate_to,
            translate_rules=self.translate_rules,
            extra_text=self.extra_text,
        )
        Human_message = HumanMessage(content=content)
        # print(Human_message)
        text = self.model([Human_message]).content
        return text

    # def text_to_lists(self, text: str) -> List[str]:
    #     return json.loads(text)

    @staticmethod
    def extract_json_from_str(input_str):
        regex = r"\{.*\}"

        # Try to find the first JSON object in the input string
        match = re.search(regex, input_str, re.DOTALL)

        if match is None:
            print("No JSON object found in the input string.")
            return {}

        json_str = match.group()
        try:
            # Try to parse the JSON object
            json_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse the JSON object: {e}")
            return {}
        return json_data

    def translated_list_to_list(self, translated_list: List[str]) -> List[str]:
        ai_chat_str = self.chat_translate(translated_list)

        returned_JSON = self.extract_json_from_str(ai_chat_str)

        value_list = list(returned_JSON.values())
        return value_list


if __name__ == "__main__":
    # ai_chat = AI_chat.chat_translate(
    #     [
    #         "此配送员有待处理的配送单，请先转移",
    #         "Terdapat pesanan pengiriman yang perlu ditangani oleh kurir ini, harap dipindahkan terlebih dahulu.",
    #         "Flex布局",
    #         "Tata letak flex",
    #     ]
    # )

    # returned_JSON = AI_chat.extract_json_from_str(ai_chat)
    # value_list = list(returned_JSON.values())
    # print(value_list)
    test = AI_chat().translated_list_to_list(
        [
            "此配送员有待处理的配送单，请先转移",
            "Terdapat pesanan pengiriman yang perlu ditangani oleh kurir ini, harap dipindahkan terlebih dahulu.",
            "Flex布局",
            "Tata letak flex",
            "https://github.com/langchain-ai/langchain/blob/master/libs/langchain/测试",
        ]
    )
    print(test)
