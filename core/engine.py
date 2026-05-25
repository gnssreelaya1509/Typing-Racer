import random

class TypingEngine:
    def __init__(self):
        self.modes = {
            "Small": ["Python is fun.", "Code your dream.", "Stay focused."],
            "Alphabet": ["abcdefghijklmnopqrstuvwxyz"],
            "Large": [
                "Flet is a framework that allows you to build desktop web and mobile apps in python with ease and speed.",
                "Programming requires patience and constant practice to master the underlying logic.",
                "Smart energy harvesting systems represent a breakthrough in sustainable technological development."
            ]
        }
        self.target_text = ""

    def start_game(self, mode):
        # Picks a random paragraph based on the mode
        self.target_text = random.choice(self.modes.get(mode, ["Default text"]))
        return self.target_text

    def calculate_results(self, user_text):
        errors = 0
        u_words = user_text.split()
        t_words = self.target_text.split()
        for i in range(min(len(u_words), len(t_words))):
            if u_words[i] != t_words[i]:
                errors += 1
        return errors + abs(len(u_words) - len(t_words))