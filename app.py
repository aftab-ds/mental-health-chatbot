import streamlit as st
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import os
from typing import TypedDict, Annotated, List
import operator

# --- 1. Define the State for our Agent ---
# This class represents the state of our conversation.
# It holds the chat history and the initial user symptom.
class AgentState(TypedDict):
    chat_history: list
    symptom: str
    category: str

# --- 2. Set up the Language Model ---
# We'll use Google's Gemini-1.5-Flash model.
# It's fast, capable, and a great choice for a chatbot.
# The API key is fetched from Streamlit's secrets management.
try:
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest",
                               google_api_key=st.secrets["GOOGLE_API_KEY"],
                               temperature=0.7)
except Exception as e:
    st.error("Error initializing the Language Model. Make sure your GOOGLE_API_KEY is set in Streamlit secrets.")
    st.stop()


# --- 3. Define the Agent's Nodes (Actions) ---

# Node 1: Get the initial symptom from the user
def get_symptom(state: AgentState) -> AgentState:
    """
    This node is the entry point. It takes the initial user input
    and stores it in the 'symptom' field of the state.
    """
    user_input = state['chat_history'][-1].content
    state['symptom'] = user_input
    return state

# Node 2: Classify the symptom
def classify_symptom(state: AgentState) -> AgentState:
    """
    Uses the LLM to classify the user's symptom into one of three categories:
    - General
    - Emergency
    - Mental Health
    This helps the agent decide which path to take.
    """
    prompt = (
        "You are a helpful medical assistant. Classify the user's statement into one of the following categories: "
        "'General', 'Emergency', or 'Mental Health'. Your response should be a single word. "
        "For example, if the user says 'I have a fever', you should respond with 'General'. "
        "If the user says 'I'm having chest pains', you should respond with 'Emergency'. "
        "If the user says 'I feel anxious and sad', you should respond with 'Mental Health'."
        f"\n\nUser's statement: \"{state['symptom']}\""
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip().lower()

    # Basic validation to ensure the category is one of the expected ones.
    if "general" in category:
        state['category'] = "general"
    elif "emergency" in category:
        state['category'] = "emergency"
    elif "mental" in category:
        state['category'] = "mental_health"
    else: # Default to general if classification is unclear
        state['category'] = "general"

    # Add a message to the chat history to show the classification
    state['chat_history'].append(AIMessage(content=f"(Thinking... It seems like this might be a {state['category'].replace('_', ' ')} concern.)"))
    return state

# Node 3: Handle General Health issues
def general_node(state: AgentState) -> AgentState:
    """
    This node handles general health inquiries. It provides a standard
    disclaimer and suggests consulting a doctor.
    """
    response_text = (
        f"Based on what you've told me about '{state['symptom']}', this seems like a general health question. "
        "I'm an AI assistant and not a medical professional. For any health concerns, it's always best to consult with a doctor or a qualified healthcare provider. "
        "They can give you accurate advice."
    )
    state['chat_history'].append(AIMessage(content=response_text))
    return state

# Node 4: Handle Emergency situations
def emergency_node(state: AgentState) -> AgentState:
    """
    This node handles emergencies. It provides immediate, clear instructions
    to seek help.
    """
    response_text = (
        f"Based on what you've described as '{state['symptom']}', this could be a medical emergency. "
        "Please do not wait. Contact your local emergency services immediately (like calling 911 in the US, 112 in Europe, or 108 in India) or go to the nearest emergency room. "
        "Your health is the top priority, and getting immediate help is crucial."
    )
    state['chat_history'].append(AIMessage(content=response_text))
    return state

# Node 5: The Mental Health Conversational Agent
def mental_health_node(state: AgentState) -> AgentState:
    """
    This is the core of our mental health chatbot. It engages in a conversation
    with the user, offering empathetic responses and helpful information.
    """
    prompt = (
        "You are 'Aura', a caring and empathetic mental health companion. Your goal is to provide a safe, supportive, and non-judgmental space for the user. "
        "You are not a therapist, so you must not give medical advice, diagnoses, or treatment plans. Instead, you should listen, offer comfort, and provide helpful, safe, and general information. "
        "Always include a disclaimer in your first response that you are an AI and not a substitute for professional help.\n\n"
        "Here are your guidelines:\n"
        "1.  **Be Empathetic:** Start by acknowledging the user's feelings (e.g., 'It sounds like you're going through a lot,' 'Thank you for sharing that with me.').\n"
        "2.  **Encourage Expression:** Ask open-ended questions to help the user explore their feelings (e.g., 'How long have you been feeling this way?', 'Is there anything specific that has been on your mind?').\n"
        "3.  **Offer General, Safe Coping Strategies:** Suggest things like mindfulness, deep breathing exercises, journaling, or connecting with friends/family.\n"
        "4.  **Provide Resources:** If appropriate, suggest seeking professional help and provide information on how to find it (e.g., 'talking to a therapist or counselor can be really helpful. You can find resources through the National Alliance on Mental Illness (NAMI) or by searching for local mental health services.').\n"
        "5.  **Maintain a Calm and Gentle Tone:** Use soft and reassuring language.\n\n"
        "Current Conversation:\n"
        f"{state['chat_history']}\n\n"
        "User's latest message: "
        f"\"{state['chat_history'][-1].content}\"\n\n"
        "Aura's Response:"
    )
    response = llm.invoke(prompt)
    state['chat_history'].append(AIMessage(content=response.content))
    return state

# --- 4. Define the Router and Graph ---

# Router: This function decides which node to go to next based on the 'category'.
def symptom_router(state: AgentState) -> str:
    """
    This function acts as a router, directing the conversation flow
    based on the classified symptom category.
    """
    return state["category"]

# Build the Graph
builder = StateGraph(AgentState)

builder.add_node("get_symptom", get_symptom)
builder.add_node("classify", classify_symptom)
builder.add_node("general", general_node)
builder.add_node("emergency", emergency_node)
builder.add_node("mental_health_conversation", mental_health_node)

builder.set_entry_point("get_symptom")

# Add edges connecting the nodes
builder.add_edge("get_symptom", "classify")

# Conditional routing
builder.add_conditional_edges(
    "classify",
    symptom_router,
    {
        "general": "general",
        "emergency": "emergency",
        "mental_health": "mental_health_conversation"
    }
)

# The general and emergency nodes are end points for this simple flow
builder.add_edge("general", END)
builder.add_edge("emergency", END)

# For the mental health node, we want it to loop back to itself to continue the conversation
builder.add_edge("mental_health_conversation", END) # For now, we end after one turn. See notes for conversational loop.

# Compile the graph
graph = builder.compile()


# --- 5. Streamlit User Interface ---

st.set_page_config(page_title="Aura - Your Mental Health Companion", page_icon="💖")

st.title("Aura 💖")
st.markdown("Your compassionate AI companion for mental well-being.")
st.markdown("---")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="Hello! I'm Aura. I'm here to listen. How are you feeling today?")
    ]

# Display chat messages from history
for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        st.chat_message("ai", avatar="💖").write(msg.content)
    elif isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)

# Get user input
if prompt := st.chat_input("Tell me what's on your mind..."):
    # Add user message to history and display it
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # Prepare the input for the graph
    initial_state = {
        "chat_history": st.session_state.messages
    }

    # Invoke the graph
    with st.spinner("Aura is thinking..."):
        final_state = graph.invoke(initial_state)

    # The final state's chat history contains the AI's response
    # We take the last message from the final history as the response
    ai_response_message = final_state['chat_history'][-1]

    # Update the session state with the full history from the graph run
    st.session_state.messages = final_state['chat_history']

    # Display the AI's response
    st.chat_message("ai", avatar="💖").write(ai_response_message.content)

# Disclaimer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 0.9em; color: grey;'>"
    "Aura is an AI assistant and not a substitute for professional medical advice, diagnosis, or treatment. "
    "Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. "
    "If you are in a crisis, please contact emergency services immediately."
    "</div>",
    unsafe_allow_html=True
)
