     
## free llm
def freellm(model_name):
    """Initializes and returns a ChatGroq language model instance.

    Args:
        model_name (str): The name of the Groq language model to load (e.g., "llama-3.1-70b-versatile").

    Returns:
        langchain_groq.ChatGroq: An initialized ChatGroq language model instance, or None if initialization fails. 
    
    Raises:
        Exception: If there is an error initializing the ChatGroq model (e.g., invalid API key, network issues).
           The specific error message will be printed to the console.
    """

    from dotenv import load_dotenv
    load_dotenv()
    import os
    from langchain_groq import ChatGroq 

    GROQ_API_KEY = os.getenv("GROQ_API_KEY") 

    try:
        model = ChatGroq(
            model=model_name,
            temperature=0.6,
            max_tokens=120,
            timeout=None,
            max_retries=2,
            groq_api_key=GROQ_API_KEY
        )
        return model
    except Exception as e:
        print(f"Error initializing ChatGroq model: {e}")
        return None 


# For testing purposes


## generic main function
'''
if __name__ =="__main__":
    choose_llm = choose_model()
    llm=openllm(choose_llm)
    if llm:
        while True:
            user_input = input("Enter your prompt (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            response = llm.invoke(user_input)
            print(f"Response: {response.content}")
    else:
        print("Could not initialize the language model. Please check the configuration.")
'''

## chose model

def choose_model():
    """Presents a menu of language models and returns the user's choice."""

    models = {
        "1": {"name": "META LLaMA 3.1 70B", "id": "llama-3.1-70b-versatile"},
        "2": {"name": "META LLaMA 3.1 8B", "id": "llama-3.1-8b-instant"},
        "3": {"name": "Mixtral 8x7B", "id": "mixtral-8x7b-32768"},
        "4": {"name": "Whisper Large v3", "id": "whisper-large-v3"}
    }

    print("Available Language Models:")
    for key, model in models.items():
        print(f"{key}. {model['name']}")

    while True:  # Keep asking until a valid choice is made
        choice = input("Enter your choice (1/2/3/4): ")
        if choice in models:
            return models[choice]["id"]
        else:
            print("Invalid choice. Please try again.")
