import streamlit as st
import numpy as np
from PIL import Image
from outhers.detect_objet import *

def load_image(image_file):
    img = Image.open(image_file)
    return img

def criar_subimagem(predict,contador):
    st.markdown(f"<h6 style='text-align:center'>Essa é a detecão: {contador} <br></h6>", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict * 1).astype(np.uint8)).convert('RGB')
    st.image(pilImage)

st.set_page_config(
    page_title="Predições",
    page_icon="👞",
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title('Predição de Calçados Semelhantes')
st.markdown("***")

st.markdown("<h3>Importe aqui a imagem dos seus calçados 👞<br></h3>", unsafe_allow_html=True)

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
    
    st.selectbox("Qual a imagem que deseja utilizar como referência?",
                range(1,quant_detection+1))
