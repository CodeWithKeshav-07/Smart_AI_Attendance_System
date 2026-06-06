import streamlit as st
import segno
import io #to handle binary data

@st.dialog("Share Class Link")
def share_subject_dialog(sub_name,sub_code):
    app_domain="snapclass-main.streamlit.app"
    join_url=f"{app_domain}/?join-code={sub_code}"
    
    st.header('Scan to Join')
    
    qr=segno.make(join_url)
    out=io.BytesIO()
    qr.save(out,kind='png',scale=10,border=1)
    
    c1,c2=st.columns(2)
    with c1:
        st.markdown('### Copy Link')
        st.code(join_url,language="text")
        st.code(sub_code,language="text")
        st.info("Copy this link to share on Whatsapp or Email")
    with c2:
        st.image(out.getvalue(),caption="QR Code for Class Joining")
    
    