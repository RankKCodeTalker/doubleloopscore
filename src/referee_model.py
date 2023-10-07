import requests
from src.config import glm_api
from src.global_var import input_template, output_options


def call_glm(prompt: str) -> str:
    lock = True
    while lock:
        try:
            response = requests.post(
                url=glm_api,
                json={
                    "prompt": prompt
                }
            )
            model_response = response.text
            lock = False
        except Exception as e:
            print(e)
    return model_response

def get_prompt(question: str, answer1: str, answer2: str):
    return input_template.format(
        question=question,
        answer1=answer1,
        answer2=answer2
    )

def get_result(model_response: str) -> int:
    """
    0 -> answer1 win
    1 -> answer2 win
    2 -> draw
    """
    for i in range(len(output_options)):
        if model_response == output_options:
            return i
    for i in range(len(output_options)):
        if model_response.startswith(output_options[i]):
            return i
    num_key_words = [model_response.count("1"), model_response.count("2"), model_response.count("一样")]
    if num_key_words[0] > num_key_words[1] and num_key_words[0] > num_key_words[2]:
        return 0
    if num_key_words[1] > num_key_words[0] and num_key_words[1] > num_key_words[2]:
        return 1
    return 2

def get_result_direct(question: str, answer1: str, answer2: str) -> int:
    """
    0 -> answer1 win
    1 -> answer2 win
    2 -> draw
    """
    prompt = get_prompt(question, answer1, answer2)
    model_response = call_glm(prompt)
    for i in range(len(output_options)):
        if model_response == output_options:
            return i
    for i in range(len(output_options)):
        if model_response.startswith(output_options[i]):
            return i
    num_key_words = [model_response.count("1"), model_response.count("2"), model_response.count("一样")]
    if num_key_words[0] > num_key_words[1] and num_key_words[0] > num_key_words[2]:
        return 0
    if num_key_words[1] > num_key_words[0] and num_key_words[1] > num_key_words[2]:
        return 1
    return 2

