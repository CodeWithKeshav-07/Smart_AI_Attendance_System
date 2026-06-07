import streamlit as st
from src.database.db import create_attendance

def show_attendance_result(df,logs):
    st.write("Please review the attendance before confirming.Absent students are automatically marked as well")
    st.dataframe(df,hide_index=True,width="stretch")
    
    c1,c2=st.columns(2)
    with c1:
        if st.button("Discard",width="stretch"):
            st.session_state.voice_attendance_results=None
            st.session_state.attendance_images=[]
            st.rerun()
    with c2:
         if st.button("Confirm & Save",width="stretch"):
            try:
                create_attendance(logs)
                st.toast("Attendance taken")
                st.session_state.attendance_images=[]
                st.session_state.voice_attendance_results=None
                st.rerun()
                
            except Exception as e:
                st.error(f"Sync Failed! Error details: {e}") 

@st.dialog("Attendance Reports")
def attendance_result_dialog(df,logs):
    show_attendance_result(df,logs)
    