import streamlit as st
import requests

BASE_URL = "http://localhost:8000"
st.set_page_config(
    page_title="Innova Schools | Bot ",
    page_icon=':robot-face:',
    layout="centered", 
)


def create_conversation():
    response = requests.post(f"{BASE_URL}/conversation/create")
    return response.json()["conversation_id"]

def send_message(conversation_id, message):
    response = requests.post(f"{BASE_URL}/conversation/{conversation_id}/message", json={"content": message})
    try:
        return response.json()["response"]["content"]
    except KeyError:
        return "Error: Unexpected response format. Please check your backend API."



st.image('assets/fernandito_01.png')
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .css-1rs6os {visibility: hidden;}
            .css-17ziqus {visibility: hidden;}
            button[title="View fullscreen"]{
            visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style,unsafe_allow_html=True)


st.title("Hola, Estoy aqui para ti \u270C\uFE0F️")
st.write("Recuerda que estamos mejorando constantemente para poder ofrecerte una mejor asistencia.")
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_conversation()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] == "assistant":
        st.chat_message("assistant",avatar="assets/assistant-pic.png").write(message["content"])
    else:
        st.chat_message("user",avatar="assets/user-avatar.jpeg").write(message["content"])

if prompt := st.chat_input("Escribe tu mensaje"):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    #st.toast('Recuerda no enviar demasiada informacion personal!', icon='✅')
    st.chat_message("user",avatar="assets/user-avatar.jpeg").write(prompt)

    response = send_message(st.session_state.conversation_id, prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant",avatar="assets/assistant-pic.png").write(response)