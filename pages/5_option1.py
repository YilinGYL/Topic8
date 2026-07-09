# READ STATE BEFORE THE WIDGET
import streamlit as st

if st.session_state.get('clear'):
    st.session_state['name'] = ''

if st.session_state.get('streamlit'):
    st.session_state['name'] = 'Streamlit'

st.text_input('Name', key='name')
st.button('Clear name', key='clear')
st.button('Streamlit!', key='streamlit')