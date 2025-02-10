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

