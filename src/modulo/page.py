import streamlit as st

# Definindo configurações de página
def page():
    st.set_page_config(
        page_title="Web Scraper Image", # Título
        page_icon="src\img\ico.png", # Ícone
        layout="wide",  # Layout da página
        menu_items={
            'Report a bug': "https://github.com/SidneyTeodoroJr",
            'About': "https://github.com/SidneyTeodoroJr/Web_Scraper_Image"
        }
    )