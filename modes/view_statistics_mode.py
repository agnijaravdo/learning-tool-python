from tabulate import tabulate
from utils import get_all_questions


def show_statistics():
    questions = get_all_questions()

    table = []
    for question in questions:
        row = [
            question.id,
            question.question_type.value,
            question.question,
            ", ".join(map(str, question.answers)),
            question.correct_answer,
            question.is_active,
            question.times_shown,
            question.correct_answers_percent,
        ]
        table.append(row)

    headers = [
        "ID",
        "Type",
        "Question",
        "Answers",
        "Correct One",
        "Is Active",
        "Times Shown",
        "Correctly answered %",
    ]
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            maxcolwidths=[None, None, 40, 40, None, None, None, None],
        )
    )
