'''
Handles rendering the UI using PyGame
'''

import pygame 
pygame.font.init()

font = pygame.font.Font(None, 28)

def draw_ui(screen, scenario, game):
    text_color = (255,255,255)

    y=50
    for line in scenario.split("\n"):
        render = font.render(line,True,text_color)
        screen.blit(render, (50,y))
        y += 30
    stats_text = f"Economy: {game.economy} Military: {game.military} Public Appeal: {game.public_appeal} Diplomacy: {game.diplomacy}"
    render = font.render(stats_text, True, text_color)
    screen.blit(render, (50,400))

    choice_texts = [
        "1. Choose first option",
        "2. Choose second option",
        "3. Choose third option"
    ]

    y = 450
    for choice in choice_texts:
        render = font.render(choice, True, text_color)
        screen.blit(render, (50,y))
        y+=30