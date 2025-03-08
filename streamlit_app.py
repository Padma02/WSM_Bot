import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Women Safety Measure")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ask for user identity (Ensuring it's a woman)
if "verified" not in st.session_state:
    st.session_state.verified = False

if not st.session_state.verified:
    gender = st.text_input("For safety reasons, please confirm: Are you a woman? (Yes/No)").strip().lower()
    
    if gender == "yes":
        st.session_state.verified = True
        st.success("Verification successful! You can now ask about safety and health advice.")
    elif gender == "no":
        st.error("Sorry, this chatbot is designed only for women. Please refer to general safety resources.")
        st.stop()
    else:
        st.warning("Please answer 'Yes' or 'No' to proceed.")
        st.stop()

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input for symptoms or safety concerns
user_input = st.chat_input("Describe your symptoms or safety concerns here...")

# Function to get a response from OpenAI with health/safety advice
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": (
                "You are an AI assistant that only provides safety and health advice for women. "
                "If a non-woman user interacts, politely refuse the conversation. "
                "Under no circumstances should you provide responses to men or any unrelated topics. "
                "Your responses should strictly focus on women's safety, health, and well-being."
            )}
        ] + [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_prompt = (
        f"User has reported: {user_input}. Provide a general remedy or safety advice. "
        "Ensure that your response remains strictly within the context of women's safety and health."
    )
    assistant_response = get_response(assistant_prompt)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
