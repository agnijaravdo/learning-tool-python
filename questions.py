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
        self,
        question_type: QuestionType,
        question: str,
        answers: Iterable[str],
        correct_answer: str,
        is_active: bool = True,
        times_shown: int = 0,
        correct_answers_percent: int = 0,
    ):
        self.question_type = question_type
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.is_active = is_active
        self.times_shown = times_shown
        self.correct_answers_percent = correct_answers_percent

    @property
    def question_type(self):
        return self._question_type

    @question_type.setter
    def question_type(self, question_type: QuestionType):
        if not isinstance(question_type, QuestionType):
            raise ValueError("Question type must be an instance of QuestionType")
        self._question_type = question_type

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

    @property
    def correct_answer(self):
        return self._correct_answer

    @correct_answer.setter
    def correct_answer(self, correct_answer: str):
        if correct_answer not in self.answers:
            raise ValueError("Correct answer option should be among all possible answers")
        self._correct_answer = correct_answer

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
                correct_answer = input(f"Enter which one of answers {answers} is the correct one: ")

            elif question_type == QuestionType.OPEN:
                open_question_answer = input("Enter the answer: ")
                correct_answer = open_question_answer
                answers.append(open_question_answer)

            question = Question(question_type, user_question, answers, correct_answer)
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

            if not is_file_exists:
                writer.writeheader()

            for i, question in enumerate(questions, start=1):
                writer.writerow(
                    {
                        "id": max_id + i,
                        "question_type": question.question_type.value,
                        "question": question.question,
                        "answers": question.answers,
                        "correct_answer": question.correct_answer,
                        "is_active": question.is_active,
                        "times_shown": question.times_shown,
                        "correct_answers_percent": question.correct_answers_percent,
                    }
                )

    @staticmethod
    def get_all_questions():
        questions = []
        with open(Question.QUESTIONS_DATA_PATH, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                question = Question(
                    question_type=QuestionType(row["question_type"]),
                    question=row["question"],
                    answers=eval(row["answers"]),
                    correct_answer=row["correct_answer"],
                    is_active=row["is_active"],
                    times_shown=int(row["times_shown"]),
                    correct_answers_percent=int(row["correct_answers_percent"]),
                )
                question.id = int(row["id"])
                questions.append(question)
        return questions

    @staticmethod
    def get_number_of_questions():
        questions = Question.get_all_questions()
        questions_count = len(questions)
        return questions_count

    @staticmethod
    def get_question_by_id(question_id):
        with open(Question.QUESTIONS_DATA_PATH, "r") as file:
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
                        correct_answers_percent=int(row["correct_answers_percent"]),
                    )

    @staticmethod
    def update_enablement_status(enablement_status, question_id):
        temp_rows = []

        with open(Question.QUESTIONS_DATA_PATH, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                temp_rows.append(row)

        for row in temp_rows:
            if int(row["id"]) == int(question_id):
                row["is_active"] = "False" if enablement_status else "True"

        with open(Question.QUESTIONS_DATA_PATH, "w") as file:
            writer = csv.DictWriter(file, fieldnames=temp_rows[0].keys())
            writer.writeheader()
            writer.writerows(temp_rows)

        print(
            f"Question with id {question_id} has been successfully {'disabled' if enablement_status else 'enabled'}"
        )
