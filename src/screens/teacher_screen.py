import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photo_dialog
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.ui.base_layout import style_base_layout ,style_backgound_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login,get_teacher_subjects,get_attendance_for_teacher
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
import pandas as pd
from datetime import datetime

def teacher_screen():
    style_backgound_dashboard()
    style_base_layout()
    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type=='register':
        teacher_screen_register()
   

def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1,c2=st.columns(2,gap="large")

    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"""Welcome,{teacher_data['name']}""")
        if st.button("Logout",key="login_back_btn",shortcut="control+backspace"):
            st.session_state["is_logged_in"]=False
            del st.session_state.teacher_data
            st.rerun()
    
    st.space()
    
    if 'current_teacher_tab' not in st.session_state:
        st.session_state.current_teacher_tab='take_attendance'
    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=='take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1,width="stretch",icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab='take_attendance'
            st.rerun()
            
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=='manage_subjects' else "tertiary"
        if st.button('Manage Subjects',type=type2,width="stretch",icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab='manage_subjects'
            st.rerun()
            
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=='attendance_records' else "tertiary"
        if st.button("Attendance Records",type=type3, width="stretch",icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab='attendance_records'
            st.rerun()
            
    st.divider()
            
    if st.session_state.current_teacher_tab=='take_attendance':
        teacher_tab_take_attendance()
    if st.session_state.current_teacher_tab=='manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state.current_teacher_tab=='attendance_records':
        teacher_tab_attendance_records()
            
    footer_dashboard()
    
    
def teacher_tab_take_attendance():
    st.header('Take AI Attendance')
    
    teacher_id=st.session_state.teacher_data['teacher_id']
    subjects=get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("You haven't created any subjects yet.Please create one to begin!")
        return
    subject_options={f"{subject['name']}-{subject['subject_code']}":subject['subject_id']for subject in subjects}
    
    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images=[]
    
    c1,c2=st.columns([3,1],vertical_alignment="bottom")
    with c1:
       selected_subject_labels=st.selectbox("Select Subjects",options=list(subject_options.keys()))
    with c2:
        if st.button("Add Photos",type="primary",icon=":material/add_a_photo:",width="stretch"):
            add_photo_dialog()
        
    selected_subject_id=subject_options[selected_subject_labels]
    
    st.divider()
    
    if st.session_state.attendance_images:
        st.header("Added photos")
        gallery_cols=st.columns(4)
        
        for i,img in enumerate(st.session_state.attendance_images):
            with gallery_cols[i%4]:
                st.image(img,width="stretch",caption=f"Photo{i+1}")
    
    has_photos=bool(st.session_state.attendance_images)
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button('Clear all photos',type="tertiary",width="stretch",icon=":material/delete:",disabled=not has_photos):
            st.session_state.attendance_images=[]
            st.rerun()
            
    with c2:
        if st.button('Run Face Analysis',width="stretch",icon=":material/analytics:",disabled=not has_photos):
            with st.spinner("Deep Scanning Classroom photos....."):
                all_detected_ids={}
                for i,img in enumerate(st.session_state.attendance_images):
                    img_np=np.array(img.convert("RGB"))
                    detected,_,_=predict_attendance(img_np)
                    if detected:
                        for stu_id in detected.keys():
                            stu_id=int(stu_id)
                            all_detected_ids.setdefault(stu_id,[]).append(f"Photo{i+1}")
                
                enrolled_res=supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_subject_id).execute()
                enrolled_students=enrolled_res.data
                
                if not enrolled_students:
                    st.warning("No students in this course")
                else:
                    result,attendance_logs=[],[]
                    current_timestamp=datetime.now().strftime("%d-%m-%YT%H:%M:%S")
                    
                    for node in enrolled_students:
                        student=node["students"]
                        sources=all_detected_ids.get(int(student['student_id']),[])
                        is_present=len(sources)>0
                        
                        result.append({
                            "Name":student['name'],
                            "ID":student['student_id'],
                            "Source":",".join(sources) if is_present else "-",
                            "Status":"✅ Present" if is_present else "❌ Absent",
                        })
                        
                        attendance_logs.append({
                            "subject_id":selected_subject_id,
                            "student_id":student["student_id"],
                            'timestamps':current_timestamp,
                            "is_present":bool(is_present)
                        })
                        
                attendance_result_dialog(pd.DataFrame(result),attendance_logs)
            
    with c3:
        if st.button("Use Voice Attendance",type="primary", width="stretch",icon=":material/mic:"):
            voice_attendance_dialog(selected_subject_id)
                
            
def teacher_tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    c1,c2=st.columns(2)
    with c1:
       st.header('Manage Subjects')
    with c2:
        if st.button("Create New Subject",width="stretch"):
            create_subject_dialog(teacher_id)
            
    #list all subjects
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("🫂","Students",sub["total_students"]),
                ("🕰️","Classes",sub["total_classes"]),
            ]
        def share_btn():
            if st.button(f"Share Code:{sub['name']}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                share_subject_dialog(sub['name'],sub['subject_code'])
            st.space()
            
        subject_card(
            name=sub['name'],
            code=sub['subject_code'],
            section=sub['section'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("NO Subjects Found.Create new One!")       
    
    
def teacher_tab_attendance_records():
    st.header("Attendance Records")
    teacher_id=st.session_state.teacher_data["teacher_id"]
    records=get_attendance_for_teacher(teacher_id)
    
    if not records:
        return 
    
    data=[]
    
    for r in records:
        ts=r.get("timestamp")
        data.append({
            "ts_grp":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%d-%m-%Y %H:%M %p") if ts else "N'A",
            "Subject":r["subjects"]["name"],
            "Subject Code":r["subjects"]["subject_code"],
            "is_present":bool(r.get("is_present",False))
        })
    
    df=pd.DataFrame(data)
    
    summary=(
        df.groupby(['ts_grp',"Time","Subject","Subject Code"]).agg(
            Present=("is_present","sum"),
            Total=("is_present","count")
        ).reset_index()
    )
    
    summary['Attendance Stats']=(
        "✅" + summary["Present"].astype(str) + "/" + summary["Total"].astype(str) + "Students"
    )
    
    display_df=(summary.sort_values(by="ts_grp",ascending=True)
                [["Time","Subject","Subject Code","Attendance Stats"]]
                )
    
    st.dataframe(display_df,width="stretch",hide_index=True)
    
def login_teacher(teacher_username,teacher_pass):
    if not teacher_username or not teacher_pass:
        return False
    teacher=teacher_login(teacher_username,teacher_pass)
    if teacher:
        st.session_state.user_role='teacher'
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False
        
def teacher_screen_login():
    c1,c2=st.columns(2,gap="large")

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",key="login_back_btn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()

    st.header("Login using password",text_alignment="center")
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder="@abhishek")
    teacher_pass=st.text_input("Enter password",type="password",placeholder="Enter your password")
    st.divider()

    btnc1,btnc2=st.columns(2)
    
    with btnc1:
        if st.button("Login",shortcut="control+Enter",icon=":material/passkey:",width="stretch"):
            if login_teacher(teacher_username,teacher_pass):
                st.toast("Welcome back!",icon="👋")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Credentials")
                
    with btnc2:
        if st.button("Register Instead",type="primary",icon=":material/passkey:",width="stretch"):
            st.session_state["teacher_login_type"]='register'
            st.rerun()

    footer_dashboard()


def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_confirm_pass):
    if not teacher_username or not teacher_name or not teacher_pass or not teacher_confirm_pass :
        return False ,"All fields are required"
    if teacher_pass!=teacher_confirm_pass:
        return False ,"Password doesn't match"
    if check_teacher_exists(teacher_username):
        return False ,"Username already taken"

    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True ,"Successfully registered! Login Now"
    except Exception as e:
        return False ,"Unexpected Error!"



def teacher_screen_register():
    c1,c2=st.columns(2,gap="large")

    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home",key="register_back_btn",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()

    st.header("Register your Teacher Profile")
    st.space()
    st.space()
    teacher_username=st.text_input("Enter username",placeholder="@abhishek")
    teacher_name=st.text_input("Enter name",placeholder="Abhishek Sharma")
    teacher_pass=st.text_input("Enter password",type="password",placeholder="Enter your password")
    teacher_confirm_pass=st.text_input("Confirm password",type="password",placeholder="Confirm your password")
    st.divider()

    btnc1,btnc2=st.columns(2)

    with btnc1:
        if st.button("Register Now",shortcut="control+Enter",icon=":material/passkey:",width="stretch"):
            success,message=register_teacher(teacher_username,teacher_name,teacher_pass,teacher_confirm_pass)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
                
                
    with btnc2:
        if st.button("Login instead",type="primary",icon=":material/passkey:",width="stretch"):
            st.session_state["teacher_login_type"]='login'
            st.rerun()

    footer_dashboard()