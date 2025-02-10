### Create virtual environment:

```
mkdir ai_strategy_game
cd ai_strategy_game
python -m venv venv
venv\Scripts\activate pip
```

### Install Ollama for text generation and use the mistral model (lightweight ig):

```
curl -fsSL https://ollama.com/install.sh | sh #Linux
#For Windows: https://ollama.com/
ollama pull mistral
ollama run mistral "Hello" #test installation
```

### Install Stable Diffusion for image generation:

Clone the repository:

```
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git cd stable-diffusion-webui
```

Run the installer:

- **Windows:** `webui-user.bat`
- **Linux/Mac:** `bash webui.sh`
  Open `http://127.0.0.1:7860` in your browser.

Install diffusers (HuggingFace library) **globally**:
`pip install torch torchvision diffusers transformers`

### Install requirements

`pip install -r requirements.txt`

### TASK LIST:

- [ ] Limit the scope for the prompts to avoid hallucinating & define country (Priority 1) @Houssem
- [ ] Work on code structure (Priority 1) @Juan
- [ ] Use JSON output with the recommended approach @Juan
- [ ] Generate prompts and options from the beginning to avoid waiting time every time a choice is selected @Edra
- [ ] Test and maybe fix game end logic (set a total number of events) (Priority 1) @Edra
- [ ] Docs (Priority 1) @Juan
- [ ] Benchmarks (Priority 1) @Houssem
- [ ] Maybe use a defined map to also shorten the time it takes for generating the map (Priority 2) @Edra
- [ ] Improve user experience and graphics (Priority 2) @Edra
- [ ] Generate random names for other countries and include them in the prompts (Priority 2) @Houssem
- [ ] Test (Priority 2) @Houssem
- [ ] Report (Priority 1) @Edra & @Juan
- [ ] Video demo & sample results (Priority 1) @Juan
- [ ] Measure timing to help evaluate the results (Priority 1) @Juan
- [ ] Select models for benchmark (Priority 2) @Juan
