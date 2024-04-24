import streamlit as st  
import os  
from openai import OpenAI  

logo = "icons/ufo.png"
user_avatar = "icons/chat.png"
assitant_avatar = "icons/ufo.png"

# Creating an instance of the OpenAI client using the API key from the environment variable
client =  OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# client = OpenAI(os.environ.get("OPENAI_API_KEY"))
# client = OpenAI(api_key=" ")
# client = OpenAI(api_key=st.user_input("Enter your OpenAI API key"))

# Setting the page configuration and title
st.set_page_config(page_title="EY Demo", page_icon=logo)
st.title('ChatGPT Clone')

# Checking if the API key is available
if client is None:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    st.success("API key found.")

# Create a selectbox to allow the user to choose between GPT-4.5-turbo and GPT-4
model_options = ["gpt-3.5-turbo", "gpt-4"]
selected_model = st.selectbox("Select Model", model_options)

# Initialize the default model and messages in the Streamlit session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = selected_model

# Checking if the selected model is available
if selected_model is None:
    st.error("Model not found")
else:
    st.success("Model found.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages with associated avatars
for message in st.session_state['messages']:
    with st.chat_message(message['role'], avatar=user_avatar if message['role'] == 'user' else assitant_avatar):
        st.markdown(message['content'])

# Get user input from the chat input box
if prompt := st.chat_input("type your message here..."):
    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user's message in the chat
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    # Generate a response from the OpenAI model
    with st.chat_message("assistant", avatar=assitant_avatar):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Add the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": response})