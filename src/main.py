# Importando as dependências
import streamlit as st
import requests as rq
from bs4 import BeautifulSoup
import webbrowser as web

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
page()

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
            animation: floatAnimation 3.5s ease-in-out infinite alternate;
            box-shadow: #ffffff 0px 0px 0px 5px;
        }
        @keyframes floatAnimation {
            0% {
                transform: translateY(0);
            }
            100% {
                transform: translateY(-10px);
            }
        }
        </style>
    """, unsafe_allow_html=True)
css()

st.markdown('<h1 class="title">Web Scraper Image 📷</h1>', unsafe_allow_html=True) # Título

# Essa função recebe uma palavra-chave como entrada e envia um formulário
def main():
    with st.form("search"):
        keyword = st.text_input("search", "landscape") # Campo de entrada do usuário
        st.form_submit_button("GO") # Botão de submit

    # Verifica se o usuário inseriu uma palavra-chave
    if keyword:
        try:
            page = get_page(keyword) # Recuperar o conteúdo HTML da página web
            if page is not None: 
                process_page(page) # pega o conteúdo como entrada e extrai as informações relevantes.
        except Exception as e:
            st.error(f"Ocorreu um erro durante a execução: {e}") # Mensagem de erro

# Recupera o conteúdo relacionada a uma determinada palavra-chave
def get_page(keyword):
    response = rq.get(f"https://unsplash.com/pt-br/s/fotografias/{keyword}")

    if response.status_code == 200:
        return response.content
    # Caso não encontre, retorna mensagem de erro
    else:
        st.warning(f"Falha na requisição. Código de status: {response.status_code}")
        return None

# Extrai elementos usando BeautifulSoup
def process_page(page_content):
    soup = BeautifulSoup(page_content, "lxml")
    rows = soup.find_all("div", class_="ripi6")
    placeholder = st.empty()
    col1, col2 = placeholder.columns(2) # Criando duas colunas de tamanhos iguais
    # Enumera as linhas e itera cada uma na lista
    for index, row in enumerate(rows): 
        process_row(row, index, col1, col2)

# A função analisa uma linha de tabela HTML com índice e duas colunas. 
def process_row(row, index, col1, col2):
    figures = row.find_all("figure")

    if len(figures) >= 2:
        for i in range(2):
            img = figures[i].find("img", class_="tB6UZ a5VGX")

            if img and "srcset" in img.attrs:
                img_url = img["srcset"].split("?")[0]

                anchor = figures[i].find("a", class_="rEAWd")

                if anchor and "href" in anchor.attrs:
                    download_url = "https://unsplash.com" + anchor["href"]
                    display_image_and_button(i, img_url, download_url, col1, col2, index)
                else:
                    st.warning("Link de download não encontrado para a imagem.")
            else:
                st.warning("URL da imagem não encontrada.")
    else:
        st.warning("Menos de duas imagens encontradas na linha.")

# Exibe a imagem e um botão para baixá-la
def display_image_and_button(i, img_url, download_url, col1, col2, index):
    if i == 0:
        col1.image(img_url)
        btn = col1.button("Download 📂", key=str(index) + str(i)) # Botão da 1° coluna
        if btn:
            web.open_new_tab(download_url)
    else:
        col2.image(img_url)
        btn = col2.button("Download 📂", key=str(index) + str(i)) # # Botão da 2° coluna
        if btn:
            web.open_new_tab(download_url)

main()