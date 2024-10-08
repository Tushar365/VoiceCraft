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

def encode_image(image_bytes):  # More robust encoding
    try:
        from PIL import Image
        from io import BytesIO
        import base64

        image = Image.open(BytesIO(image_bytes))
        buffered = BytesIO()
        image.save(buffered, format="JPEG") # Ensure JPEG format
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except Exception as e:
        st.error(f"Image encoding error: {e}")
        return None

# --- Image Handling ---
def process_image(image_bytes):
    encoded_image = encode_image(image_bytes)
    if encoded_image: # Check if encoding succeeded
        st.session_state.encoded_image = encoded_image # Store encoded image
        return vision(encoded_image) 
    else:
        return None


# --- Main App ---
def main():
    st.title("Voicecraft 🤖🎤")

    model = choose_model()
    selected_prompt_type = st.sidebar.radio("Select Prompt Type:", ["Chat", "Report"])

    # --- Settings ---
    st.sidebar.subheader("⚙️ Settings")
    voice_enabled = st.sidebar.checkbox("Enable Voice Output", value=True)

    available_voices = ["Charlie", "Alice", "Charlotte", "Sakuntala","Lily","Eric"]  # Example voice list
    voice_name = st.sidebar.selectbox("Select a voice", available_voices)
    
    

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
                    if "encoded_image" not in st.session_state:
                        st.error("Please upload an image first.")
                    else:
                        encoded_image = st.session_state.encoded_image # Use stored encoded image
                        response_text = chat_response(client_prompt, encoded_image)

                        # ... (rest of the response handling, voice, etc.)

                else:
                    response_text = report_response(st.session_state.source_data, model)

                st.write(response_text)

                if voice_enabled:
                    audio_result = generate_voice(response_text,voice_name)
                    st.audio(audio_result, format="audio/wav")

            except Exception as e:
                st.error(f"An error occurred: {e}")


    


if __name__ == "__main__":
    main()
