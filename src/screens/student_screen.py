import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
from src.ui.base_layout import style_base_layout ,style_backgound_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance,get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import process_bulk_audio,get_voice_embeddings
from src.database.db import get_all_students,create_student,get_student_subjects,get_student_attendance,unenroll_student_to_subject

def student_dashboard():
    style_backgound_dashboard()
    style_base_layout()
    
    student_data=st.session_state.student_data
    student_id=student_data['student_id']
    c1,c2=st.columns(2,gap="large")

    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome,{student_data['name']}""")
        if st.button("Logout",key="login_back_btn",shortcut="control+L"):
            st.session_state["is_logged_in"]=False
            del st.session_state.student_data
            st.rerun()
    
    st.space()
    
    c1,c2=st.columns(2)
    with c1:
        st.header("Your enrolled Subjects")
    with c2:
        if st.button("Enroll in subjects",type="primary",width="stretch"):
            enroll_dialog()
            
    st.divider()
    
    #list of subjects
    with st.spinner("Loading your enrolled subjects..."):
        subjects=get_student_subjects(student_id)
        logs=get_student_attendance(student_id)
        
        stats_map={}
        for log in logs:
            sub_id=log['subject_id']
            
            if sub_id not in stats_map:
                stats_map[sub_id]={'Total':0,'Attended':0}
                
            stats_map[sub_id]['Total']+=1
            
            if log.get('is_present'):
                stats_map[sub_id]['Attended']+=1
       
        cols=st.columns(2)
        for i,sub_node in enumerate(subjects):
            sub=sub_node['subjects']
            sub_id=sub['subject_id']
            
            stats=stats_map.get(sub_id,{'Total':0,'Attended':0})
            
            def unenroll_btn():
                if st.button("Unenroll from this course",type='tertiary',key=f"unenroll_btn_{sub_id}",width="stretch",icon=":material/delete_forever:"):
                    unenroll_student_to_subject(student_id,sub_id)
                    st.toast(f"Unenrolled from {sub['name']} successfully!")
                    st.rerun()
                    
            with cols[i%2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('📅','Total',stats['Total']),
                        ('✅','Attended',stats['Attended']),
                    ],
                   footer_callback=unenroll_btn,
                )
        
    footer_dashboard()
    
    
def student_screen():
    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1,c2=st.columns(2,gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",key="login_back_btn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()
    
    style_backgound_dashboard()
    style_base_layout()
    
    st.header("Login with Face ID",text_alignment="center")
    st.space()
    st.space()
    
    show_registration=False
    photo=st.camera_input("Position your face in center")
    if photo:
        img=np.array(Image.open(photo))
        with st.spinner('AI is scanning....'):
           detected,all_ids,num_faces=predict_attendance(img)
           if num_faces==0:
               st.warning('No face found!')
           elif num_faces>1:
               st.warning('Multiple faces found!')
           else:
               if detected:
                   stu_id=list(detected.keys())[0]
                   all_students=get_all_students()
                   student = next((stu for stu in all_students if stu['student_id'] == stu_id), None)
                   
                   if student:
                       st.session_state.is_logged_in=True
                       st.session_state.user_role='student'
                       st.session_state.student_data=student
                       st.toast(f'Welcome back {student['name']}!')
                       import time
                       time.sleep(1)
                       st.rerun()
               else:
                    st.info("Face not recognized! You might be a new student")
                    show_registration=True
                    
    if show_registration:
        with st.container(border=True):
            st.header("Register a new profile")
            new_name=st.text_input("Enter your name")
            
            st.subheader('Optional: Voice Enrollment')
            st.info("enroll for voice only attendance")
            
            audio_data=None
            try:
                audio_data=st.audio_input('Record a short phrase like I am present,My name is Akash')
            except Exception:
                st.error('Audio Data failed')
                
            if st.button('Create Account',type='primary'):
                if new_name:
                    with st.spinner('Creating your Profile...'):
                        img=np.array(Image.open(photo))
                        embedding=get_face_embeddings(img)
                        if embedding:
                            face_emb=embedding[0].tolist()
                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embeddings(audio_data.read())
                            
                            response_data=create_student(new_name,face_emb,voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state.student_data=response_data[0]
                                st.toast(f'Profile created! Hi {new_name}!')
                                import time
                                time.sleep(1)
                                st.rerun()   
                        else:
                            st.error("Couln't capture your facial features for registration")
                                
                            
                else:
                    st.warning('Please enter your name')
                
        
                   
    
    footer_dashboard()