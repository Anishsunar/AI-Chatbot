#app.py
from dotenv import load_dotenv
import os
import streamlit as st
from groq_llm import GroqLLM

# LOAD env & VALIDATE
load_dotenv()
if not os.getenv("GROQ_CHATBOT_API_KEY"):
    st.error("GROQ_CHATBOT_API_KEY not found in .env")
    st.stop()


# PAGE CONFIG
st.set_page_config(
    page_title = "Ask Anything Chatbot",
    page_icon="🤖",
    layout="wide",
    )

# SESSION STATE HELPERS
def init_history():
    if "history" not in st.session_state:
        st.session_state.history = []

def clear_history():
    st.session_state.history =[]

init_history()

# SIDEBAR CONTROLS
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature",0.0,1.0,0.7,0.05)
    if st.button("Clear Chat"):
        clear_history()
    if st.session_state.history:
        transcript = "\n\n".join(
            f"You:{u}\n Bot: {b}" for u, b in st.session_state.history
        )
        st.download_button(
            "Download Transcript",
            transcript,
            file_name = "chat_transcript.txt",
            mime = "text/plain",
        )
# MAIN CHAT UI
st.title("Chatbot")
st.markdown("Enter any question...")

# Display prior messages
for user_msg, bot_msg in st.session_state.history:
    st.chat_message("user").write(user_msg)
    st.chat_message("assistant").write(bot_msg)

# Capture new user input
if user_input := st.chat_input("Type your message here...."):
    # Build context-aware prompt
    convo_context = "".join(
        f"User: {u}\nBot:{b}\n" for u,b in st.session_state.history
    )
    full_prompt = (
        "You are a helpful, Knowledgable assistant.\n"
        f"{convo_context}"
        f"User: {user_input}\n"
        "Bot:"
        )

    llm = GroqLLM(temperature = temperature)
    with st.spinner("Thinking...."):
        try:
            bot_response = llm(full_prompt)
        except Exception as e:
            bot_response = f"Error:{e}"

    # Append and Display
    st.session_state.history.append((user_input, bot_response))
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(bot_response)