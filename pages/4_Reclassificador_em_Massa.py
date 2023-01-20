import cv2
import time
import jsonpickle
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from outhers.utils import check_password, plot_image_class
from outhers.conect_data import select_table

endereco = 'http://54.83.166.236'
url_change_class_image = f'{endereco}/change_class_image'
content_type = 'image/jpeg'
headers = {'content-type': content_type}

st.set_page_config(
    page_title="Predições",
    page_icon="👞",
    initial_sidebar_state="collapsed",
    layout="wide"
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.image("files/images/logo.png", use_column_width=True)

if 'reclassificacao_1' not in st.session_state:
    st.session_state['reclassificacao_1'] = False
if 'data_class' not in st.session_state:
    st.session_state['data_class'] = None

def write_variable():
    st.session_state.reclassificacao_1 = False
    st.session_state['data_class'] = None

if check_password():
    st.markdown("""<h1 style="text-align:center">Reclassificador em Massa</h1>""", unsafe_allow_html=True)
    st.markdown("***")
    
    predict_class = st.selectbox("Qual classe de imagens deseja reclassificar?",
                                        ('BOTAS','CASUAL ESPORTIVO FEMININO','CASUAL ESPORTIVO MASCULINO',
                                            'ESPORTIVO','FLATS','FUTEBOL','MOCASSIM','MOCHILA','RN','SANDALIAS',
                                            'SANDALIAS DE DEDO','SANDALIAS MASCULINAS','SAPATILHAS','SAPATOS',
                                            'SCARPINS','SHOPPER','TIRACOLO','TOTE', 'NÃO É CALÇADO'),on_change=write_variable)

    if st.button('Imagens Classificadas'):
        st.session_state.reclassificacao_1 = True
        data = select_table("chicod46_imagens_beirario.shoe_class")
        st.session_state.data_class = data
        
    if st.session_state.reclassificacao_1:
        data = st.session_state.data_class
        data = data.rename(columns=({0:'nome',
                                    1:'clases_1'}))
        data = data.query(f"clases_1 == '{predict_class}'")
        data["link"] = data.nome.apply(lambda linha: f"https://dog5o645uha8q.cloudfront.net/{linha}")
        st.metric(label="Imagens", value=f"{data.shape[0]}")
        max_pages = int(round(data.shape[0]/50,0))
        if max_pages < 1:
            max_pages = 1
        quantidade = st.selectbox("Qual a página deseja buscar?",
                            range(max_pages),index=0)
        if quantidade == 0:
            data = data.iloc[0:50]
            st.metric(label="Imagem Inicial", value="0")
            st.metric(label="Imagem Final", value=f"{data.shape[0]}")
        else:
            data = data.iloc[50*quantidade:50*(quantidade+1)]
            st.metric(label="Imagem Inicial", value=f"{50*quantidade}")
            st.metric(label="Imagem Final", value=f"{50*(quantidade+1)}")
        
        st.dataframe(data)
        
        tamanho = len(data)
        contador = 0
        while contador < tamanho:
            linhas = data.iloc[contador:contador+8]
            plot_image_class(linhas,url_change_class_image,headers)
            contador += 8
            