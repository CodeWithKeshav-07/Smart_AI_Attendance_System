import streamlit as st

def student_screen():
    st.header('Student screen')

    if st.button("Go to home page"):
        st.session_state["login_type"]=None
        st.rerun()