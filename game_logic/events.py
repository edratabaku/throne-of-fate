'''
Manage story events
'''

def process_choice(game, choice_index, options):
    selected_option = options[choice_index - 1]  
    effects = selected_option["effects"]

    game.economy += effects["economy"]
    game.military += effects["military"]
    game.public_appeal += effects["public_appeal"]
    game.diplomacy += effects["diplomacy"]

    # Check if any stat is 0 or below to end the game
    if game.economy <= 0 or game.military <= 0 or game.public_appeal <= 0 or game.diplomacy <= 0:
        game.game_over = True