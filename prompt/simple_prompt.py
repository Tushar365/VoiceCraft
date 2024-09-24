from langchain.prompts import PromptTemplate  
from langchain.chains import LLMChain  

def generate_output(model, user_prompt):
    """Generates output from the language model using a LangChain prompt.

    Args:
        model: The initialized language model instance (e.g., a ChatGroq object).
        user_prompt (str): The user's prompt or input to the language model.

    Returns:
        str: The language model's response to the prompt.
    """

    # 1. Define the prompt template (unchanged)
    template = """
    You are a helpful and creative AI assistant.
    you only answer in less than 100 tokens.
    the answer should be knowledgeable and simple to understand.
    The response will be played by eleven_multilingual_v1 so it must be ieal for text to voice tool. 
    Please respond to the following user prompt:

    {user_prompt}
    """
    prompt = PromptTemplate(template=template, input_variables=["user_prompt"])

    # 2. Create an LLMChain (unchanged) 
    llm_chain = LLMChain(prompt=prompt, llm=model)

    # 3. Generate the response (Use invoke instead of run)
    response = llm_chain.invoke({"user_prompt": user_prompt})
    
    return response['text'] # Access the 'text' key in the response