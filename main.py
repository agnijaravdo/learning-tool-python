from enum import Enum
import random
from simple_term_menu import TerminalMenu
from tabulate import tabulate
from questions import Question, QuestionType
import os


class StartMenuItem(Enum):
    ADD_QUESTIONS = "Add Questions"
    VIEW_STATISTICS = "View Statistics"
    DISABLE_ENABLE_QUESTIONS = "Disable/Enable Questions"
    PRACTICE_MODE = "Practice Mode"
    TEST_MODE = "Test Mode"


def show_starting_menu():
    while True:
        options = [item.value for item in StartMenuItem]
        terminal_menu = TerminalMenu(
            options,
            title="\nℹ️ Use ↓ or ↑ arrow keys to navigate and 'Enter' to select:\n",
            menu_cursor_style=("fg_green", "bold"),
        )
        menu_entry_index = terminal_menu.show()
        selected_mode = StartMenuItem(options[menu_entry_index])

        clear_screen()
        if selected_mode == StartMenuItem.ADD_QUESTIONS:
            show_select_question_type_menu()
        if selected_mode == StartMenuItem.VIEW_STATISTICS:
            show_statistics()
        if selected_mode == StartMenuItem.DISABLE_ENABLE_QUESTIONS:
            show_question_enablement_menu()
        elif selected_mode == StartMenuItem.PRACTICE_MODE:
            questions_count = Question.get_number_of_questions()
            if questions_count < 5:
                print(
                    f"\n❗ To select '{StartMenuItem.PRACTICE_MODE.value}' you need to have minimum of 5 questions. Current count of questions is {questions_count}"
                )
            else:
                start_practice_mode()
        elif selected_mode == StartMenuItem.TEST_MODE:
            questions_count = Question.get_number_of_questions()
            if questions_count < 5:
                print(
                    f"\n❗ To select '{StartMenuItem.TEST_MODE.value}' you need to have minimum of 5 questions. Current count of questions is {questions_count}"
                )
            else:
                print("opening test mode")


def show_select_question_type_menu():
    while True:
        options = [question.value for question in QuestionType]
        terminal_menu = TerminalMenu(
            options,
            title="\nℹ️ Use ↓ or ↑ arrow keys to navigate and 'Enter' to select the question type you want to add:\n",
            menu_cursor_style=("fg_green", "bold"),
        )
        menu_entry_index = terminal_menu.show()
        selected_type = QuestionType(options[menu_entry_index])

        if selected_type == QuestionType.BACK:
            return

        Question.add_question(selected_type)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_statistics():
    questions = Question.get_all_questions()

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


def show_question_enablement_menu():
    question_id = input("Type question id to change its enablement: ")
    question = Question.get_question_by_id(question_id)
    is_enabled = question.is_active.lower() == "true"
    enablement_status_to_change = "DISABLED" if is_enabled else "ENABLED"
    print(
        f"Selected question: '{question.question}' with answers: '{', '.join(question.answers)}' and current enablement status: '{question.is_active}'"
    )

    options = [
        f"Change question '{question.question}' enablement status to '{enablement_status_to_change}'",
        "Go Back To The Main Menu ↵",
    ]
    terminal_menu = TerminalMenu(
        options,
        title="\nℹ️ Use ↓ or ↑ arrow keys to navigate and 'Enter' to select the question type you want to add:\n",
        menu_cursor_style=("fg_green", "bold"),
    )
    menu_entry_index = terminal_menu.show()
    selected_type = options[menu_entry_index]

    clear_screen()
    if selected_type == options[0]:
        Question.update_row_value_based_on_question_id(
            question_id, "is_active", not is_enabled
        )
    elif selected_type == options[1]:
        return


def start_practice_mode():

    while True:
        questions = Question.get_all_questions()
        random_question = get_weighted_random_question(questions)

        times_shown = int(random_question.times_shown)
        correct_answers_percent = random_question.correct_answers_percent

        if times_shown > 0:
            current_correct_count = (correct_answers_percent / 100) * times_shown
        else:
            current_correct_count = 0

        if random_question.question_type == QuestionType.QUIZ:
            practice_answer = input(
                f"{random_question.question} Possible answers to choose: {random_question.answers}: "
            )

            if practice_answer == random_question.correct_answer:
                print("Correct!")
                current_correct_count += 1
            else:
                print("Incorrect!")

        elif random_question.question_type == QuestionType.OPEN:
            practice_answer = input(f"{random_question.question} ")

            if practice_answer == random_question.correct_answer:
                print("Correct!")
                current_correct_count += 1
            else:
                print("Incorrect!")

        times_shown += 1

        correct_answers_percent = (current_correct_count / times_shown) * 100

        Question.update_row_value_based_on_question_id(
            random_question.id, "times_shown", times_shown
        )
        Question.update_row_value_based_on_question_id(
            random_question.id, "correct_answers_percent", correct_answers_percent
        )


def get_weighted_random_question(questions):
    enabled_questions = [question for question in questions if question.is_active]

    weight = [
        100.00 - (question.correct_answers_percent) for question in enabled_questions
    ]
    random_question = random.choices(
        enabled_questions, weights=weight, k=len(enabled_questions)
    )[0]
    return random_question


def main():
    show_starting_menu()


if __name__ == "__main__":
    main()
