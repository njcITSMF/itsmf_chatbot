import streamlit as st
from backend_logic import run_rag_llm

if 'messages' not in st.session_state:
    st.session_state['messages'] = []


def display_messages():
    print("display_messages")
    for message in st.session_state['messages']:
        with st.chat_message(message['role']):
            st.write(message['content'])

def run_user_query(query):
    print("run_user_query")
    response = run_rag_llm(query)
    st.session_state['messages'].append({'role': 'user', 'content': query})
    st.session_state['messages'].append({'role': 'assistant', 'content': response})
    display_messages()



st.title(":blue[ITSMF Chat Bot]")


st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #222222;
    }

    [data-testid="stSidebar"] {
        background-color: black;
    }

    [data-testid="stHeader"] {
        background-color: black;
    }

    [data-testid="stBottomBlockContainer"] {
        background-color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")



if st.sidebar.button(':red[Reset Chat]'):
    st.session_state['messages'].clear()



st.sidebar.write(" ")
st.sidebar.write(" ")
st.sidebar.write(" ")


if st.sidebar.button(":blue[What is ITSMF?]"):
    run_user_query("What is ITSMF?")

st.sidebar.write(" ")

if st.sidebar.button(":blue[How do I join ITSMF?]"):
    run_user_query("How do I join ITSMF?")

st.sidebar.write(" ")

if st.sidebar.button(":blue[Is ITSMF hiring?]"):
    run_user_query("Is ITSMF hiring?")

st.sidebar.write(" ")



user_question = st.chat_input("Ask a question...")


if user_question:
    run_user_query(user_question)
    