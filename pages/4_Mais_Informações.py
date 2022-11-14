import streamlit as st
import pandas as pd
import numpy as np
import base64
from Entrar import check_password

st.set_page_config(
    page_title="Mais Informações",
    page_icon="👞",
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.image("files/images/logo.png", use_column_width=True)    

if check_password():
    st.markdown("""<h1 style="text-align:center">Mais Informações</h1>""", unsafe_allow_html=True)
    st.markdown("***")

    st.markdown("""<p style="text-align:justify">Para obter mais informações sobre o projeto, temos nessa seção o material consolidado para consulta.</p>""", unsafe_allow_html=True)

    st.markdown("<h3>Material Complementar 👞<br></h3>", unsafe_allow_html=True)
    with open("files/Projeto Beira Rio - IA para Reconhecimento de Imagens.pdf","rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="500" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    st.markdown("***")
    st.markdown("""<p style="text-align:justify">Estamos a disposição e podem entrar em contato via oficial@insidergic.com.br</p>""", unsafe_allow_html=True)