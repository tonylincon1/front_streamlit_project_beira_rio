import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from Entrar import check_password

st.set_page_config(
    page_title="Sobre o Projeto",
    page_icon="👞",
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.image("files/images/logo.png", use_column_width=True)
    
if check_password():
    
    st.markdown("""<h1 style="text-align:center">Projeto Beira Rio <br> IA para Reconhecimento de Imagens</h1>""", unsafe_allow_html=True)
    st.markdown("***")

    st.markdown("<h3>1) Objetivo 👞<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">O projeto trata-se do desenvolvimento de um algoritmo para reconhecimento de calçados semelhantes. Para isso foi utilizada técnicas de tratamento e padronização de imagens, modelos de machine learning e deep learning e outras ferramentas de desenvolvimento web.</p>""", unsafe_allow_html=True)

    st.markdown("<h3>2) Etapas de Desenvolvimento 👠<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Para o desenvolvimento do projeto, foram seguidas as seguintes etapas:</p>""", unsafe_allow_html=True)
    st.markdown("""
                <ul style='list-style-type:decimal'>
                    <li>Conhecimento e tratamento da banco de imagens;</li>
                    <li>Limpeza do banco de imagens;</li>
                    <li>Desenvolvimento do algoritmo de extração de características e clusterização;</li>
                    <li>Implantação e testes.</li>
                </ul>""", unsafe_allow_html=True)

    st.markdown("<h3>3) Parceria 🥾<br></h3>", unsafe_allow_html=True)
    image = Image.open('files/images/parceria.png')
    st.image(image)
    st.markdown("")