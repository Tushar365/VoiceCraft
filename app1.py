import streamlit as st
from tools.encodding import encode_image
from LLM.vision import vision
from prompt.prompt_chat import chat_response
from prompt.prompt_report import report_response
from tools.word2voice import generate_voice
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="💬 VoiceCraft",
    page_icon="🤖",
    layout="wide",
)

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
    /* ... other styles if needed ... */
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

    # --- Prompt Type Selection ---
    prompt_types = {
        "chat": "Chat",
        "report": "Report"
    }
    selected_prompt_type = st.sidebar.radio("Select Prompt Type:", list(prompt_types.keys()), format_func=lambda x: prompt_types[x])

    # --- Session State Initialization ---
    if 'image_encoded' not in st.session_state:
        st.session_state.image_encoded = None
    if 'audio_result' not in st.session_state:
        st.session_state.audio_result = None
    if 'voice_enabled' not in st.session_state:
        st.session_state.voice_enabled = True

    # --- Voice Tool Toggle ---
    st.sidebar.subheader("⚙️ Settings")
    st.session_state.voice_enabled = st.sidebar.checkbox("Enable Voice Output", value=True)

    # --- Image Upload ---
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # --- Display the image ---
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if uploaded_file is not None:
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.read())
        image_path = "temp_image.jpg"

        if st.session_state.image_encoded is None or st.session_state.image_encoded != image_path:
            st.session_state.image_encoded = image_path
            encoded_image = encode_image(image_path)
            st.session_state.source_data = vision(encoded_image)
        else:
            encoded_image = st.session_state.image_encoded

        os.remove(image_path)

        # --- User Query Input (Conditional) ---
        if selected_prompt_type == "chat":
            client_prompt = st.text_input("Write your query")
        else:
            client_prompt = None

        # --- Response Generation ---
        if st.button("Generate Response"):
            with st.spinner("Generating response..."):
                if selected_prompt_type == "chat":
                    text_result = chat_response(client_prompt=client_prompt, resource=st.session_state.source_data, model=model)
                elif selected_prompt_type == "report":
                    text_result = report_response(resource=st.session_state.source_data, model=model)
                else:
                    st.error("Invalid prompt type selected.")
                    text_result = ""

                if st.session_state.voice_enabled:
                    st.session_state.audio_result = generate_voice(text_result)

            st.write(text_result)

            if st.session_state.audio_result and st.session_state.voice_enabled:
                st.audio(st.session_state.audio_result, format="audio/wav")



# --- Run the app ---
if __name__ == "__main__":
    main()
