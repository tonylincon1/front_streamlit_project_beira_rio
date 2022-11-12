import streamlit as st
import numpy as np
from PIL import Image
from outhers.detect_objet import *
import requests
import jsonpickle
from Entrar import check_password

url_color = 'http://127.0.0.1:5000/predict_recomendation'
url_gray = 'http://127.0.0.1:5000/predict_recomendation_gray'
content_type = 'image/jpeg'
headers = {'content-type': content_type}

def load_image(image_file):
    img = Image.open(image_file)
    return img

def criar_subimagem(predict,contador):
    st.markdown(f"<h6 style='text-align:center'>Essa é a detecão: {contador} <br></h6>", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict).astype(np.uint8))
    st.image(pilImage)

st.set_page_config(
    page_title="Predições",
    page_icon="👞",
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

if check_password():
    st.markdown("""<h1 style="text-align:center">Obter Imagens Semelhantes</h1>""", unsafe_allow_html=True)
    st.markdown("***")

    st.markdown("<h3>1) Importe aqui a imagem dos seus calçados 👞<br></h3>", unsafe_allow_html=True)

    foto_predict = st.file_uploader("Selecione a foto que deseja", type=['png', 'jpg'], accept_multiple_files=False)

    if foto_predict:
        st.markdown(f"<h5 style='text-align:center'>Você importou a imagem: {foto_predict.name}<br></h5>", unsafe_allow_html=True)
        st.image(foto_predict, width=500)
        foto_predict = np.array(load_image(foto_predict))
        
        #Retorno detecção
        foto_com_detectada = trat_detect_objet_extract(foto_predict)
        quant_detection = len(foto_com_detectada)
        st.markdown(f"<h5 style='text-align:left'>Foram detectados {quant_detection} objetos, Esses foram os objetos detectados: <br></h5>", unsafe_allow_html=True)
        
        col1,col2 = st.columns(2)
        col3,col4 = st.columns(2)
        col5,col6 = st.columns(2)
        contador = 1
        
        for predict in foto_com_detectada:
            if contador == 1:
                with col1:
                    criar_subimagem(predict,contador)
                    contador = contador + 1
            elif contador == 2:
                with col2:
                    criar_subimagem(predict,contador)
                    contador = contador + 1
            elif contador == 3:
                with col3:
                    criar_subimagem(predict,contador)
                    contador = contador + 1
            elif contador == 4:
                with col4:
                    criar_subimagem(predict,contador)
                    contador = contador + 1
            elif contador == 5:
                with col5:
                    criar_subimagem(predict,contador)
                    contador = contador + 1
            elif contador == 6:
                with col6:
                    criar_subimagem(predict,contador)
                    contador = contador + 1
        
        col7,col8 = st.columns(2)
        with col7:
            imagem_referencia = st.selectbox("Qual a imagem que deseja utilizar como referência?",
                                range(1,quant_detection+1))
        with col8:
            quantas_imagens = st.selectbox("Quantas imagens de referência deseja?",
                                (5, 10, 20, 30, 40, 50))
        
        if st.button("Enviar"):
            _, img_encoded = cv2.imencode('.jpg', foto_com_detectada[imagem_referencia-1])
            lista_envio = [quantas_imagens,img_encoded]
            predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
            if predict_ia.status_code == 200:
                predict_ia = jsonpickle.decode(predict_ia.text)
                for image in predict_ia:
                    st.markdown(image)
                    image_api = Image.fromarray((image).astype(np.uint8))
                    st.image(image_api)
            else:
                st.markdown(f"<h5 style='text-align:center; color:red'>Olá, houve algum problema, por favor contacte o administrador!<br></h5>", unsafe_allow_html=True)
            
            _, img_encoded = cv2.imencode('.jpg', foto_com_detectada[imagem_referencia-1])
            img_encoded=img_encoded.reshape(224,224,1)
            lista_envio = [quantas_imagens,img_encoded]
            predict_ia = requests.post(url_gray, data=jsonpickle.encode(lista_envio), headers=headers)
            if predict_ia.status_code == 200:
                predict_ia = jsonpickle.decode(predict_ia.text)
                for image in predict_ia:
                    st.markdown(image)
                    image_api = Image.fromarray((image).astype(np.uint8))
                    st.image(image_api)
            else:
                st.markdown(f"<h5 style='text-align:center; color:red'>Olá, houve algum problema, por favor contacte o administrador!<br></h5>", unsafe_allow_html=True)
