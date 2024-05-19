from enum import Enum
from typing import Iterable
from simple_term_menu import TerminalMenu
import csv
import os


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
            raise ValueError("Question must be a string")
        self._question = question

    @property
    def answers(self):
        return self._answers

    @answers.setter
    def answers(self, answers: Iterable[str]):
        if not isinstance(answers, (list, tuple)):
            raise ValueError("Answers must be a list or a tuple")
        if self.question_type == QuestionType.QUIZ and len(answers) < 2:
            raise ValueError("For quiz questions, there must be at least 2 answers")
        self._answers = answers


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

        add_question(selected_type)


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def add_question(question_type):
    questions = []
    while True:
        user_question = input(
            f"Enter {question_type.value} (type 'exit' to save your question and go back to the questions menu ↵): "
        )
        if user_question.strip().lower() == "exit":
            break

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

        question = Question(question_type, user_question, answers)
        questions.append(question)
    write_questions_to_file(questions)


def write_questions_to_file(questions):
    file_path = "data/questions.csv"
    is_file_exists = os.path.isfile(file_path)

    max_id = 0
    if is_file_exists:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row_id = int(row["id"])
                if row_id > max_id:
                    max_id = row_id

    with open(file_path, "a") as file:
        header = ["id", "question_type", "question", "answers"]
        writer = csv.DictWriter(file, fieldnames=header)

        if not is_file_exists:
            writer.writeheader()

        for i, question in enumerate(questions, start=1):
            writer.writerow(
                {
                    "id": max_id + i,
                    "question_type": question.question_type.value,
                    "question": question.question,
                    "answers": question.answers,
                }
            )


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
