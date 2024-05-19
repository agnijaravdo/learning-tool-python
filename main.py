from enum import Enum
from simple_term_menu import TerminalMenu
from questions import Question, QuestionType
import csv
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
        elif selected_mode == StartMenuItem.PRACTICE_MODE:
            questions_count = get_number_of_questions()
            if questions_count < 5:
                print(
                    f"\n❗ To select '{StartMenuItem.PRACTICE_MODE.value}' you need to have minimum of 5 questions. Current count of questions is {questions_count}"
                )
            else:
                print("opening practice mode")
        elif selected_mode == StartMenuItem.TEST_MODE:
            questions_count = get_number_of_questions()
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
    print("show statistics")


def get_number_of_questions():
    with open("data/questions.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        questions_count = 0
        for _ in reader:
            questions_count += 1
    return questions_count


def main():
    show_starting_menu()


if __name__ == "__main__":
    main()
