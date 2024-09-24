import streamlit as st
from tools.word2voice import generate_voice
from LLM.free_llm import freellm
from prompt.simple_prompt import generate_output

# --- Page Configuration for a More Engaging Look ---
st.set_page_config(
    page_title="💬 VoiceCraft", 
    page_icon="🤖", 
    layout="wide",  # Use the full page width
)

# --- Styling with CSS for a Unique Look ---
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4; 
    }
    .stApp {
        padding: 2rem;
    }
    .stButton>button {
        background-color: #007bff; 
        color: white;
        padding: 0.8rem 1.5rem;
        border: none;
        border-radius: 5px;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.3s; 
    }
    .stButton>button:hover {
        background-color: #0056b3; 
    }
    .stTextArea textarea {
        padding: 1rem;
        border-radius: 5px;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Model Selection with Clearer UI --- 
def choose_model():
    models = {
        "llama-3.1-70b-versatile": "🧠 META LLaMA 3.1 (70B)",
        "llama-3.1-8b-instant": "🧠 META LLaMA 3.1 (8B)",
        "mixtral-8x7b-32768": "🧠 Mixtral 8x7B",
        "whisper-large-v3": "👂 Whisper Large v3",
    }

    st.sidebar.title("🤖 Choose Your AI")
    selected_model_id = st.sidebar.selectbox(
        "Select a Model:", 
        list(models.keys()), 
        format_func=lambda x: models[x] 
    )
    return selected_model_id

# --- Main App Logic ---
def main():
    st.title("🎙️ VoiceCraft: Hear Your Words Come Alive!")
    st.write("Generate text with powerful AI models and listen to the results.")

    chosen_llm_id = choose_model()

    if chosen_llm_id:
        try:
            llm = freellm(chosen_llm_id)
            if not llm:
                st.error("Oops! Couldn't initialize the model. Please check the configuration.")
                return

            user_prompt = st.text_area("Enter your prompt:", placeholder="e.g., Write a short story about a cat who loves to code.", height=150)

            if st.button("✨ Generate & Listen! ✨"):
                if user_prompt:
                    with st.spinner("Generating... ✨"):
                        text = generate_output(llm, user_prompt)
                        st.write("**Generated Text:**", text)

                    with st.spinner("Speaking... 🎙️"):
                        try:
                            audio = generate_voice(text)
                            st.audio(audio)
                        except Exception as audio_error:
                            st.error(f"Uh oh! Audio error: {audio_error}")
                else:
                    st.warning("Please enter a prompt! 😊")
        except Exception as e:
            st.error(f"Oops! An error occurred: {e}")
    else:
        st.info("Start by choosing a model from the sidebar. 👈")

if __name__ == "__main__":
    main()