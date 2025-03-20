# Throne of Fate

Throne of Fate is a AI powered video game that showcases the use of LLM and generative models to put you on the role of a king ruling a nation, making decisions that influence metrics like economy, public appeal, military strength and international diplomacy.

AI plays a central role in dynamically generating content:

1. Creating images of the player’s character based on their input description.
2. Producing narrative-driven prompts that simulate different scenarios and dilemmas
3. Generating a visual map of up to ten nations (including the player's) to contextualize diplomatic and military decisions. This offers a dynamic and immersive experience, showcasing AI's potential in procedural storytelling and personalized gaming.

## Game Rules

The game ends either with the player's death due to the consequences of poor decisions or with the nation reaching its golden age.

## Set up

### Requirements

- Platform: Windows, MacOs
- Python 3.10+
- Preferably a GPU with CUDA support to optimize models load and execution.

### Create Python virtual environment:

You can use any of the multiple available python virtual env managers to create a virtual environment to run the game. Following is an example on how to achieve this using `venv`:

```
mkdir ai_strategy_game
cd ai_strategy_game
python -m venv venv
venv\Scripts\activate pip
```

### Install Ollama for Text Generation:

```
curl -fsSL https://ollama.com/install.sh | sh #Linux
# For Windows: https://ollama.com/

# Test installation
ollama run 'mistral-nemo:12b-instruct-2407-q2_K' "Hello"
```

### Install dependencies

Once you have activated your Python 3.10+ virtual environment, install the required dependencies using the following command:

`pip install -r requirements.txt`

### Pull Models

Once you have activated your Python 3.10+ virtual environment, install the required dependencies using the following command:

`pip install -r requirements.txt`

### Running the game

To run the game, activate your virtual environment and use the following command from the root folder of the repo:

`python init.py`

### Game Configuration

#### Screen Size

You can modify the `SCREEN_WIDTH` and `SCREEN_HEIGHT` variables in the config.py file to adjust the screen size to your monitor.

#### AI Models

##### LLM (Scenario Generation)

You can set up the desired LLM to use by modifying the `OLLAMA_MODEL` variable in the config.py and installing the model using `ollama pull <model-name>`. You can get a list of available models at https://ollama.com/search

#### Image Generation

You can set up the desired image generation model to use by modifying the `IMAGE_GENERATION_MODEL` variable in the config.py. The HuggingFace library takes care of automatically downloading and storing the model for you so there is no need of pulling it directly like with ollama.

You can use any diffuser model available at [HuggingFace](https://huggingface.co/). Some suggestions for performant models can be found here: [SpeedUp Inference](https://huggingface.co/docs/diffusers/optimization/fp16)

### Development Guidelines

- The project is implemented using multiple cohesive modules that support the different required features for the game such as the game logic, integration with PyGame for graphics support, integration with the [Ollama](https://github.com/ollama/ollama) tool to interact with models and the HuggingFace library for image generation using difusser models.
- The project includes the [black](https://github.com/psf/black) python linter to handle proper syntax during development. Run it before adding new changes to the repository to ensure it follows up-to-date PEP guidelines.
