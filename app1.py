import streamlit as st
from tools.encodding import encode_image
from LLM.vision import vision
from prompt.prompt_chat import chat_response
from prompt.prompt_report import report_response
from tools.word2voice import generate_voice
import os

# --- Page Configuration ---
st.set_page_config(page_title="💬 VoiceCraft", page_icon="🤖", layout="wide")

# --- Funky Styling ---
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

# --- Model Selection ---
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


# --- Main App Function ---
def main():
    st.title("Voicecraft 🤖🎤")

    model = choose_model()
    selected_prompt_type = st.sidebar.radio("Select Prompt Type:", ["Chat", "Report"])

    # --- Session State ---
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = True
    st.sidebar.subheader("⚙️ Settings")
    st.session_state.voice_enabled = st.sidebar.checkbox("Enable Voice Output", value=True)

    # --- Image Upload and Processing ---
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        if 'image_encoded' not in st.session_state or st.session_state.image_encoded != uploaded_file:
            st.session_state.image_encoded = uploaded_file
            bytes_data = uploaded_file.read()
            encoded_image = encode_image(bytes_data)
            st.session_state.source_data = vision(encoded_image)

        # --- User Query Input (Conditional) ---
        if selected_prompt_type == "Chat":
            client_prompt = st.text_input("Write your query")
        else:
            client_prompt = None

        # --- Response Generation ---
        if st.button("Generate Response"):
            with st.spinner("Generating response..."):
                try:
                    if selected_prompt_type == "Chat":
                        text_result = chat_response(client_prompt, st.session_state.source_data, model)
                    else:
                        text_result = report_response(st.session_state.source_data, model)
                    st.write(text_result)
                    if st.session_state.voice_enabled:
                        audio_result = generate_voice(text_result)
                        st.audio(audio_result, format="audio/wav")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

# --- Run the app ---
if __name__ == "__main__":
    main()
