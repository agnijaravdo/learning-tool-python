import csv
from enum import Enum
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
                print("opening practice mode")
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
            question.is_active,
            question.times_shown,
            question.correct_answers,
        ]
        table.append(row)

    headers = [
        "ID",
        "Type",
        "Question",
        "Answers",
        "Is Active",
        "Times Shown",
        "Correct Answers",
    ]
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            maxcolwidths=[None, None, 80, 60, None, None, None],
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
        Question.update_enablement_status(is_enabled, question_id)
    elif selected_type == options[1]:
        return


def main():
    show_starting_menu()


if __name__ == "__main__":
    main()
