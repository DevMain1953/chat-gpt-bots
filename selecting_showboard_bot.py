import json
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()


async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def get_user_input_using_prompt(prompt: str) -> str:
    """
    Returns text that is entered by user using prompt. This text will be used in gpt model.

    :param prompt: A prompt that is used to get text from target user.
    :type prompt: str

    :return: A text that is entered by user using prompt. This text will be used in gpt model.
    :rtype: str
    """
    response = await async_client.chat.completions.create(
        model="gpt-3.5",
        messages=[
            {
                "role": "system",
                "content": "Ты - робот Алёша. Помоги человеку выбрать доску для сноуборда.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=100,
    )
    return response.choices[0].message["content"].strip()


def get_snowboard_info() -> str:
    """
    Returns text with snowboard info.

    :return: A text with snowboard info.
    :rtype: str
    """
    user_info = {}

    user_info["Имя"] = get_user_input_using_prompt("Как вас зовут?")
    user_info["Опыт"] = get_user_input_using_prompt(
        "Каков ваш опыт в сноубординге? (Начинающий, Средний, Опытный)"
    )
    user_info["Цель покупки"] = get_user_input_using_prompt(
        "Для чего вы покупаете сноуборд? (Например: катание в парке, спуск с гор, фрирайд и т.д.)"
    )
    user_info["Дополнительная информация"] = get_user_input_using_prompt(
        "Есть ли другая полезная информация, которую вы хотите сообщить?"
    )

    return json.dumps(user_info, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    snowboard_info = get_snowboard_info()
    print(snowboard_info)
