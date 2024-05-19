import csv
from enum import Enum
import os
from typing import Iterable


class QuestionType(Enum):
    QUIZ = "Quiz Question"
    OPEN = "Open Question"
    BACK = "Go Back To The Main Menu ↵"


class Question:
    QUESTIONS_DATA_PATH = "data/questions.csv"

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

    @staticmethod
    def add_question(question_type: QuestionType):
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
                    print(
                        "A quiz question requires minimum of 2 answers. Add more answers"
                    )
                    continue
            elif question_type == QuestionType.OPEN:
                open_question_answer = input("Enter the answer: ")
                answers.append(open_question_answer)

            question = Question(question_type, user_question, answers)
            questions.append(question)
        Question.write_questions_to_file(questions)

    @staticmethod
    def write_questions_to_file(questions):
        is_file_exists = os.path.isfile(Question.QUESTIONS_DATA_PATH)

        max_id = 0
        if is_file_exists:
            with open(Question.QUESTIONS_DATA_PATH, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row_id = int(row["id"])
                    if row_id > max_id:
                        max_id = row_id

        with open(Question.QUESTIONS_DATA_PATH, "a") as file:
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
