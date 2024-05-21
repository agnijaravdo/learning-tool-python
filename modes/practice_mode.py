import random
from utils import ask_question, clear_screen, get_all_questions


def start_practice_mode():
    print("---------- Welcome to practice mode. Press 'Ctrl + C' to exit ----------\n")
    while True:
        try:
            questions = get_all_questions()
            random_question = get_weighted_random_question(questions)
            ask_question(random_question)
        except KeyboardInterrupt:
            clear_screen()
            return


def get_weighted_random_question(questions):
    enabled_questions = [question for question in questions if question.is_active]

    weight = [
        100.00 - (question.correct_answers_percent) for question in enabled_questions
    ]
    random_question = random.choices(
        enabled_questions, weights=weight, k=len(enabled_questions)
    )[0]
    return random_question
