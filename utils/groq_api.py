import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_llm_response(messages, system_prompt):
    """
    Get response from Groq LLM
    """
    try:
        # Prepare the messages with system prompt
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        # Get response from Groq
        response = client.chat.completions.create(
            messages=full_messages,
            model="llama-3.3-70b-versatile",  # Using LLAMA model
            temperature=0.8,
            max_tokens=1024,
            top_p=0.9,  # Added for better response quality
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}" 