import json

class GameStats:

    def __init__(self,ai_game):
        self.settings = ai_game.settings
        with open("highscores.json", "r") as f:
            data = json.load(f)
        self.high_score = data["high_score"]
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

