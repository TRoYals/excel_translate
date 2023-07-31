from typing import List, Dict, Tuple, Union
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.output_parsers import json
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import subprocess


class AI_chat:
    """where we chat"""

    load_dotenv()
    model = ChatOpenAI(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
    )  # type: ignore

    translate_rules = os.getenv("TRANSLATE_RULES")

    def edit_env_file(self):
        env_file = ".env"
        subprocess.run(["vim", env_file])

    @classmethod
    # FIXME: may add some feature to this
    def chat_translate(
        cls,
        text: str,
        translate_from="cn",
        translate_to="en",
    ) -> str:
        content = """Here is a list of text you need translate from {translate_from} to {translate_to}, your translation should followed the rules below:{translate_rules},
        and your response should be a translated list  in JSON format.
        Here is the word list you need to translate:{translate_test}"""

        content = content.format(
            translate_test=text,
            translate_from=translate_from,
            translate_to=translate_to,
            translate_rules=cls.translate_rules,
        )
        Human_message = HumanMessage(content=content)
        print(Human_message)
        text = cls.model([Human_message]).content
        return text


if __name__ == "__main__":
    ai_chat = AI_chat.chat_translate('[""你好"", "test 1", "SKU 号码"]')
    print(ai_chat)
