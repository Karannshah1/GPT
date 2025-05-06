import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Streamlit app title
st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖")
st.title("💬 ChatGPT UI in Streamlit")


# Initialize memory and message storage
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# When the user inputs a message
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        # Update LangChain memory
        st.session_state.memory.chat_memory.add_user_message(prompt)

        # LLM configuration with tuned temperature for better quality
        llm = ChatOpenAI(
            model="deepseek/deepseek-prover-v2:free",
            temperature=0.5,  # More focused replies
            base_url="https://openrouter.ai/api/v1",
    api_key="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",
        )

        # System message to guide the assistant
        system_prompt = """
You are a helpful and knowledgeable AI assistant that gives concise, clear, and practical answers.
When asked any questions, you provide well-structured response.
Always answer politely and support your responses with reasoning if needed.
"""

        # Define LangChain prompt template
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])

        # Construct the full LLMChain with memory
        chain = LLMChain(
            llm=llm,
            prompt=prompt_template,
            memory=st.session_state.memory,
            verbose=False,
        )

        # Generate response
        try:
            reply = chain.predict(input=prompt)
        except Exception as e:
            reply = f"Error: {e}"

        # Display and store reply
        placeholder.markdown(reply)
        st.session_state.memory.chat_memory.add_ai_message(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
