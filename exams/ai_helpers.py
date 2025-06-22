import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def generate_question_from_image_context(context_text, correct_answer):
    prompt = f"""
    На основе следующей информации создай экзаменационный вопрос с 4 вариантами ответов.
    Обязательные требования:
    - Один правильный ответ.
    - Добавь подсказку (hint) по теме.

    Вопрос: {context_text}
    Ответ: {correct_answer}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помощник-преподавателя."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']
