import streamlit as st
from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from src.components.dialog_attendance_result import show_attendance_result
from datetime import datetime
import pandas as pd

@st.dialog("Voice Attendance Reports")
def voice_attendance_dialog(sub_id):
    st.write("Record audio of students saying I am present.Then AI will recognise the students")
    
    audio_data=None
    audio_data=st.audio_input("Record classroom audio")
    if st.button("Analyze Audio",width="stretch",type="primary"):
        with st.spinner("Processing audio data...."):
            enrolled_res=supabase.table("subject_students").select("*,students(*)").eq("subject_id",sub_id).execute()
            enrolled_students=enrolled_res.data
                
            if not enrolled_students:
                st.warning("No students in this course")
                return
            
            candidate_dict={s['students']['student_id']:s['students']['voice_embedding'] for s in enrolled_students if s['students'].get('voice_embedding') }
            if not candidate_dict:
                st.error("No student has voice profile registered")
                return
            
            audio_bytes=audio_data.read()
            detected_score=process_bulk_audio(audio_bytes,candidate_dict)
            
            result,attendance_logs=[],[]
            current_timestamp=datetime.now().strftime("%d-%m-%YT%H:%M:%S")
            
            for node in enrolled_students:
                student=node["students"]
                score=detected_score.get(student['student_id'],0.0)
                is_present=bool(score>0)
                
                result.append({
                    "Name":student['name'],
                    "ID":student['student_id'],
                    "Score":score if is_present else "-",
                    "Status":"✅ Present" if is_present else "❌ Absent",
                })
                
                attendance_logs.append({
                    "subject_id":sub_id,
                    "student_id":student["student_id"],
                    'timestamps':current_timestamp,
                    "is_present":bool(is_present)
                })
                
            st.session_state.voice_attendance_results=(pd.DataFrame(result),attendance_logs)
            
    if st.session_state.get('voice_attendance_results'):
        st.divider()
        df,logs=st.session_state.voice_attendance_results
        show_attendance_result(df,logs)