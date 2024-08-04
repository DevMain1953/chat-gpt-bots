import json
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()


async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def get_recommended_snowboards(
    name: str, experience: str, goal: str, additional_info: str
) -> str:
    """
    Returns text about recommend snowboard based on user experience, goal of buying and additional info.

    :param name: A name of user.
    :type name: str

    :param experience: An experience of user.
    :type experience: str

    :param goal: A goal of buying snowboard.
    :type goal: str

    :param additional_info: An additional info from user.
    :type additional_info: str

    :return: A text about recommend snowboard based on user experience, goal of buying and additional info.
    :rtype: str
    """
    conversation = [
        {
            "role": "system",
            "content": "Ты - робот Алёша. Помоги человеку выбрать доску для сноуборда.",
        },
        {
            "role": "user",
            "content": f"Имя: {name}\nОпыт: {experience}\nЦель покупки: {goal}\nДополнительная информация: {additional_info}\nПосоветуй, какой сноуборд лучше выбрать.",
        },
    ]

    response = await async_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=conversation, max_tokens=150
    )

    return response.choices[0].message["content"].strip()


async def get_user_input_using_prompt(prompt: str) -> str:
    """
    Returns text that is entered by user using prompt. This text will be used in gpt model.

    :param prompt: A prompt that is used to get text from target user.
    :type prompt: str

    :return: A text that is entered by user using prompt. This text will be used in gpt model.
    :rtype: str
    """
    conversation = [
        {
            "role": "system",
            "content": "Ты - робот Алёша. Помоги человеку выбрать доску для сноуборда.",
        },
        {"role": "user", "content": prompt},
    ]
    response = await async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        max_tokens=100,
    )
    return response.choices[0].message["content"].strip()


async def get_snowboard_info() -> str:
    """
    Returns text with snowboard info.

    :return: A text with snowboard info.
    :rtype: str
    """
    user_info = {}
    user_info["Имя"] = await get_user_input_using_prompt("Как вас зовут?")
    user_info["Опыт"] = await get_user_input_using_prompt(
        "Каков ваш опыт в сноубординге? (Начинающий, Средний, Опытный)"
    )
    user_info["Цель покупки"] = await get_user_input_using_prompt(
        "Для чего вы покупаете сноуборд? (Например: катание в парке, спуск с гор, фрирайд и т.д.)"
    )
    user_info["Дополнительная информация"] = await get_user_input_using_prompt(
        "Есть ли другая полезная информация, которую вы хотите сообщить?"
    )

    snowboard_info = {}
    snowboard_info["Рекомендация"] = get_recommended_snowboards(
        user_info["Имя"],
        user_info["Опыт"],
        user_info["Цель покупки"],
        user_info["Дополнительная информация"],
    )

    return json.dumps(snowboard_info, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    snowboard_info = asyncio.run(get_snowboard_info())
    print(snowboard_info)
