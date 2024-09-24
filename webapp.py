import streamlit as st
from tools.word2voice import generate_voice
from elevenlabs import play
from LLM.free_llm import openllm
from prompt.simple_prompt import generate_output

def choose_model():
    """Presents a menu of language models in Streamlit and returns the user's choice."""

    models = {
        "1": {"name": "META LLaMA 3.1 70B", "id": "llama-3.1-70b-versatile"},
        "2": {"name": "META LLaMA 3.1 8B", "id": "llama-3.1-8b-instant"},
        "3": {"name": "Mixtral 8x7B", "id": "mixtral-8x7b-32768"},
        "4": {"name": "Whisper Large v3", "id": "whisper-large-v3"}
    }

    st.sidebar.title("Choose Free Language Model")
    selected_model_key = st.sidebar.radio(
        "Available Models:", list(models.keys()), format_func=lambda x: models[x]["name"]
    )
    return models.get(selected_model_key, {}).get("id")

def main():
    """Main function for the Streamlit app."""

    st.title("Text Generation and Audio Playback App")

    chosen_llm_id = choose_model()

    if chosen_llm_id:
        try:
            # Initialize Language Model 
            llm = openllm(chosen_llm_id)
            if not llm:
                st.error("Could not initialize the language model. Check your configuration.")
                return

            # Generate Text Output
            user_prompt = st.text_area("Enter your prompt:", "")  # Text input box

            if st.button("Generate and Play"):  # Button to trigger generation
                if user_prompt:
                    # Generate Text Output
                    text = generate_output(llm, user_prompt) # Pass the prompt to the function
                    st.write(f"**Generated text:** {text}")
                else:
                    st.warning("Please enter a prompt.") 

            # Generate and Play Audio
                try:
                    audio = generate_voice(text)
                    st.audio(audio)  # Provide the audio bytes to st.audio
                except Exception as audio_error:
                        st.error(f"An error occurred during audio generation or playback: {audio_error}") 
            else:
                st.warning("Please enter a prompt.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please select a language model from the sidebar.")

if __name__ == "__main__":
    import streamlit as st  # Import Streamlit here
    main()