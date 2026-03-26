import streamlit as st
from project_backend import chatbot
from langchain_core.messages import HumanMessage
import time

# 🧠 Configsz
CONFIG = {"configurable": {"thread_id": "advanced-thread"}}

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

# 🎨 Sidebar
with st.sidebar:
    st.title("🤖 AI Assistant")
    st.markdown("### Features")
    st.markdown("""
    - 🧠 Memory enabled  
    - ⚡ Fast responses  
    - 🎯 Structured answers  
    """)
    
    if st.button("🗑️ Clear Chat"):
        st.session_state["messages"] = []
        st.rerun()

# 🧠 Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 💬 Display Chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ✍️ Input
user_input = st.chat_input("Ask anything...")

if user_input:
    # Show user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # 🔥 AI Response with typing effect
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        response = chatbot.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG
        )

        ai_text = response["messages"][-1].content

        # Typing animation
        for word in ai_text.split():
            full_response += word + " "
            placeholder.markdown(full_response)
            time.sleep(0.02)

    # Save response
    st.session_state["messages"].append(
        {"role": "assistant", "content": full_response}
    )