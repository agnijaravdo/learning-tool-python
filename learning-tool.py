from enum import Enum
from typing import Iterable
from simple_term_menu import TerminalMenu


class QuestionType(Enum):
    QUIZ = "Quiz Question"
    OPEN = "Open Question"
    BACK = "Go Back To The Main Menu ↵"


class StartMenuItem(Enum):
    ADD_QUESTIONS = "Add Questions"
    VIEW_STATISTICS = "View Statistics"
    DISABLE_ENABLE_QUESTIONS = "Disable/Enable Questions"
    PRACTICE_MODE = "Practice Mode"
    TEST_MODE = "Test Mode"


class Question:
    def __init__(
        self, question_type: QuestionType, question: str, answers: Iterable[str]
    ):
        self.question_type = question_type
        self.question = question
        self.answers = answers

    def __str__(self):
        return f"{self.question_type.value}: '{self.question}' with answer(s) {self.answers}"

    @property
    def question_type(self):
        return self._question_type

    @question_type.setter
    def question_type(self, question_type: QuestionType):
        if not isinstance(question_type, QuestionType):
            raise ValueError("Question type must be an instance of QuestionType")
        self._question_type = question_type

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, question):
        if not isinstance(question, str):
            raise ValueError("Question must be a string.")
        self._question = question

    @property
    def answers(self):
        return self._answers

    @answers.setter
    def answers(self, answers: Iterable[str]):
        if not isinstance(answers, (list, tuple)):
            raise ValueError("Answers must be a list or a tuple.")
        if self.question_type == QuestionType.QUIZ and len(answers) < 2:
            raise ValueError("For quiz questions, there must be at least 2 answers.")
        self._answers = answers


def show_starting_menu():
    while True:
        options = [item.value for item in StartMenuItem]
        terminal_menu = TerminalMenu(
            options,
            title="\nUse ↓ or ↑ arrow keys to navigate and 'Enter' to select:\n",
            menu_cursor_style=("fg_green", "bold"),
        )
        menu_entry_index = terminal_menu.show()
        if StartMenuItem(options[menu_entry_index]) == StartMenuItem.ADD_QUESTIONS:
            show_select_question_type_menu()


def show_select_question_type_menu():
    while True:
        options = [question.value for question in QuestionType]
        terminal_menu = TerminalMenu(
            options,
            title="\nUse ↓ or ↑ arrow keys to navigate and 'Enter' to select the question type you want to add:\n",
            menu_cursor_style=("fg_green", "bold"),
        )
        menu_entry_index = terminal_menu.show()
        selected_type = QuestionType(options[menu_entry_index])

        if selected_type == QuestionType.BACK:
            return

        add_question(selected_type)


def add_question(question_type):
    while True:
        question = input(
            f"Enter {question_type.value} (type 'exit' to go back to the questions menu ↵): "
        )
        if question.strip().lower() == "exit":
            return

        answers = []
        if question_type == QuestionType.QUIZ:
            while True:
                quiz_question_answer = input(
                    "Enter one of the possible answers (type 'done' to finish adding answer): "
                )
                if quiz_question_answer.strip().lower() == "done":
                    break
                answers.append(quiz_question_answer)

            if len(answers) < 2:
                print("A quiz question requires minimum of 2 answers. Add more answers")
                continue
        elif question_type == QuestionType.OPEN:
            open_question_answer = input("Enter the answer: ")
            answers.append(open_question_answer)

        question = Question(question_type, question, answers)
        print(question)


def main():
    show_starting_menu()


if __name__ == "__main__":
    main()
