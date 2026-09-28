import streamlit as st


def initialize_chat():

    if "chats" not in st.session_state:
        st.session_state.chats = {
            "New Chat": []
        }

    if "current_chat" not in st.session_state:
        st.session_state.current_chat = "New Chat"


def get_messages():
    return st.session_state.chats[
        st.session_state.current_chat
    ]


def add_message(role, content):

    st.session_state.chats[
        st.session_state.current_chat
    ].append({
        "role": role,
        "content": content
    })


def new_chat():

    number = len(st.session_state.chats) + 1

    name = f"Chat {number}"

    st.session_state.chats[name] = []

    st.session_state.current_chat = name


def delete_current_chat():

    if len(st.session_state.chats) == 1:
        return

    del st.session_state.chats[
        st.session_state.current_chat
    ]

    st.session_state.current_chat = list(
        st.session_state.chats.keys()
    )[0]


def switch_chat(name):
    st.session_state.current_chat = name