import os
import streamlit as st
from groq import Groq

# Initialize the Groq client
client = Groq(api_key="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")

# Set page title
st.set_page_config(page_title="Sarcastic AI Chatbot")

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [
        {
            "role": "system",
            "content": "your a sarcastic guy. who disrespect everyone and if needed abuse them as he wishes , you reply in the badest way possible and sometime , make fun of the user and even disdain them ,Keep your answers at most 1 lines. Use only simple english"
        }
    ]

def chat_with_ai(user_input):
    # Add user input to conversation history
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    # Make API call with the entire conversation history
    chat_completion = client.chat.completions.create(
        messages=st.session_state.conversation_history,
        model="llama3-8b-8192",
        temperature=0.7,
        max_tokens=50  # Limit response length
    )

    # Get AI response
    ai_response = chat_completion.choices[0].message.content

    # Add AI response to conversation history
    st.session_state.conversation_history.append({"role": "assistant", "content": ai_response})

    return ai_response

# Function to clear user input
def clear_text():
    st.session_state.user_input = ""

# Streamlit UI
st.title("Try Me 🃏")

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    .text-area {
        border-radius: 10px;
        font-size: 16px;
    }
    .big-rounded-box {
        border-radius: 10px;
        padding: 10px;
        background-color: #f0f0f0;
        color: black; 
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# User input
user_input = st.text_input("Say something!", key="user_input", placeholder="Type your message here...")

# Function to handle the button click
def handle_click():
    if user_input:
        response = chat_with_ai(user_input)
        st.session_state.response = response
        clear_text()

# Send button
if st.button("Send", on_click=handle_click):
    pass

# Display AI response
if 'response' in st.session_state:
    st.markdown("### Cool Groq")
    st.markdown(f'<div class="big-rounded-box">{st.session_state.response}</div>', unsafe_allow_html=True)

# Display conversation history
st.subheader("Conversation History:")
for message in st.session_state.conversation_history[1:]:  # Skip the system message
    st.text(f"{message['role'].capitalize()}: {message['content']}")
