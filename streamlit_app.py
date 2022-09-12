import streamlit as st
from gsheetsdb import connect


gsheet = "https://docs.google.com/spreadsheets/d/1YsMlHjmeTPr_WV9yNRlnrEgk-ytX9kp_YZ8cQDRmcKY/edit?usp=sharing"


# Create a connection object.
conn = connect()

@st.cache
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows


rows = run_query(f'SELECT * FROM "{gsheet}"')
answers = []
for row in rows:
    st.write('WAT',row.name)
    answers.append(st.text_input('Enter Sentence', ''))
    for i in range(20):
            sleep(1000)
            st.write('Timer',i)
    if i ==20:
            continue
            
      
    
