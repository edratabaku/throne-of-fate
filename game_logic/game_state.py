"""
Handle player stats and choices
"""


class GameState:
    def __init__(self, economy=50, military=50, public_appeal=50, diplomacy=50):
        self.economy = economy
        self.military = military
        self.public_appeal = public_appeal
        self.diplomacy = diplomacy
        self.turn = 1  # Turn counter
        self.is_alive = True

    def apply_choice(self, chosen_option):

        economy_change = chosen_option["effects"].get("economy", 0)
        military_change = chosen_option["effects"].get("military", 0)
        public_change = chosen_option["effects"].get("public_appeal", 0)
        diplomacy_change = chosen_option["effects"].get("diplomacy", 0)

        self.economy += economy_change
        self.military += military_change
        self.public_appeal += public_change
        self.diplomacy += diplomacy_change
        self.turn += 1

        # Game over condition
        if (
            self.economy <= 0
            or self.military <= 0
            or self.public_appeal <= 0
            or self.diplomacy <= 0
        ):
            self.is_alive = False
