from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def report_response(resource, model):
    """Gets an LLM-generated report from resource data.

    Args:
        resource: The data (string) for the LLM to analyze.
        model: The Groq chat model to use (default: orca-mini-v3).

    Returns:
        The LLM-generated report (string).  Returns an error message if the API call fails.
    """
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        completion = client.chat.completions.create(
            model=model,
               messages=[
        {
            "role": "assistant",
            "content": "You are a talented satellite image analyst. Analyze the resourse data and generate a highly detailed accurate report suitable for text-to-speech, within 1000 tokens. the data {resource}"
        },
        {
            "role": "user",
            "content": "your answers must be suitable for tts tools avoid * within 1000 tokens"
        },
        {
            "role": "user",
            "content": f"Resource Data:\n\n{resource}"
        },
        
    ],
            #messages=[
            #    {"role": "system", "content": "You are a talented satellite image analyst. Analyze the provided data thoroughly and generate a detailed report suitable for text-to-speech, within 1000 tokens."},  # Combined instructions into system role
            #    {"role": "user", "content": f"Analyze:\n\n{resource}"} #Simplified user prompt
            #],
            temperature=0.7, #Slightly lower temperature for more focused response
            max_tokens=1000, #Increased max_tokens to match requirement
            top_p=0.5,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:  # Added error handling
        return f"Error generating report: {e}"

