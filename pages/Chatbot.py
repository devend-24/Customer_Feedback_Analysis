<<<<<<< HEAD
import streamlit as st
from groq import Groq
import pandas as pd
import os
import json
import sqlite3


# Set API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY is not set.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Load Product Data
def load_product_data():
    with open("pages/products.json", "r") as file:
        return json.load(file)

product_data = load_product_data()


# Function to fetch data from SQLite
def fetch_data():
    try:
        conn = sqlite3.connect("db.sqlite3")  # Connect to SQLite DB
        query = "SELECT * FROM analytics_feedback"
        df = pd.read_sql(query, conn)  # Load data into DataFrame
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None  # Return None if there's an error

# Fetch and display data
data = fetch_data()

# System Prompt
SYSTEM_PROMPT = f"""
You are a helpful product assistant for an e-commerce store. 
Use this product data to answer questions: {json.dumps(product_data)}
You can also use this product database and ratings: {data.to_string(index=False)}

Follow these rules:
1. Keep answers conversational and brief
2. Maintain context from previous questions
3. If asked about unspecified details, say you don't have that information
4. Never mention the JSON structure or technical terms
5. For features/specs, use bullet points only when explicitly asked
6. Be Transparent, also provide negative reviews if asked explicitly.
"""

# Streamlit UI
st.sidebar.title("🔹 Product Assistant")
st.title("🛍️ Product Chatbot")
st.write("Ask about any product!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] != "system":  # Don't show system message
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User Input
user_query = st.chat_input("Type your question...")

if user_query:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        # Generate Response (include full history)
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=300
        )

        bot_reply = response.choices[0].message.content

        # Ensure reply stays focused on products
        if "I don't have access to that information" in bot_reply:
            bot_reply = "I'm sorry, I don't have that information in my product database. Would you like me to check something else?"

    except Exception as e:
        bot_reply = "Sorry, I'm having trouble answering that right now. Please try again later."

    # Display Bot Response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    
    # Save to Chat History (excluding system prompt)
=======
import streamlit as st
from groq import Groq
import pandas as pd
import os
import json
import sqlite3


# Set API Key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("❌ GROQ_API_KEY is not set.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Load Product Data
def load_product_data():
    with open("pages/products.json", "r") as file:
        return json.load(file)

product_data = load_product_data()


# Function to fetch data from SQLite
def fetch_data():
    try:
        conn = sqlite3.connect("db.sqlite3")  # Connect to SQLite DB
        query = "SELECT * FROM analytics_feedback"
        df = pd.read_sql(query, conn)  # Load data into DataFrame
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None  # Return None if there's an error

# Fetch and display data
data = fetch_data()

# System Prompt
SYSTEM_PROMPT = f"""
You are a helpful product assistant for an e-commerce store. 
Use this product data to answer questions: {json.dumps(product_data)}
You can also use this product database and ratings: {data.to_string(index=False)}

Follow these rules:
1. Keep answers conversational and brief
2. Maintain context from previous questions
3. If asked about unspecified details, say you don't have that information
4. Never mention the JSON structure or technical terms
5. For features/specs, use bullet points only when explicitly asked
6. Be Transparent, also provide negative reviews if asked explicitly.
"""

# Streamlit UI
st.sidebar.title("🔹 Product Assistant")
st.title("🛍️ Product Chatbot")
st.write("Ask about any product!")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] != "system":  # Don't show system message
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User Input
user_query = st.chat_input("Type your question...")

if user_query:
    # Add User Message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        # Generate Response (include full history)
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=300
        )

        bot_reply = response.choices[0].message.content

        # Ensure reply stays focused on products
        if "I don't have access to that information" in bot_reply:
            bot_reply = "I'm sorry, I don't have that information in my product database. Would you like me to check something else?"

    except Exception as e:
        bot_reply = "Sorry, I'm having trouble answering that right now. Please try again later."

    # Display Bot Response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    
    # Save to Chat History (excluding system prompt)
>>>>>>> ee367e60d63fa073741c0a3e635232e7ce489ca7
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})