from enum import Enum
from simple_term_menu import TerminalMenu
from modes.add_questions_mode import show_select_question_type_menu
from modes.disable_enable_questions_mode import show_question_enablement_menu
from modes.practice_mode import start_practice_mode
from modes.test_mode import open_test_mode
from modes.view_statistics_mode import show_statistics
from utils import clear_screen, get_number_of_questions


class StartMenuItem(Enum):
    ADD_QUESTIONS = "Add Questions"
    VIEW_STATISTICS = "View Statistics"
    DISABLE_ENABLE_QUESTIONS = "Disable/Enable Questions"
    PRACTICE_MODE = "Practice Mode"
    TEST_MODE = "Test Mode"


def show_mode_selection_menu():
    while True:
        options = [item.value for item in StartMenuItem]
        terminal_menu = TerminalMenu(
            options,
            title="\nℹ️ Use ↓ or ↑ arrow keys to navigate and 'Enter' to select:\n",
            menu_cursor_style=("fg_green", "bold"),
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == None:
            return

        selected_mode = StartMenuItem(options[menu_entry_index])
        questions_count = get_number_of_questions()

        clear_screen()
        if selected_mode == StartMenuItem.ADD_QUESTIONS:
            show_select_question_type_menu()
        if selected_mode == StartMenuItem.VIEW_STATISTICS:
            validate_questions_count(questions_count, selected_mode, 1, show_statistics)
        if selected_mode == StartMenuItem.DISABLE_ENABLE_QUESTIONS:
            validate_questions_count(
                questions_count, selected_mode, 1, show_question_enablement_menu
            )
        elif selected_mode == StartMenuItem.PRACTICE_MODE:
            validate_questions_count(
                questions_count, selected_mode, 5, start_practice_mode
            )
        elif selected_mode == StartMenuItem.TEST_MODE:
            validate_questions_count(questions_count, selected_mode, 5, open_test_mode)


def validate_questions_count(
    questions_count, selected_mode, min_questions, function_name
):
    if questions_count < min_questions:
        print(
            f"\n❗ To select '{selected_mode.value}' you need to have minimum of {min_questions} questions. Current count of questions is {questions_count}"
        )
    else:
        function_name()
