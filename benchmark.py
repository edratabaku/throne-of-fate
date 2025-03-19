import time
import sys
import os

# Ensure the directory containing `game.py` is in the Python path
sys.path.append(os.path.dirname(__file__))

# Import the Game class from game.py
from game_logic.game import Game

# Benchmark for Game Initialization
def benchmark_game_initialization():
    start_time = time.time()
    game = Game()  # Initialize the game
    game.generate_scenarios()  # Pre-generate scenarios
    end_time = time.time()
    return end_time - start_time

# Benchmark for Scenario Update
def benchmark_scenario_update():
    game = Game()
    game.generate_scenarios()
    start_time = time.time()
    game.update_scenario()  # Update to the next scenario
    end_time = time.time()
    return end_time - start_time

# Benchmark for Image Generation
def benchmark_image_generation():
    game = Game()
    player_description = "A wise and noble king with a golden crown."
    map_description = "A map showing 10 made-up countries with varied terrain."
    start_time = time.time()
    game.generate_images(player_description, map_description)  # Generate images
    game.image_generation_thread.join()  # Wait for the thread to finish
    end_time = time.time()
    return end_time - start_time

def write_results_to_report(initialization_time, scenario_time, image_time):
    report_path = "c:\\Users\\Houssem\\Downloads\\throne-of-fate\\benchmark-report.md"
    with open(report_path, "r") as file:
        lines = file.readlines()

    # Update the Results section in the report
    for i, line in enumerate(lines):
        if line.startswith("### 1. Game Initialization"):
            lines[i + 1] = f"- **Average Time**: {initialization_time:.4f} seconds\n"
        elif line.startswith("### 2. Scenario Update"):
            lines[i + 1] = f"- **Average Time**: {scenario_time:.4f} seconds\n"
        elif line.startswith("### 3. Image Generation"):
            lines[i + 1] = f"- **Average Time**: {image_time:.4f} seconds\n"

    with open(report_path, "w") as file:
        file.writelines(lines)

if __name__ == "__main__":
    initialization_time = benchmark_game_initialization()
    scenario_time = benchmark_scenario_update()
    image_time = benchmark_image_generation()

    print("Game Initialization:", initialization_time, "seconds")
    print("Scenario Update:", scenario_time, "seconds")
    print("Image Generation:", image_time, "seconds")

    write_results_to_report(initialization_time, scenario_time, image_time)
