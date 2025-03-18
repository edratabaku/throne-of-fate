"""
Main game
"""

import pygame
from ai.ollama_ai import generate_scenario
from ai.stable_diffusion import generate_image
from game_logic.game_state import GameState
import threading

from config import SCREEN_HEIGHT, SCREEN_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Throne of Fate")
        self.font = pygame.font.SysFont("Arial", 24)
        self.option_font = pygame.font.SysFont("Arial", 22)
        self.input_box = pygame.Rect(150, 250, 500, 40)
        self.input_text = ""
        self.active_input = False
        self.start_game = False
        self.button_rect = pygame.Rect(320, 320, 160, 50)
        self.button_color = (0, 128, 255)
        self.game_state = GameState()
        self.king_image = None
        self.map_image = None
        self.running = False
        self.game_over = False
        self.win = False
        self.scenario_index = 0
        self.max_scenarios = 15  # Total number of scenarios
        self.scenarios = []  # Store pre-generated scenarios

        self.reuse_player_image = False
        self.reuse_map_image = True #Use map.png image to reduce waiting time

        self.scenario_prompt, self.options = None, None
        self.loading_character = False
        self.loading_map = False
        self.loading_scenario = False
        self.image_generation_tread = None
        self.scenario_generation_tread = None

        self.generate_scenarios()
    
    def generate_scenarios(self):
        """Pre-generate 15 scenarios before the game starts."""
        for _ in range(self.max_scenarios):
            scenario, options = generate_scenario(
                self.game_state.economy,
                self.game_state.military,
                self.game_state.public_appeal,
                self.game_state.diplomacy,
                False,
            )
            self.scenarios.append((scenario, options))
        self.scenario_prompt, self.options = self.scenarios[0]
    
    def _generate_images_thread(
        self, player_description, map_description, reuse_player_image, reuse_map_image
    ):
        print("Generating character image")
        if not reuse_player_image:
            generate_image(player_description, "assets/king.png")
        self.king_image = pygame.image.load("assets/king.png")
        self.king_image = pygame.transform.scale(self.king_image, (150, 150))
        self.loading_character = False

        print("Generating map image")
        if not reuse_map_image:
            generate_image(map_description, "assets/map.png")
        self.map_image = pygame.image.load("assets/map.png")
        self.map_image = pygame.transform.scale(
            self.map_image, ((SCREEN_WIDTH // 2) - 30, SCREEN_HEIGHT // 2)
        )  # Resize the map
        self.loading_map = False

    def generate_images(
        self,
        player_description,
        map_description,
        reuse_player_image=False,
        reuse_map_image=False,
    ):
        self.loading_map = True
        self.loading_character = True
        self.image_generation_thread = threading.Thread(
            target=self._generate_images_thread,
            args=(
                player_description,
                map_description,
                reuse_player_image,
                reuse_map_image,
            ),
        )
        self.image_generation_thread.start()

    def _generate_player_image_thread(self, player_description):
        print("Generating character image", player_description)
        generate_image(player_description, "assets/king.png")
        self.king_image = pygame.image.load("assets/king.png")
        self.king_image = pygame.transform.scale(self.king_image, (150, 150))
        self.loading_character = False

    def generate_player_image(self, player_description):
        self.loading_character = True
        self.player_image_generation_thread = threading.Thread(
            target=self._generate_player_image_thread, args=(player_description,)
        )
        self.player_image_generation_thread.start()

    def _generate_map_image_thread(self, map_description):
        print("Generating map image", map_description)
        generate_image(map_description, "assets/map.png")
        self.map_image = pygame.image.load("assets/map.png")
        self.map_image = pygame.transform.scale(
            self.map_image, ((SCREEN_WIDTH // 2) - 30, SCREEN_HEIGHT // 2)
        )  # Resize the map
        self.loading_map = False

    def generate_map_image(self, map_description):
        self.loading_map = True
        self.map_image_generation_thread = threading.Thread(
            target=self._generate_map_image_thread, args=(map_description,)
        )
        self.map_image_generation_thread.start()

    def update_scenario(self):
        self.loading_scenario = True
        self.scenario_generation_tread = threading.Thread(
            target=self._update_scenario_thread
        )
        self.scenario_generation_tread.start()

    def _update_scenario_thread(self):
        """Moves to the next scenario or ends the game if necessary."""
        if self.scenario_index < self.max_scenarios - 1:
            self.scenario_index += 1
            self.scenario_prompt, self.options = self.scenarios[self.scenario_index]
        else:
            self.win = True  # Win condition met
            self.game_over = True
        self.loading_scenario = False

    def draw_loading_screen(self):
        # print('Drawing loading screen')
        self.screen.fill((0, 0, 0))  # Clear screen with black background
        self.draw_text_with_border(
            self.screen,
            "Loading...",
            self.font,
            (255, 255, 255),
            SCREEN_WIDTH // 2 - 50,
            SCREEN_HEIGHT // 2,
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        pygame.display.flip()

    # Function to draw text with black border for readability
    def draw_text_with_border(self, screen, text, font, color, x, y):
        """Draw text with a black border around it for readability."""
        text_surface = font.render(text, True, color)
        border_surface = font.render(text, True, (0, 0, 0))  # Black outline

        # Draw the border (slightly offset in all directions)
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            screen.blit(border_surface, (x + dx, y + dy))

        # Draw the original text
        screen.blit(text_surface, (x, y))

    def draw_initial_ui(self):
        # print('Drawing initial UI')
        self.draw_text_with_border(
            self.screen,
            "Describe your emperor's appearance:",
            self.font,
            (255, 255, 255),
            150,
            200,
        )
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box, 2)
        self.draw_text_with_border(
            self.screen,
            self.input_text,
            self.font,
            (255, 255, 255),
            self.input_box.x + 10,
            self.input_box.y + 10,
        )
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        self.draw_text_with_border(
            self.screen,
            "Next",
            self.font,
            (255, 255, 255),
            self.button_rect.x + 45,
            self.button_rect.y + 10,
        )
        pygame.display.flip()

        # Event handling for text input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active_input = True
                else:
                    self.active_input = False
                if self.button_rect.collidepoint(event.pos) and self.input_text:
                    self.map_description = (
                        "Map showing 10 made up countries with varied terrain."
                    )
                    self.generate_images(
                        self.input_text,
                        self.map_description,
                        self.reuse_player_image,
                        self.reuse_map_image,
                    )
                    # self.scenario_prompt, self.options = self.update_scenario()
                    self.update_scenario()
                    self.start_game = True
            if event.type == pygame.KEYDOWN and self.active_input:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

    def draw_main_screen(self):
        # print('Drawing main screen')
        # Game main screen
        self.screen.fill((0, 0, 0))  # Clear screen with black background

        # Draw the map image at a specific position (e.g., top-right corner)
        map_x, map_y = SCREEN_WIDTH // 2, 0
        self.screen.blit(self.map_image, (map_x, map_y))

        # Draw the king image at the top-left corner
        king_x, king_y = 20, 20
        self.screen.blit(self.king_image, (king_x, king_y))

        # Draw game stats below the king
        stats_text = (
            f"Economy: {self.game_state.economy} | Military: {self.game_state.military}"
        )
        self.draw_text_with_border(
            self.screen, stats_text, self.font, (255, 255, 255), king_x, king_y + 160
        )
        stats_text = f"Public Appeal: {self.game_state.public_appeal} | Diplomacy: {self.game_state.diplomacy}"
        self.draw_text_with_border(
            self.screen, stats_text, self.font, (255, 255, 255), king_x, king_y + 190
        )
        # Draw the scenario prompt and options on the left side below the map
        text_x, text_y = 20, SCREEN_HEIGHT // 2 + 20
        self.draw_text_with_border(
            self.screen,
            self.scenario_prompt,
            self.font,
            (255, 255, 255),
            text_x,
            text_y,
        )
        option_y = text_y + 50
        for i, option in enumerate(self.options):
            self.draw_text_with_border(
                self.screen,
                f"{i+1}. {option['text']}",
                self.option_font,
                (255, 255, 255),
                text_x,
                option_y,
            )
            option_y += 30

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    choice_index = int(chr(event.key)) - 1
                    selected_option = self.options[choice_index - 1]
                    self.game_state.apply_choice(selected_option)

                    if not self.game_state.is_alive:
                        self.game_over = True
                    else:
                        # self.scenario_prompt, self.options = self.update_scenario()
                        self.update_scenario()

    def draw_game_over_screen(self):
        """Handles game over screen for both loss and win cases."""
        self.screen.fill((0, 0, 0))
        # First message (Game Over / Win message)
        message = "You won! Your reign was successful." if self.win else "Game Over! Your rule has ended."
        text_surface1 = self.font.render(message, True, (255, 0, 0))  # Red text
        self.screen.blit(text_surface1, (250, 250))  

        # Second message (Restart/Quit prompt)
        text_surface2 = self.font.render("Press R to restart or Q to quit.", True, (255, 255, 255))  # White text
        self.screen.blit(text_surface2, (250, 300))  # Position it below the first message
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game_state = GameState()
                    self.scenario_prompt, self.options = self.update_scenario()
                    self.game_over = False
                elif event.key == pygame.K_q:
                    self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.screen.fill((0, 0, 0))
            if not self.start_game:
                self.draw_initial_ui()
            elif self.loading_character or self.loading_map or self.loading_scenario:
                self.draw_loading_screen()
            elif not self.game_over:
                self.draw_main_screen()
            else:
                self.draw_game_over_screen()
        pygame.quit()
