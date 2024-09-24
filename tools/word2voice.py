
def generate_voice(text_results):
    from dotenv import load_dotenv 
    load_dotenv()
    import os
    from elevenlabs import generate, set_api_key
    client=set_api_key(
        api_key=os.getenv("EL_API_KEY")
        )
    audio = generate(
    text=text_results,
    voice="Charlie",
    model="eleven_multilingual_v1")
    return audio

