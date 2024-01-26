# Importando as dependências
import streamlit as st
import requests as rq
from bs4 import BeautifulSoup
import webbrowser as web


def page():
    st.set_page_config(
        page_title="Web Scraper Image",
        page_icon="src\img\ico.png",
        layout="wide",
        menu_items={
            'Report a bug': "https://github.com/SidneyTeodoroJr",
            'About': "https://github.com/SidneyTeodoroJr/Web_Scraper_Image"
        }
    )
page()

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

st.markdown('<h1 class="title">Web Scraper Image 📷</h1>', unsafe_allow_html=True)
def main():
    with st.form("search"):
        keyword = st.text_input("search", "landscape")
        st.form_submit_button("GO")

    if keyword:
        try:
            page = get_page(keyword)
            if page is not None:
                process_page(page)
        except Exception as e:
            st.error(f"Ocorreu um erro durante a execução: {e}")

def get_page(keyword):
    response = rq.get(f"https://unsplash.com/pt-br/s/fotografias/{keyword}")

    if response.status_code == 200:
        return response.content
    else:
        st.warning(f"Falha na requisição. Código de status: {response.status_code}")
        return None

def process_page(page_content):
    soup = BeautifulSoup(page_content, "lxml")
    rows = soup.find_all("div", class_="ripi6")
    placeholder = st.empty()
    col1, col2 = placeholder.columns(2)

    for index, row in enumerate(rows):
        process_row(row, index, col1, col2)

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

def display_image_and_button(i, img_url, download_url, col1, col2, index):
    if i == 0:
        col1.image(img_url)
        btn = col1.button("Download 📂", key=str(index) + str(i))
        if btn:
            web.open_new_tab(download_url)
    else:
        col2.image(img_url)
        btn = col2.button("Download 📂", key=str(index) + str(i))
        if btn:
            web.open_new_tab(download_url)

if __name__ == "__main__":
    main()