import streamlit as st
import requests
import orjson
from datetime import datetime

# Set your Hugging Face API key
API_KEY = "Bearer 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"
#API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"  # Replace with desired model
API_URL = "https://router.huggingface.co/fireworks-ai/inference/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """
You are a highly intelligent and helpful assistant with deep knowledge of programming, writing, reasoning, and research.
Always respond clearly, accurately, and with proper formatting (markdown and code if needed).
Respond in a friendly, professional, and thoughtful tone.
"""

st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖")
st.title("💬 ChatGPT UI in Streamlit")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "history" not in st.session_state:
    st.session_state["history"] = []

with st.sidebar:
    st.header("📄 Conversation")
    if st.button("⭳ Save & Export History"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_filename = f"chat_history_{timestamp}.json"
        chat_bytes = orjson.dumps(st.session_state.messages, option=orjson.OPT_INDENT_2)
        st.download_button(
            label="🔹 Download Chat History",
            data=chat_bytes,
            file_name=history_filename,
            mime="application/json"
        )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        # Prepare full conversation prompt (simple format for inference)
        conversation = SYSTEM_PROMPT + "\n\n"
        for msg in st.session_state.messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            conversation += f"{role}: {msg['content']}\n"
        conversation += "Assistant:"

        payload = {
            "inputs": conversation,
            "parameters": {
                "max_new_tokens": 200,
                "do_sample": True,
                "top_p": 0.9,
                "temperature": 0.7,
            },
            "model":"accounts/fireworks/models/qwen3-235b-a22b",
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            reply = result[0]["generated_text"].split("Assistant:")[-1].strip()
        except Exception as e:
            reply = f"**Error**: {e}"

        message_placeholder.markdown(reply, unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": reply})
