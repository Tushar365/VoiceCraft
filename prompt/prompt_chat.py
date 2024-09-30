from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def chat_response(client_prompt,encoded_image):
    """Generates an LLM chat response based on user prompt and resource data.

    Args:
        client_prompt: The user's question or prompt.
        max_tokens: Maximum number of tokens in the response.
        temperature: Controls randomness of the response.

    Returns:
        The LLM-generated chat response (string) or an error message.
    """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
         # Construct the image URL using the data protocol
        image_url = f"data:image/jpeg;base64,{encoded_image}"
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",

            messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "answer the following question based upon the image in 200 tokens. question: {client_prompt}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
            temperature=1,
            max_tokens=200,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating chat response: {e}"

