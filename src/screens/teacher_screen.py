import streamlit as st

def teacher_screen():
    st.header('Teacher screen')
    
    if st.button("Go to home page"):
        st.session_state["login_type"]=None
        st.rerun()