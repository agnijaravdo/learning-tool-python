import pytest
from questions import Question, QuestionType


def test_question_init():
    question = Question(
        QuestionType.OPEN, "What is the chemical symbol for water?", ["H2O"], "H2O"
    )
    assert question.question == "What is the chemical symbol for water?"
    assert question.correct_answer == "H2O"
    assert question.question_type == QuestionType.OPEN
    assert question.is_active == True
    assert question.correct_answers_percent == 0.0


def test_incorrect_question_type():
    with pytest.raises(ValueError):
        Question("Open", "What is the chemical symbol for water?", ["H2O"], "H2O")


def test_incorrect_answers_type():
    with pytest.raises(ValueError):
        Question(
            QuestionType.OPEN, "What is the chemical symbol for water?", "H2O", "H2O"
        )


def test_quiz_question_with_less_than_two_answers():
    with pytest.raises(ValueError):
        Question(
            QuestionType.QUIZ, "What is the chemical symbol for water?", ["H2O"], "H2O"
        )


def test_correct_answer_not_in_answers():
    with pytest.raises(ValueError):
        Question(
            QuestionType.QUIZ,
            "What is the chemical symbol for water?",
            ["H2O", "H2O2"],
            "H2O3",
        )


def test_question_answer_setter():
    question = Question(
        QuestionType.QUIZ,
        "What is the chemical symbol for water?",
        ["H2O", "H2O2"],
        "H2O",
    )
    question.correct_answer = "H2O2"
    assert question.correct_answer == "H2O2"
