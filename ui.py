import streamlit as st
import llm

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    .stTextInput input {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #dcdcdc;
        padding: 10px;
    }
    .stButton button {
        background-color: #4caf50;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .human-message {
        background-color: #e1f5fe;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
    }
    .ai-message {
        background-color: #fbe9e7;
        border-radius: 15px;
        padding: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 AI Chatbot")
st.write("Welcome! Ask me anything, and I'll do my best to assist. Type your message below and hit **Submit**!")

humanInput = st.text_input("Enter your prompt here", placeholder="What's on your mind?")
if st.button("Submit"):
    if not humanInput:
        st.warning("⚠️ Please enter a prompt above before submitting.")
    else:
        llm_response = llm.process(humanInput)
        
        # Reverse the order of messages before displaying
        reversed_messages = reversed(llm_response)
        
        for m in reversed_messages:
            if m.type == 'human':
                st.markdown(
                    f"<div class='human-message'><strong>Human:</strong> {m.content}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='ai-message'><strong>AI:</strong> {m.content}</div>",
                    unsafe_allow_html=True
                )
