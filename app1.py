import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Set up Streamlit UI
st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖")
st.title("💬 ChatGPT UI in Streamlit")

SYSTEM_PROMPT = """
You are a highly intelligent and helpful assistant with deep knowledge of programming, writing, reasoning, and research.
Always respond clearly, accurately, and with proper formatting (markdown and code if needed).

If the user input requires calculation, reasoning, or tool use (like search or calculator), indicate the required tool.
When answering questions, always refer to the previous context and summarize if helpful.

Respond in a friendly, professional, and thoughtful tone.
"""

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
        st.download_button(
            label="🔹 Download Chat History",
            data=json.dumps(st.session_state.messages, indent=2),
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

        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-prover-v2:free",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages,
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"**Error**: {e}"

        # Show and save assistant response
        message_placeholder.markdown(reply, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": reply})
