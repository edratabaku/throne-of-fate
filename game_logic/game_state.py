'''
Handle player stats and choices
'''

class GameState:
    def __init__(self):
        self.economy = 50
        self.military = 50
        self.public_appeal = 50
        self.diplomacy = 50
        self.turn = 1
        self.is_alive = True

    def apply_choice(self, economy_change, military_change, public_change, diplomacy_change):
        self.economy += economy_change
        self.military += military_change
        self.public_appeal += public_change
        self.diplomacy += diplomacy_change
        self.turn += 1

        #Game over condition
        if self.economy <= 0 or self.military <= 0 or self.public_appeal <= 0 or self.diplomacy <= 0:
            self.is_alive = False



    