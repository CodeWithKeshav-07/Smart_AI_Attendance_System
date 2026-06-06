from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
    return bcrypt.checkpw(pwd.encode(),hashed.encode())

def check_teacher_exists(username):
    #check unique username,returns false when username already taken
    response=supabase.table("teachers").select("username").eq("username",username).execute()
    return len(response.data)>0

def create_teacher(username,password,name):
    data={"username":username,"password":hash_pass(password),"name":name}
    response=supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username,password):
    response=supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:
        teacher=response.data[0]
        if check_pass(password,teacher["password"]):
            return teacher
    return None

def get_all_students():
    response=supabase.table("students").select("*").execute()
    return response.data

def create_student(name,face_emb=None,voice_emb=None):
    data={"name":name,"face_embedding":face_emb,"voice_embedding":voice_emb}
    response=supabase.table("students").insert(data).execute()
    return response.data

def create_subject(sub_code,sub_name,sub_section,teacher_id):
    data={"subject_code":sub_code,"name":sub_name,"section":sub_section,"teacher_id":teacher_id}
    response=supabase.table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    response=supabase.table("subjects").select("*,subject_students(count),attendance_logs(timestamps)").eq("teacher_id",teacher_id).execute()
    subjects=response.data
    
    for sub in subjects:
        sub['total_students']=sub.get('subject_students',[{}])[0].get('count',0) if sub.get('subject_students') else 0
        attendance=sub.get('attendance_logs',[])
        sub['total_classes']=len(set(log['timestamps'] for log in attendance))
        
        sub.pop('subject_students',None)
        sub.pop('attendance_logs',None)
        
    return subjects

def enroll_student_to_subject(stu_id,sub_id):
    data={"subject_id":sub_id,"student_id":stu_id}
    response=supabase.table("subject_students").insert(data).execute()
    return response.data

def unenroll_student_to_subject(stu_id,sub_id):
    response=supabase.table("subject_students").delete().eq('student_id',stu_id).eq('subject_id',sub_id).execute()
    return response.data

def get_student_subjects(stu_id):
    res=supabase.table("subject_students").select("*,subjects(*)").eq("student_id",stu_id).execute()
    return res.data
    
def get_student_attendance(stu_id):
    res=supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",stu_id).execute()
    return res.data

def create_attendance(logs):
    res=supabase.table("attendance_logs").insert(logs).execute()
    return res.data

def get_attendance_for_teacher(teacher_id):
    res=supabase.table("attendance_logs").select("*,subjects!inner(*)").eq("subjects.teacher_id",teacher_id).execute()
    return res.data