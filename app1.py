import streamlit as st
import requests
import orjson
from datetime import datetime

# Set your OpenRouter API key
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# System prompt for the assistant
SYSTEM_PROMPT = """
You are a highly intelligent and helpful assistant with deep knowledge of programming, writing, reasoning, and research.
Always respond clearly, accurately, and with proper formatting (markdown and code if needed).

If the user input requires calculation, reasoning, or tool use (like search or calculator), indicate the required tool.
When answering questions, always refer to the previous context and summarize if helpful.

Respond in a friendly, professional, and thoughtful tone.
"""

# Set up Streamlit UI
st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖")
st.title("💬 ChatGPT UI in Streamlit")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "history" not in st.session_state:
    st.session_state["history"] = []

# Sidebar for history export
with st.sidebar:
    st.header("📄 Conversation")
    if st.button("⭳ Save & Export History"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_filename = f"chat_history_{timestamp}.json"
        # Serialize messages using orjson
        chat_bytes = orjson.dumps(st.session_state.messages, option=orjson.OPT_INDENT_2)
        st.download_button(
            label="🔹 Download Chat History",
            data=chat_bytes,
            file_name=history_filename,
            mime="application/json"
        )

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek/deepseek-prover-v2:free",
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"**Error**: {e}"

        # Show and save assistant response
        message_placeholder.markdown(reply, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": reply})
