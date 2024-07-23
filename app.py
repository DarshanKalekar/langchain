import os
from groq import Groq
import streamlit as st
from apikey import groq

# Initialize the Groq client with your API key
client = Groq(api_key=groq)

# For conversation history
conversation_history = []

def update_history(user_input, bot_response):
    conversation_history.append({"user": user_input, "bot": bot_response})

def get_history():
    return conversation_history

def solve_math_problem(problem):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"Solve this math problem: {problem}"}
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)

def generate_idea(topic=None):
    try:
        prompt = f"Generate a creative YouTube video idea"
        if topic:
            prompt += f" about {topic}"
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return str(e)

def chatbot(user_input):
    response = ""
    
    if user_input.lower().startswith("solve"):
        math_problem = user_input[6:]  # Remove 'solve ' from the input
        response = solve_math_problem(math_problem)
    
    elif user_input.lower().startswith("idea for"):
        topic = user_input[9:]  # Remove 'idea for ' from the input
        response = generate_idea(topic)
    
    elif user_input.lower().startswith("history"):
        response = get_history()
    
    else:
        response = "I'm sorry, I don't understand that command. Please try 'solve [math problem]', 'idea for [topic]', or 'history'."
    
    update_history(user_input, response)
    return response

# Streamlit interface
st.title("Chatbot with History, Math Solving, and Creative Ideas")
user_input = st.text_input("You: ", "Type your message here...")
if st.button("Send"):
    response = chatbot(user_input)
    st.text_area("Bot:", value=response, height=200)
    
    st.write("Conversation History:")
    for entry in conversation_history:
        st.write(f"**User:** {entry['user']}")
        st.write(f"**Bot:** {entry['bot']}")
