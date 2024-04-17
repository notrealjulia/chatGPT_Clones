import streamlit as st  
import os  
from openai import OpenAI  

# Creating an instance of the OpenAI client using the API key from the environment variable
client =  OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# client = OpenAI(os.environ.get("OPENAI_API_KEY"))
# client = OpenAI(api_key=" ")
# client = OpenAI(api_key=st.user_input("Enter your OpenAI API key"))

# Setting the page configuration and title
st.set_page_config(page_title="EY Demo", page_icon="icons/ufo.png")
st.title('ChatGPT Clone')

# Checking if the API key is available
if client is None:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    st.success("API key found.")

selected_model = "gpt-3.5-turbo"  # Setting the default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = selected_model

# Checking if the selected model is available
if selected_model is None:
    st.error("Model not found")
else:
    st.success("Model found.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Getting user input
prompt = st.chat_input("Type your message here...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generating a chat completion using the OpenAI client
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Writing the response from the chat completion to the streamlit app
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
