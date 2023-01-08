import cv2
import time
import jsonpickle
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from Entrar import check_password
from outhers.detect_objet import *
from outhers.utils import load_image, criar_subimagem, plot_subimagem, predicao_imagens_semelhantes

endereco = 'http://127.0.0.1:80'
url_color = f'{endereco}/predict_recomendation_streamlit'
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

if check_password():
    st.markdown("""<h1 style="text-align:center">Obter Imagens Semelhantes</h1>""", unsafe_allow_html=True)
    st.markdown("***")

    st.markdown("<h3>1) Importe aqui a imagem dos seus calçados 👞<br></h3>", unsafe_allow_html=True)

    foto_predict = st.file_uploader("Selecione a foto que deseja", type=['png', 'jpg', 'jpeg','jfif'], accept_multiple_files=False)

    if foto_predict:
        st.markdown(f"<h5 style='text-align:center'>Você importou a imagem: {foto_predict.name}<br></h5>", unsafe_allow_html=True)
        st.image(foto_predict, width=500)
        foto_predict = np.array(load_image(foto_predict))
        
        #Retorno detecção
        with st.spinner('Carregando Detecções'):
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
        
        col7,col8,col9 = st.columns(3)
        with col7:
            imagem_referencia = st.selectbox("Qual a imagem que deseja utilizar como referência?",
                                range(1,quant_detection+1))
        with col8:
            quantas_imagens = st.selectbox("Quantas imagens de referência deseja?",
                                (6, 10, 20, 30, 40, 50))
        with col9:
            recomendacao = st.selectbox("Deseja considerar o sistema de recomendação?",
                                ('Sim', 'Não'))
            notas = st.selectbox("Imagens semelhantes com avaliações iguais a?",
                                    (1,2,3,4,5),index=2)
                    
        predict_ia = predicao_imagens_semelhantes(foto_com_detectada,imagem_referencia,quantas_imagens,recomendacao,notas,url_color,headers)
            
        if predict_ia.status_code == 200:
            st.markdown("***")
            st.markdown(f"<h5 style='text-align:left'>Aqui estão as {int(quantas_imagens)} imagens semelhantes: <br></h5>", unsafe_allow_html=True)
            st.markdown(f"""<p class="observacao_predicao" style='text-align:left;'>*Atenção: Caso as predição tenham muitas imagens que não são semelhantes a imagem enviada, isso significa que não temos imagens parecidas no banco de dados que foi utilizado para treinar a inteligência artifical e as imagens que foram devolvidas são imagens "mais próximas" da atual.<br></p>""", unsafe_allow_html=True)
            predict_ia = jsonpickle.decode(predict_ia.text)
            st.dataframe(predict_ia)
            classe = predict_ia[0][1]
            print(classe)
            predict_ia = predict_ia[1:]
            
            contador = 1
            if int(quantas_imagens) == 6:
                plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia)
            elif int(quantas_imagens) == 10:
                plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,8,12,contador,foto_com_detectada,imagem_referencia)
            elif int(quantas_imagens) == 20:
                plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,8,12,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,12,16,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,16,20,contador,foto_com_detectada,imagem_referencia)
            elif int(quantas_imagens) == 30:
                plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,8,12,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,12,16,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,16,20,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,20,24,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,24,28,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,28,32,contador,foto_com_detectada,imagem_referencia)
            elif int(quantas_imagens) == 40:
                plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,8,12,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,12,16,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,16,20,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,20,24,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,24,28,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,28,32,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,32,36,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,36,40,contador,foto_com_detectada,imagem_referencia)
            elif int(quantas_imagens) == 50:
                plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,8,12,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,12,16,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,16,20,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,20,24,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,24,28,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,28,32,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,32,36,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,36,40,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,40,44,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,44,48,contador,foto_com_detectada,imagem_referencia)
                plot_subimagem(predict_ia,48,50,contador,foto_com_detectada,imagem_referencia)
            
        else:
            st.markdown(f"<h5 style='text-align:center; color:red'>Houve algum problema na predição. Por favor contacte o administrador!<br></h5>", unsafe_allow_html=True)
