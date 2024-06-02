import streamlit as st
import requests as rq
from bs4 import BeautifulSoup

from modulo.style import css
from modulo.page import page

page()
css()

st.markdown('<h1 class="title">Web Scraper Image 📷</h1>', unsafe_allow_html=True)

def main():
    with st.form("search"):
        keyword = st.text_input("search", "vacation")
        submit = st.form_submit_button("GO")

    if submit and keyword:
        try:
            print(f"Buscando imagens para: {keyword}...")
            page_content = get_page(keyword)
            if page_content:
                process_page(page_content)
                print("Busca completa!")
            else:
                print("Falha ao recuperar a página. Verifique a palavra-chave e tente novamente.")
                st.error("Falha ao recuperar a página. Verifique a palavra-chave e tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro durante a execução: {e}")
            st.error(f"Ocorreu um erro durante a execução: {e}")

def get_page(keyword):
    try:
        response = rq.get(f"https://unsplash.com/pt-br/s/fotografias/{keyword}")
        response.raise_for_status()
        return response.content
    except rq.RequestException as e:
        st.error(f"Erro na requisição: {e}")
        return None

def process_page(page_content):
    soup = BeautifulSoup(page_content, "html.parser")

    # Verificação e ajuste da classe de imagem conforme necessário
    image_elements = soup.find_all("img")  # Verifique todas as tags de imagem

    if not image_elements:
        st.warning("Nenhuma imagem encontrada. Verifique a classe usada na busca.")
        return

    placeholder = st.empty()
    col1, col2 = placeholder.columns(2)

    for index, img in enumerate(image_elements[:10]):  # Limite para 10 imagens
        img_url = img.get("src")
        if img_url:
            if index % 2 == 0:
                col1.image(img_url)
            else:
                col2.image(img_url)
        else:
            st.warning("URL da imagem não encontrada.")

main()