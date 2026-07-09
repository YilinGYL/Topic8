# USE ST.CONTAINER TO REORDER RENDERING
import streamlit as st

begin = st.container()

if st.button('Clear name'):
    st.session_state.name = ''

if st.button('Streamlit!'):
    st.session_state.name = 'Streamlit'

begin.text_input('Name', key='name')