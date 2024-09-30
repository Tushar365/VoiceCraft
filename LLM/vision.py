#groq vision (llama 3.2 11b)
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
import os
def vision(encoded_image):
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Identify and describe all objects in the image, including their location and size. Provide the dominant colors and a brief aesthetic evaluation."},  # can change the prompt from here
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }
        ],
        model="llama-3.2-11b-vision-preview",
    )

    return chat_completion.choices[0].message.content