
def generate_voice(text_results,voice_name):
    from dotenv import load_dotenv 
    load_dotenv()
    import os
    from elevenlabs import generate, set_api_key
    client=set_api_key(
        api_key=os.getenv("EL_API_KEY")
        )
    audio = generate(
    text=text_results,
    voice=voice_name,
    model="eleven_turbo_v2.5")
    return audio

