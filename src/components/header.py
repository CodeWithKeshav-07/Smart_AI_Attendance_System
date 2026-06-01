import streamlit as st

def header_home():
    st.markdown("""
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px;">
                    <img src="https://i.ibb.co/YTYGn5qV/logo.png"/>
                    <h1>Smart Attendance System</h1>
                </div>
                """,
                unsafe_allow_html=True
                )