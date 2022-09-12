import streamlit as st
from gsheetsdb import connect
import time

gsheet = "https://docs.google.com/spreadsheets/d/1YsMlHjmeTPr_WV9yNRlnrEgk-ytX9kp_YZ8cQDRmcKY/edit?usp=sharing"


@st.cache
def run_query(query):
    # Create a connection object.
    conn = connect()
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


def gather_info():
    st.title("Word Association Test - 20 Seconds")
    st.write('Please enter details')
    with st.form(key='my_form'):
        st.text_input('Enter Name', key='name')
        st.number_input('Enter Beginning question no.',value=0, step=1, key='count')
        st.number_input('Enter Total Questions',value=3, step=1, key='total')
        submit = st.form_submit_button(label='Submit', on_click=initialize)


def initialize():
    rows = run_query(f'SELECT * FROM "{gsheet}"')
    if 'count' not in st.session_state:
        st.session_state.count = 1
    st.session_state.timer = 0
    st.session_state.data = {}
    st.session_state.end = int(st.session_state.count) + int(st.session_state.total)
    i = 1
    for row in rows:
        if i >= st.session_state.count:
            st.session_state.data[row.words] = ''
        if i >= st.session_state.end:
            break
        i += 1
    st.session_state.current = 0
    st.session_state.end = st.session_state.total
    st.session_state.word = list(st.session_state.data.keys())[st.session_state.count]
    st.session_state.started = True


def generate_results():
    st.title("Word Association Test - 20 Seconds")
    for key, value in st.session_state.data.items():
        st.write(key, " : ", value)


def update_data():
    if st.session_state.current < st.session_state.end:
        st.session_state.current += 1
        st.session_state.timer = 0
        st.session_state.data[st.session_state.word] = st.session_state.statement
        st.session_state.word = list(st.session_state.data.keys())[st.session_state.current]
        generate_ques()
    else:
        generate_results()


def generate_ques():
    st.session_state.start_time = time.time()
    st.title("Word Association Test - 20 Seconds")
    st.write('Word= ', st.session_state.word)
    with st.form(key='my_form'):
        st.text_input('Enter Sentence', value = '', key='statement')
        submit = st.form_submit_button(label='Submit', on_click=update_data)


if 'started' not in st.session_state:
    gather_info()
elif st.session_state.started and st.session_state.current == 0:
    generate_ques()
