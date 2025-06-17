import streamlit as st
from dotenv import load_dotenv
import os
import json
from utils.groq_api import get_llm_response
from utils.framework_builder import generate_framework

# Load environment variables
load_dotenv()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add initial welcome message
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi there!👋I am Mary Tales. Who is this story about?✨"
    })

if "story_info" not in st.session_state:
    st.session_state.story_info = {
        "title": "",
        "setting": "",
        "character_main": "",
        "character_side": "",
        "goal": "",
        "conflict": "",
        "climax": "",
        "helpers": "",
        "villains": "",
        "ending": "",
        "theme": "",
        "extras": []
    }

def extract_story_info(messages):
    """
    Extract story information from the conversation
    """
    try:
        # Create a prompt to analyze the conversation
        analysis_prompt = """Analyze this conversation and extract key story elements. 
        Return ONLY a valid JSON object with these exact fields (leave empty string if not mentioned):
        {
            "title": "",
            "setting": "",
            "character_main": "",
            "character_side": "",
            "goal": "",
            "conflict": "",
            "climax": "",
            "helpers": "",
            "villains": "",
            "ending": "",
            "theme": ""
        }
        Do not include any other text or explanation, just the JSON object."""
        
        # Get analysis from LLM
        analysis = get_llm_response(messages, analysis_prompt)
        
        # Try to parse the JSON response
        try:
            # Find the JSON object in the response
            start_idx = analysis.find('{')
            end_idx = analysis.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = analysis[start_idx:end_idx]
                story_data = json.loads(json_str)
                
                # Update story_info with the parsed data
                for key in st.session_state.story_info:
                    if key in story_data and story_data[key]:
                        st.session_state.story_info[key] = story_data[key]
        except json.JSONDecodeError:
            st.error("Could not parse story information from the response")
            
    except Exception as e:
        st.error(f"Error analyzing conversation: {str(e)}")

def main():
    st.title("📚 Mary Tales")
    st.subheader("Your Friendly Story Building Assistant")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to write about?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get Mary Tales response
        try:
            with st.chat_message("assistant"):
                with st.spinner("Mary Tales is thinking..."):
                    # Read the system prompt
                    with open("prompts/story_qa_prompt.txt", "r") as f:
                        system_prompt = f.read()
                    
                    # Get response from LLM
                    response = get_llm_response(st.session_state.messages, system_prompt)
                    
                    # Add response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)
                    
                    # Update story info after each exchange
                    extract_story_info(st.session_state.messages)
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
        
    # Create Framework button
    if st.button("Create Framework"):
        # Generate and display the framework
        framework = generate_framework(st.session_state.story_info)
        st.markdown(framework)
        
        # Add download button for the framework
        st.download_button(
            label="Download Framework",
            data=framework,
            file_name="story_framework.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main() 