import streamlit as st

# Estilizando a página
def css():
    st.markdown("""
        <style>
        h1 {
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        .title {
            color: #ffffff;
            text-align: center;
            position: relative;
            font-size: 2.5rem;
            letter-spacing: 0.3em;
            transition: 0.3s;
            text-shadow: 1px 1px 0 grey, 1px 2px 0 grey, 1px 3px 0 grey, 1px 4px 0 grey,
            1px 5px 0 grey, 1px 6px 0 grey, 1px 7px 0 grey, 1px 8px 0 grey,
            5px 13px 15px #bd4bfb9b;
        }
        img {
            margin: 0.8em;
            filter: brightness(60%);
            border-radius: 15px;
            box-shadow: #ffffff 0px 0px 0px 5px;
        }
        </style>
    """, unsafe_allow_html=True)