from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def chat_response(client_prompt, resource, model="groq/chat/orca-mini-v3"):
    """Generates an LLM chat response based on user prompt and resource data.

    Args:
        client_prompt: The user's question or prompt.
        resource: Contextual data for the LLM (string).
        model: The Groq chat model to use.
        max_tokens: Maximum number of tokens in the response.
        temperature: Controls randomness of the response.

    Returns:
        The LLM-generated chat response (string) or an error message.
    """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a helpful and informative chat assistant specializing in satellite image analysis. Use the provided resource data to answer user questions.  Your responses should be detailed, suitable for text-to-speech, and within 200 tokens."},
                {"role": "user", "content": f"Resource Data:\n\n{resource}"}, # Provide resource data separately
                {"role": "user", "content": client_prompt}  # User's actual question
            ],
            temperature=1,
            max_tokens=200,
            top_p=0.5,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating chat response: {e}"

