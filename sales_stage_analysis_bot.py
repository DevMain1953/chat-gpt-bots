import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()


async_client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def get_answer_from_target_client_about_dialogue_continuation(
    current_stage: str, dialogue: str
) -> str:
    """
    Returns text of answer from target client about dialogue continuation.

    :param current_stage: Current stage of sales.
    :type current_stage: str

    :param dialogue: Dialogue with target client.
    :type dialogue: str

    :return: A text of answer from target client about dialogue continuation.
    :rtype: str
    """
    response = await async_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты специалист по продажам."},
            {
                "role": "user",
                "content": f"Текущий этап продаж: {current_stage}.\nТекущий диалог:\n{dialogue}\nМожем ли мы двигаться к следующему этапу продаж? Пожалуйста ответьте 'да' или 'нет' и дайте небольшое пояснение.",
            },
        ],
    )
    return response["choices"][0]["message"]["content"]


async def get_sales_stage(stages: list, current_stage: str, dialogue: str) -> str:
    """
    Returns sales stage that depends on client answer.

    :param stages: List of sales stages.
    :type stages: list

    :param current_stage: Current sales stage.
    :type current_stage: str

    :param dialogue: Dialogue with client.
    :type dialogue: str

    :return: A sales stage that depends on client answer.
    :rtype: str
    """
    if current_stage not in stages:
        raise ValueError("Такого этапа продаж нет в списке.")

    current_stage_index = stages.index(current_stage)
    if current_stage_index == len(stages) - 1:
        return "Текущий этап продаж является последним в списке."

    client_answer = await get_answer_from_target_client_about_dialogue_continuation(
        current_stage, dialogue
    )
    if "yes" in client_answer.lower():
        return stages[current_stage_index + 1]
    else:
        return current_stage


if __name__ == "__main__":
    sales_stages = [
        "Первый контакт",
        "Выявление потребностей",
        "Презентация",
        "Обработка возражений",
        "Закрытие сделки",
        "Постпродажное обслуживание",
    ]

    current_stage = "Выявление потребностей"
    dialogue = """
    Клиент: Мы рассматриваем возможность улучшения нашего IT-инфраструктуры.
    Специалист: Хорошо, расскажите, пожалуйста, о текущих проблемах и задачах, которые вы хотите решить.
    Клиент: У нас есть проблемы с масштабируемостью и безопасностью.
    Специалист: Понял вас, мы можем предложить решения, которые помогут вам в этих областях.
    """

    next_stage = asyncio.run(get_sales_stage(sales_stages, current_stage, dialogue))
    print(f"Следующий этап: {next_stage}")
