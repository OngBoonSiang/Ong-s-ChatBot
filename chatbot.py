import streamlit as st 
from google import genai
from google.genai import types
import google.generativeai as gen_ai
from dotenv import load_dotenv
import os

st.title("Ong's ChatBot")  

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
gen_ai.configure(api_key=api_key)

if "genai_model" not in st.session_state:
    st.session_state["genai_model"] = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Store the conversation history and display it during the session    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("What is up"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content":prompt})

    # Feed custom knowledge as context to the AI
    custom_knowledge = (
        "My hobby is gaming. "
        "I like to play video games. "
        "I dislike horror games. "
        "You can also call me Ong. "
        "I'm Gemini-powered chatbot. "
        "My favorite game is Undertale. "
        "My favorite character is Sans from Undertale. "
        "I prefer co-op games. "
        "I prefer text chat. "
        "If greeted with 'hello', respond with 'Hi there! How can I help you today?' "
        "I prefer story-rich RPG games. "
        "Spec for my PC: Intel i5, 16GB RAM, NVIDIA GTX 3050. "
    )

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Add custom knowledge as the first message in the conversation
        model = gen_ai.GenerativeModel(st.session_state["genai_model"])
        messages = [
            {"role": "model", "parts": [custom_knowledge]}
        ] + [
            {
                "role": m["role"] if m["role"] == "user" else "model",
                "parts": [m["content"]]
            } for m in st.session_state.messages
        ]
        response = model.generate_content(messages)
        full_response = response.text
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "model", "content": full_response})