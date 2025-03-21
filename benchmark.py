import time
import sys
import os
import math

# Ensure the directory containing `game.py` is in the Python path
sys.path.append(os.path.dirname(__file__))

# Import the Game class from game.py
from game_logic.game import Game

# Benchmark for Game Initialization
def benchmark_game_initialization():
    start_time = time.time()
    game = Game()  # Initialize the game
    game.generate_scenarios(False)  # Pre-generate scenarios
    game.scenario_generation_tread.join() # Wait for the thread to finish
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

def write_results_to_report(initialization_time, image_time):
    report_path = "benchmark_report.md"
    total_time = initialization_time + image_time

    with open(report_path, "w") as file:
        file.write("# Benchmark Report\n\n")
        file.write("## Results\n\n")
        file.write("### 1. Game Initialization\n")
        file.write(f"- **Time Taken**: {initialization_time:.4f} seconds\n")
        file.write(f"- **Percentage of Total Time**: {(initialization_time / total_time) * 100:.2f}%\n\n")
        # file.write("### 2. Scenario Update\n")
        # file.write(f"- **Time Taken**: {scenario_time:.4f} seconds\n")
        # file.write(f"- **Percentage of Total Time**: {(scenario_time / total_time) * 100:.2f}%\n\n")
        file.write("### 2. Image Generation\n")
        file.write(f"- **Time Taken**: {image_time:.4f} seconds\n")
        file.write(f"- **Percentage of Total Time**: {(image_time / total_time) * 100:.2f}%\n\n")

        # Add analysis section
        file.write("## Analysis\n\n")
        file.write("- **Game Initialization**: If the time exceeds 1 second, consider optimizing the scenario generation process.\n")
        file.write("- **Scenario Update**: A time below 0.5 seconds is ideal for smooth gameplay. If higher, check threading or logic efficiency.\n")
        file.write("- **Image Generation**: This is expected to take the longest. If it exceeds 5 seconds, consider optimizing image generation or reusing assets.\n\n")

        # Summary of performance
        file.write("### Summary\n")
        if initialization_time > 1.0:
            file.write("- Game Initialization is slower than expected. Optimization recommended.\n")
        else:
            file.write("- Game Initialization is within acceptable limits.\n")

        # if scenario_time > 0.5:
        #     file.write("- Scenario Update is slower than expected. Consider reviewing the update logic.\n")
        # else:
        #     file.write("- Scenario Update is performing well.\n")

        if image_time > 5.0:
            file.write("- Image Generation is taking too long. Optimization or asset reuse is advised.\n")
        else:
            file.write("- Image Generation is within acceptable limits.\n")

        # Add total time statistics
        file.write("\n## Total Time\n")
        file.write(f"- **Total Benchmark Time**: {total_time:.4f} seconds\n")
        file.write(f"- **Longest Task**: {'Game Initialization' if initialization_time > image_time else 'Image Generation'}\n")

if __name__ == "__main__":
    initialization_time = benchmark_game_initialization()
    image_time = benchmark_image_generation()

    print("Game Initialization:", initialization_time, "seconds")
    print("Image Generation:", image_time, "seconds")

    write_results_to_report(initialization_time, image_time)
