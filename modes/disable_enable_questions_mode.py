from simple_term_menu import TerminalMenu
from questions import Question
from utils import (
    clear_screen,
    get_question_by_id,
    update_row_value_based_on_question_id,
)


def show_question_enablement_menu():
    question_id = input("Type question id to change its enablement: ")
    question = get_question_by_id(question_id)
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
        update_row_value_based_on_question_id(question_id, "is_active", not is_enabled)
    elif selected_type == options[1]:
        return
