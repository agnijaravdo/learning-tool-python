from datetime import datetime


class Score:
    def __init__(self, user_name, score):
        self.name = user_name
        self.score = score
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.time = datetime.now().strftime("%H:%M:%S")     

    def __str__(self):
        return f"Name: {self.name}, Score: {self.score}, Date: {self.date}, Time: {self.time}"
    
    @staticmethod
    def save_score_to_file(score):
        with open("data/results.txt", "a", newline="") as file:
            file.write(str(score))
