import json
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()


async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_recommended_snowboards(experience: str, goal: str) -> str:
    """
    Returns text about recommend snowboard based on user experience and goal of buying.

    :param experience: An experience of user.
    :type experience: str

    :param goal: A goal of buying snowboard.
    :type goal: str

    :return: A text about recommend snowboard based on user experience and goal of buying.
    :rtype: str
    """
    recommendations = {
        "Начинающий": {
            "катание в парке": "Для начинающих, которые хотят кататься в парке, рекомендуется использовать мягкие и легкие сноуборды, которые прощают ошибки и обеспечивают легкость в управлении.",
            "спуск с гор": "Для начинающих, которые предпочитают спускаться с гор, лучше подойдут универсальные (all-mountain) сноуборды с средней жесткостью, обеспечивающие стабильность и контроль.",
            "фрирайд": "Для фрирайда начинающим рекомендуется выбирать сноуборды с направленной формой и немного более жесткие, чем универсальные модели, для лучшей управляемости в глубоком снегу.",
        },
        "Средний": {
            "катание в парке": "Для среднего уровня в парке лучше подойдут твин-тип (twin-tip) сноуборды с хорошей гибкостью и усиленными краями для выполнения трюков.",
            "спуск с гор": "Сноуборды для среднего уровня для спусков с гор должны быть универсальными, но с немного большей жесткостью для лучшего контроля на высоких скоростях.",
            "фрирайд": "Для среднего уровня в фрирайде подойдут сноуборды с прогибом camber или directional сноуборды с усиленными краями для лучшего сцепления и стабильности.",
        },
        "Опытный": {
            "катание в парке": "Опытным райдерам в парке подойдут жесткие твин-тип сноуборды с высококачественными материалами для максимальной отзывчивости и точности.",
            "спуск с гор": "Опытные райдеры для спусков с гор могут выбирать жесткие универсальные или карвинговые (carving) сноуборды для максимальной производительности на высоких скоростях.",
            "фрирайд": "Для опытных фрирайдеров идеальны жесткие directional или powder сноуборды, обеспечивающие максимальную плавучесть и контроль в глубоком снегу.",
        },
    }

    return recommendations.get(experience, {}).get(
        goal, "Извините, у нас нет рекомендаций для вашей комбинации опыта и цели."
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
        model="gpt-3.5-turbo",
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
    user_info["Рекомендация"] = get_recommended_snowboards(
        user_info["Опыт"], user_info["Цель покупки"]
    )

    return json.dumps(user_info, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    snowboard_info = asyncio.run(get_snowboard_info())
    print(snowboard_info)
