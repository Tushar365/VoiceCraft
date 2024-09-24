"# VoiceCraft"
https://lablab.ai/event/elevenlabs-ai-audio-challenge

## ✨ Features 

- **Easy-to-Use Interface:** Generate text and audio with just a few clicks.
- **Multiple Language Models:** Choose from a variety of free-to-use AI models.
- **Customizable Prompts:** Provide your own creative prompts to guide the AI.
- **Realistic Text-to-Speech:** Hear your generated text spoken aloud with natural-sounding voices.

## 🚀 Getting Started

Here's how to get VoiceCraft up and running on your local machine use bash:

**1. Clone the Repository:**
```
git clone https://github.com/Tushar365/VoiceCraft.git
```
after the change the cd  
```
cd voiceCraft
```

**2. Create a Virtual Environment:**
```
python -m venv .venv
```

**3. Activate the Environment:**

Windows:
```
.venv\Scripts\activate
```

macOS/Linux:
```
source .venv/bin/activate
```

**4. Add Your API Keys:**

Add your API keys to the .env file:
```
GROQ_API_KEY="your_actual_groq_api_key"
EL_API_KEY="your_actual_elevenlabs_api_key"
```

**5. Install Requirements:**
```
pip install -r requirements.txt
```

**6. Run the Streamlit App:**
```
streamlit run app.py
```

**📚 Project Structure**
```
Here's a brief overview of the project's file structure:
word2voice_voiceCraft/
├── LLM/               # Code related to language model interactions 
│   └── open_llm.py     
├── prompt/            # Code for handling and formatting prompts
│   └── simple_prompt.py 
├── tools/             # Utility functions (like text-to-speech)
│   └── word2voice.py   
└── app.py # The main Streamlit application script
```
**⚙️ How to run**

https://youtu.be/Wf1RnVjvLmw

**▶️ Demo Video**

https://youtu.be/fh4i449wGiE

**🙏 Acknowledgments**

This project uses the following amazing libraries:
Streamlit: For building the web app interface.
LangChain: For working with language models.
ElevenLabs: For realistic text-to-speech synthesis.
