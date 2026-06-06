import streamlit as st

def header_home():
    st.markdown("""
                <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px;">
                    <img src="https://i.ibb.co/YTYGn5qV/logo.png" style='height:100px;'/>
                    <h1>Snap <br>Class</h1>
                </div>
                """,
                unsafe_allow_html=True
                )
    
def header_dashboard():
    st.markdown("""
                <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
                    <img src="https://i.ibb.co/YTYGn5qV/logo.png" style='height:85px;'/>
                    <h2 style="color:red">Snap<br> Class</h2>
                </div>
                """,
                unsafe_allow_html=True
                )