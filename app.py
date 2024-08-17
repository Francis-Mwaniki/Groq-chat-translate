import os
import streamlit as st
from groq import Groq
import speech_recognition as sr
from gtts import gTTS
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit app
st.set_page_config(page_title="Chat & Language Translation App", layout="wide")

# Custom CSS
st.markdown("""
<style>
.stApp {
    background-color: black;
}
.stTextInput > div > div > input {
    background-color: #ffffff;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
}
.chat-message.user {
    background-color: #2b313e;
    color: #ffffff;
}
.chat-message.bot {
    background-color: black;
    color: #ffffff;
}
.chat-message .avatar {
    width: 20%;
}
.chat-message .message {
    width: 80%;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for app selection
app_mode = st.sidebar.selectbox("Choose the app mode", ["Chat", "Language Translation"])

if app_mode == "Chat":
    

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="mixtral-8x7b-32768",
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

elif app_mode == "Language Translation":
    st.title("Language Translation")

    # Language selection
    languages = ["English", "French", "Spanish", "German", "Italian", "Portuguese", "Russian", "Chinese", "Japanese", "Korean"]
    source_lang = st.selectbox("Select source language:", languages)
    target_lang = st.selectbox("Select target language:", languages)

    # Text input
    text_to_translate = st.text_area("Enter text to translate:", height=150)

    if st.button("Translate"):
        if text_to_translate:
            # Translate text using Groq
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful translator."},
                    {"role": "user", "content": f"Translate the following text from {source_lang} to {target_lang}: {text_to_translate}"},
                ],
                model="mixtral-8x7b-32768",
            )
            translation = response.choices[0].message.content
            st.write("Translation:")
            st.write(translation)
        else:
            st.warning("Please enter some text to translate.")
st.sidebar.markdown("---")
st.sidebar.info("This app uses LLMA Mistral AI its Super Fast check it out")
