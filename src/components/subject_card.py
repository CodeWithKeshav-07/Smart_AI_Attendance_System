import streamlit as st
def subject_card(name,code,section,stats=None,footer_callback=None):
    html=f"""
       <div style="background-color:white; border-left:8px solid #EB459E; border:2px solid black; padding:25px; border-radius:20px; margin-bottom:20px;">
       <h3 style="margin:0; color:#1e293b; font-size:1.5rem">{name}</h3>
       <p style="color:#64748b;margin:10px 0;">Code:<span style="color:#5685F2; background:#E0E3FF; padding:2px 8px; border-radius:5px;">{code}</span> | Section:{section} </p>
    """
    
    if stats:
       html+=f"""
         <div style="display:flex; flex-wrap:wrap; gap:8px;">
       """
       for icon,label,value in stats:
           html+=f'<div style="background:#EB459E10; padding:5px 12px; border-radius:12px; font-size:0.9rem;"> {icon} <b>{value}</b> {label} </div>'
           
       html+="</div>"
    html+="</div>"
    
    st.markdown(html,unsafe_allow_html=True)
    
    if footer_callback:
        footer_callback()