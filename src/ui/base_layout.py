import streamlit as st

def style_backgound_home():
    st.markdown("""
                <style>
                    .stApp{
                        background-color:rgb(64, 61, 252,0.5) !important;
                    }
                
                    .stApp div[data-testid="stColumn"]{
                        height:270px !important;
                        width:50px !important;
                        background-color:white !important;
                        margin-top:20px; !important;
                        padding-left:30px  !important;
                        border-radius:50px !important;
                    }
                </style>
                """,
                unsafe_allow_html=True
                )
    
def style_backgound_dashboard():
    st.markdown("""
                <style>
                    .stApp{
                        background-color:rgb(186, 122, 245,0.3) !important;
                    }
                </style>
                """,
                unsafe_allow_html=True
                )
    
def style_base_layout():
    st.markdown("""
                <style>
                @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
                @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

                  /*Hide top bar of streamlit*/
                    #MainMenu,footer,header{
                       visibility:hidden;
                    }
                
                    .block-container{
                       padding-top:1.5rem !important;
                    }
                
                    h1{
                        font-family:'Climate Crisis',sans-sarif !important;
                        font-size:3.5rem !important;
                        text-align:center !important;
                        line-height:1 !important;
                        margin:0rem !important;
                        color:white !important;
                    }
                    
                
                    h2{
                        font-family:'Climate Crisis',sans-sarif !important;
                        font-size:2rem !important;
                        line-height:1.1 !important;
                        margin:0rem !important;
                        
                    }
                
                    h3,h4,p{
                        font-family:'Outfit',sans-sarif !important;
                    }
                     
                    

                    button[kind="secondary"]{
                        background-color:#EB459E !important;
                        border-radius:15px !important;
                        padding:0 20px 0 20px !important;
                        color:white !important;
                        border:none !important;
                        transition:transform 0.25s ease-in-out !important;
                    }
                
                    button{
                        background-color:#5865F2 !important;
                        border-radius:15px !important;
                        padding:0 20px !important;
                        margin-top:5px !important;
                        margin-bottom:5px !important;
                        color:white !important;
                        border:none !important;
                        transition:transform 0.25s ease-in-out !important;
                    }
                
                    button[kind="tertiary"]{
                        background-color:black !important;
                        border-radius:15px !important;
                        padding:0 20px 0 20px !important;
                        color:white !important;
                        border:none !important;
                        transition:transform 0.25s ease-in-out !important;
                    }
                    
                    button:hover{
                       transform:scale(1.05)
                    }

                </style>
                """,
                unsafe_allow_html=True
                )
    
