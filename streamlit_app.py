import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

def create_conversation():
    response = requests.post(f"{BASE_URL}/conversation/create")
    return response.json()["conversation_id"]

def send_message(conversation_id, message):
    response = requests.post(f"{BASE_URL}/conversation/{conversation_id}/message", json={"content": message})
    try:
        return response.json()["response"] 
    except KeyError:
        return "Error: Unexpected response format. Please check your backend API."


st.set_page_config(
    page_title="Innova Schools | Bot ",
    page_icon=':bar_chart:',
    layout="centered", 
)
st.image('assets/fernandito_01.png')
st.title("Hola, Estoy aqui para ti")
st.write("Recuerda que estamos mejorando constantemente para poder ofrecerte una mejor asistencia.")
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Escribe tu mensaje"):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = send_message(st.session_state.conversation_id, prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)