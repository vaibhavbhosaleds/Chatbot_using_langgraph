from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

#  Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

#  Chat State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

#  System Prompt (VERY IMPORTANT for recruiters)
SYSTEM_PROMPT = """
You are an advanced AI assistant designed for real-world productivity.
- Be concise but helpful
- Explain when needed
- Use structured answers
- Act like a professional AI assistant (like ChatGPT)
"""

#  Chat Node
def chat_node(state: ChatState):
    messages = state["messages"]

    # Inject system prompt only once
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = model.invoke(messages)

    return {"messages": [response]}

# Memory
checkpointer = InMemorySaver()

#  Graph
graph = StateGraph(ChatState)
graph.add_node("chat", chat_node)

graph.add_edge(START, "chat")
graph.add_edge("chat", END)

chatbot = graph.compile(checkpointer=checkpointer)