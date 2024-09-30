from groq import Groq
from dotenv import load_dotenv
import os
import base64

load_dotenv()  # Load environment variables from .env file

def vision(encoded_image):
    """Analyzes an image using the Groq API and provides a description.

    Args:
        encoded_image: Base64 encoded image data.

    Returns:
        str: The image description generated by the Groq API. 
    """

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY") 
    )

    # Construct the image URL using the data protocol
    image_url = f"data:image/jpeg;base64,{encoded_image}" 

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
Analyze the provided image and provide a comprehensive description of all discernible objects.  For each object, include:

* **Object Type/Class:** (e.g., person, car, building, tree, animal)
* **Location:** Describe the object's position in the image (e.g., "center," "top-left," "next to the [other object]").
* **Size (Relative):**  Estimate the object's size relative to other objects or the overall image (e.g., "small," "large," "covers most of the image").  If possible, estimate actual size (e.g., "approximately 2 meters tall").
* **Other Notable Features:** Include any other visually distinctive characteristics (e.g., color, shape, texture).

Also provide:

* **Dominant Colors:** List the most prominent colors in the image.
* **Aesthetic Evaluation (Brief):** A short commentary on the image's aesthetic qualities (e.g., "vibrant," "serene," "dynamic," etc.).
* **Object Count:** The total number of each type of object identified.
                        """
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
        model="llama-3.2-11b-vision-preview", 
    )
    return chat_completion.choices[0].message.content 
