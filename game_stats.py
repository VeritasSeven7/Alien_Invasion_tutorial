from pathlib import Path

class GameStats:
    # class for tracking statistics

    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0

        # load high score
        self._load_hs()
        self.high_score = self.loaded_score
        self.level = 1

    def _load_hs(self):
        self.score_path = Path('assets/high score.txt')
        self.loaded_score = int(self.score_path.read_text().rstrip())
