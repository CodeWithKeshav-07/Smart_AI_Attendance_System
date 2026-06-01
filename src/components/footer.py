import streamlit as st

def footer_home():
    footer = """
        <style>
        .footer {
            display:flex;
            align-items:center;
            justify-content:center;
            position: fixed;
            font-weight:bold;
            width:100%;
            bottom: 0;               
            left: 0;
            color: white;
            padding: 20px;
            margin-top:70px;
            font-size: 25px;
        }
        </style>

        <div class="footer">
            <p>Created with ❤️ by Keshav </p>
        </div>
    """

    st.markdown(footer, unsafe_allow_html=True)