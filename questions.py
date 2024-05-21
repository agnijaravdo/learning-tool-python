from enum import Enum
from typing import Iterable


class QuestionType(Enum):
    QUIZ = "Quiz Question"
    OPEN = "Open Question"
    BACK = "Go Back To The Main Menu ↵"


class Question:
    def __init__(
        self,
        question_type: QuestionType,
        question: str,
        answers: Iterable[str],
        correct_answer: str,
        is_active: bool = True,
        times_shown: int = 0,
        correct_answers_percent: float = 0.00,
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
            raise ValueError(
                "Correct answer option should be among all possible answers"
            )
        self._correct_answer = correct_answer

    @staticmethod
    def add_questions(question_type: QuestionType):
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
                        "A quiz question requires a minimum of 2 answers. Add more answers"
                    )
                    continue
                correct_answer = input(
                    f"Enter which one of the answers {answers} is the correct one: "
                )

            elif question_type == QuestionType.OPEN:
                open_question_answer = input("Enter the answer: ")
                correct_answer = open_question_answer
                answers.append(open_question_answer)

            question = Question(question_type, user_question, answers, correct_answer)
            questions.append(question)
        return questions
