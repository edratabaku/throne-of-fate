'''
Main game
'''

import pygame
from ai.ollama_ai import generate_scenario
from ai.stable_diffusion import generate_character_image, generate_map
from game_logic.game_state import GameState
from game_logic.events import process_choice
from ui.pygame_ui import draw_ui
from config import SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Throne of Fate")

font = pygame.font.SysFont('Arial', 24)
option_font = pygame.font.SysFont('Arial', 22)

# Input box variables
input_box = pygame.Rect(150, 250, 500, 40)
input_text = ""
active_input = False
start_game = False

# Button
button_rect = pygame.Rect(320, 320, 160, 50)
button_color = (0, 128, 255)

# Initialize game state
game = GameState()

def update_scenario():
    return generate_scenario(game.economy, game.military, game.public_appeal, game.diplomacy)

# Function to draw text with black border for readability
def draw_text_with_border(screen, text, font, color, x, y):
    """Draw text with a black border around it for readability."""
    text_surface = font.render(text, True, color)
    border_surface = font.render(text, True, (0, 0, 0))  # Black outline

    # Draw the border (slightly offset in all directions)
    for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
        screen.blit(border_surface, (x + dx, y + dy))

    # Draw the original text
    screen.blit(text_surface, (x, y))


running = True
game_over = False
king_image = None
map_image = None
while running:
    screen.fill((0, 0, 0))  

    if not start_game:
        # Start screen for character description input
        draw_text_with_border(screen, "Describe your emperor's appearance:", font, (255, 255, 255), 150, 200)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        draw_text_with_border(screen, input_text, font, (255, 255, 255), input_box.x + 10, input_box.y + 10)
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text_with_border(screen, "Next", font, (255, 255, 255), button_rect.x + 45, button_rect.y + 10)
        pygame.display.flip()

        # Event handling for text input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active_input = True
                else:
                    active_input = False
                if button_rect.collidepoint(event.pos) and input_text:
                    # Generate king image and start game
                    generate_character_image(input_text, "assets/king.png")
                    map_description = "Map showing 10 made up countries with varied terrain."
                    generate_map(map_description, "assets/map.png")
                    king_image = pygame.image.load("assets/king.png")
                    king_image = pygame.transform.scale(king_image, (150, 150))
                    map_image = pygame.image.load("assets/map.png")
                    map_image = pygame.transform.scale(map_image, ((SCREEN_WIDTH // 2) - 30, SCREEN_HEIGHT // 2))  # Resize the map
                    scenario_prompt, options = update_scenario()
                    start_game = True
            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    else:
        if not game_over:
            # Game main screen
           # Game main screen
            screen.fill((0, 0, 0))  # Clear screen with black background

            # Draw the map image at a specific position (e.g., top-right corner)
            map_x, map_y = SCREEN_WIDTH // 2, 0
            screen.blit(map_image, (map_x, map_y))

            # Draw the king image at the top-left corner
            king_x, king_y = 20, 20
            screen.blit(king_image, (king_x, king_y))

            # Draw game stats below the king
            stats_text = f"Economy: {game.economy} | Military: {game.military}"
            draw_text_with_border(screen, stats_text, font, (255, 255, 255), king_x, king_y + 160)
            stats_text = f"Public Appeal: {game.public_appeal} | Diplomacy: {game.diplomacy}"
            draw_text_with_border(screen, stats_text, font, (255, 255, 255), king_x, king_y + 190)
            # Draw the scenario prompt and options on the left side below the map
            text_x, text_y = 20, SCREEN_HEIGHT // 2 + 20
            draw_text_with_border(screen, scenario_prompt, font, (255, 255, 255), text_x, text_y)
            option_y = text_y + 50  
            for i, option in enumerate(options):
                draw_text_with_border(screen, f"{i+1}. {option['text']}", option_font, (255, 255, 255), text_x, option_y)
                option_y += 30  

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                        choice_index = int(chr(event.key)) - 1 
                        process_choice(game, choice_index, options)

                        if game.economy <= 0 or game.military <= 0 or game.public_appeal <= 0 or game.diplomacy <= 0:
                            game_over = True
                        else:
                            scenario_prompt, options = update_scenario()
        else:
            # Game Over Screen
            screen.fill((0, 0, 0))
            draw_text_with_border(screen, "Game Over! Your rule has ended.", font, (255, 0, 0), 250, 250)
            draw_text_with_border(screen, "Press R to restart or Q to quit.", font, (255, 255, 255), 220, 300)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game = GameState()
                        scenario_prompt, options = update_scenario()
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False


pygame.quit()