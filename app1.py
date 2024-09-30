import streamlit as st
import os
from tools.encodding import encode_image
from LLM.vision import vision
from prompt.prompt_chat import chat_response
from prompt.prompt_report import report_response
from tools.word2voice import generate_voice

# --- Styling ---
st.markdown(
    """
    <style>
    body {font-family:'Arial', sans-serif; background-color:#f4f4f4;}
    .stApp {padding:2rem;}
    .stButton>button {background-color:#007bff;color:white;padding:.8rem 1.5rem;
                      border:none;border-radius:5px;font-size:1rem;cursor:pointer;
                      transition:background-color .3s;}
    .stButton>button:hover {background-color:#0056b3;}
    .stTextArea textarea {padding:1rem; border-radius:5px; font-size:1rem;}
    .demo-image {cursor:pointer; margin:5px;}  /* Unused, consider removing */
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
    selected_model_id = st.sidebar.selectbox("Select a Model:", list(models.keys()), format_func=models.get)
    return selected_model_id
    
# --- Image Handling ---
def process_image(image_bytes):
    encoded_image = encode_image(image_bytes)
    return vision(encoded_image)

# --- Main App ---
def main():
    st.title("Voicecraft 🤖🎤")

    model = choose_model()
    selected_prompt_type = st.sidebar.radio("Select Prompt Type:", ["Chat", "Report"])

    # --- Settings ---
    st.sidebar.subheader("⚙️ Settings")
    voice_enabled = st.sidebar.checkbox("Enable Voice Output", value=True)
    
    

    # --- Image Upload ---
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        st.session_state.source_data = process_image(uploaded_file.read())
        

    # --- User Query Input ---  
    client_prompt = st.text_input("Write your query") if selected_prompt_type == "Chat" else None

    # --- Response Generation ---  (Moved up)
    if st.button("Generate Response"):
        with st.spinner("Generating response..."):
            try:
                if selected_prompt_type == "Chat":
                    encoded_image = encode_image(image_bytes)
                    response_text = chat_response(client_prompt,encoded_image)
                else:
                    response_text = report_response(st.session_state.source_data, model)

                st.write(response_text)

                if voice_enabled:
                    audio_result = generate_voice(response_text)
                    st.audio(audio_result, format="audio/wav")

            except Exception as e:
                st.error(f"An error occurred: {e}")


    


if __name__ == "__main__":
    main()
