import csv
import os
from simple_term_menu import TerminalMenu

from questions import Question, QuestionType


QUESTIONS_DATA_PATH = "data/questions.csv"


def ask_question(question):
    times_shown = int(question.times_shown)
    correct_answers_percent = question.correct_answers_percent

    if times_shown > 0:
        current_correct_count = (correct_answers_percent / 100) * times_shown
    else:
        current_correct_count = 0

    if question.question_type == QuestionType.QUIZ:
        options = question.answers
        terminal_menu = TerminalMenu(
            options,
            title=f"\n{question.question}\n",
            menu_cursor_style=("fg_green", "bold"),
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index is None:
            return

        user_answer = options[menu_entry_index]
    elif question.question_type == QuestionType.OPEN:
        user_answer = input(f"{question.question} ")

    times_shown += 1
    if user_answer == question.correct_answer:
        print("Correct!")
        current_correct_count += 1
    else:
        print("Incorrect!")

    correct_answers_percent = (current_correct_count / times_shown) * 100
    update_question_statistics_data(question, times_shown, correct_answers_percent)

    return user_answer


def update_question_statistics_data(question, times_shown, correct_answers_percent):
    update_row_value_based_on_question_id(question.id, "times_shown", times_shown)
    update_row_value_based_on_question_id(
        question.id, "correct_answers_percent", correct_answers_percent
    )


def write_questions_to_file(questions):
    is_file_exists = os.path.isfile(QUESTIONS_DATA_PATH)

    max_id = 0
    if is_file_exists:
        with open(QUESTIONS_DATA_PATH, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row_id = int(row["id"])
                if row_id > max_id:
                    max_id = row_id

    with open(QUESTIONS_DATA_PATH, "a") as file:
        header = [
            "id",
            "question_type",
            "question",
            "answers",
            "correct_answer",
            "is_active",
            "times_shown",
            "correct_answers_percent",
        ]
        writer = csv.DictWriter(file, fieldnames=header)

        if not is_file_exists or os.path.getsize(QUESTIONS_DATA_PATH) == 0:
            writer.writeheader()

        for i, question in enumerate(questions, start=1):
            writer.writerow(
                {
                    "id": max_id + i,
                    "question_type": question.question_type.value,
                    "question": question.question,
                    "answers": question.answers,
                    "correct_answer": question.correct_answer,
                    "is_active": str(question.is_active),
                    "times_shown": question.times_shown,
                    "correct_answers_percent": f"{question.correct_answers_percent:.2f}",
                }
            )


def get_all_questions():
    questions = []
    with open(QUESTIONS_DATA_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = Question(
                question_type=QuestionType(row["question_type"]),
                question=row["question"],
                answers=eval(row["answers"]),
                correct_answer=row["correct_answer"],
                is_active=row["is_active"].lower() == "true",
                times_shown=int(row["times_shown"]),
                correct_answers_percent=float(row["correct_answers_percent"]),
            )
            question.id = int(row["id"])
            questions.append(question)
    return questions


def get_question_by_id(question_id):
    with open(QUESTIONS_DATA_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id"] == str(question_id):
                return Question(
                    question_type=QuestionType(row["question_type"]),
                    question=row["question"],
                    answers=eval(row["answers"]),
                    correct_answer=row["correct_answer"],
                    is_active=row["is_active"],
                    times_shown=int(row["times_shown"]),
                    correct_answers_percent=float(row["correct_answers_percent"]),
                )


def update_row_value_based_on_question_id(question_id, column_name, row_new_value):
    temp_rows = []

    with open(QUESTIONS_DATA_PATH, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            temp_rows.append(row)

    for row in temp_rows:
        if int(row["id"]) == int(question_id):
            if column_name == "is_active":
                row[column_name] = str(row_new_value)
            else:
                row[column_name] = (
                    f"{row_new_value:.2f}"
                    if isinstance(row_new_value, float)
                    else str(row_new_value)
                )

    with open(QUESTIONS_DATA_PATH, "w") as file:
        writer = csv.DictWriter(file, fieldnames=temp_rows[0].keys())
        writer.writeheader()
        writer.writerows(temp_rows)


def get_number_of_questions():
    questions = get_all_questions()
    questions_count = len(questions)
    return questions_count


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
