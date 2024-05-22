import random
from score import Score
from utils import ask_question, clear_screen, get_all_questions, get_number_of_questions


def open_test_mode():
    possible_number_of_questions = get_number_of_questions()
    while True:
        questions_count = input(
            "How many questions do you want to appear in the test? "
        )

        if not questions_count.isdigit():
            print("Enter a valid number")
            continue
        elif int(questions_count) > possible_number_of_questions:
            print(
                f"Provided number of questions is greater than the number of available questions. Available questions count is: {possible_number_of_questions}"
            )
            continue
        elif int(questions_count) < 5:
            print("Test mode requires minimum of 5 questions")
            continue
        else:
            break

    try:
        possible_questions = get_all_questions()
        enabled_questions = [
            question for question in possible_questions if question.is_active
        ]
        sampled_questions = random.sample(enabled_questions, int(questions_count))
    except ValueError:
        print(
            f"Not enough questions to sample. Possible sample count is {len(enabled_questions)}"
        )
        return

    start_test_mode(int(questions_count), sampled_questions)


def start_test_mode(questions_count, sampled_questions):
    print("\n---------- Welcome to test mode. Press 'Ctrl + C' to exit ----------\n")
    user_score = 0

    try:
        for question_index, question in enumerate(sampled_questions, start=1):
            print(f"{question_index}.", end=" ")
            if ask_question(question) == question.correct_answer:
                user_score += 1

        score_percentage = f"{(float(user_score) / questions_count * 100):.2f}%"
        print(f"Your score is {score_percentage}")
        user_name = input("Enter your name to save score: ")
        score = Score(user_name, score_percentage)
        score.save_score_to_file(score)

    except KeyboardInterrupt:
        clear_screen()
        return
