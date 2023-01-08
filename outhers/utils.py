import cv2
import keras
import requests
import jsonpickle
import numpy as np
from PIL import Image
import streamlit as st
from numpy import expand_dims
from matplotlib import pyplot as plt
from outhers.conect_data import read_image_from_s3, envia_avaliacao_para_banco, salvar_avaliacoes_pkl
from matplotlib.backends.backend_agg import FigureCanvasAgg


#Elementos Gerais
def process_image_download_file(image_file):
    pilImage = Image.fromarray((image_file).astype(np.uint8))
    st.markdown(pilImage)
    return pilImage

def load_image(image_file):
    img = Image.open(image_file)
    return img

#Detecção das Imagens Semelhantes
def gerar_uniao_de_imagens(image_enviada,image_predita):
    images = [image_enviada.astype(np.uint8),image_predita]
    fig, axes = plt.subplots(1,2, figsize=(2.24,2.24))
    for i,ax in enumerate(axes.flat):
        ax.imshow(images[i])
        ax.axis('off')
    fig.canvas.draw()
    im = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    im = im.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    return im
    
def criar_subimagem(predict,contador):
    st.markdown(f"<h6 style='text-align:center'>Essa é a detecão: {contador} <br></h6>", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict).astype(np.uint8))
    st.image(pilImage)

def criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia):
    print(predict)
    st.markdown(f"""<p style='text-align:center'>Imagem: {predict[0]}<br>Data: {predict[4].split(" ")[1] + '-' + predict[4].split(" ")[2] + '-' + predict[4].split(" ")[3]}<br></p>""", unsafe_allow_html=True)
    with st.spinner('Enviando Avaliação'):
        my_slot1 = st.empty()
        my_slot2 = st.empty()
        nota = my_slot1.selectbox("Nota (1 = Ruim, 3 = Aceitável e 5 = Ótima)",[1,2,3,4,5],key=predict[0]+'_value')
        botao_avaliacao = my_slot2.button('Avaliar Predição',key=predict[0]+'_button')
        st.markdown(f""" <img class="image_predict" src="{predict[3]}">""", unsafe_allow_html=True)
        
        if botao_avaliacao:
            image_enviada = foto_com_detectada[imagem_referencia-1]
            image_predita = read_image_from_s3("beirario-imagens",predict[0])
            fig = gerar_uniao_de_imagens(image_enviada,image_predita)
            salvar_avaliacoes_pkl(fig,nota)
            my_slot1.empty(), my_slot2.empty()
            st.markdown("<p class='avaliacao'>✅ Avaliação enviada!</p>", unsafe_allow_html=True)
            #envia_avaliacao_para_banco(array_imagem_reduzido,nota)
        
def plot_subimagem(predict_ia,init,fim,contador,foto_com_detectada,imagem_referencia):
    col9,col10,col11,col12 = st.columns(4)
    for predict in predict_ia[init:fim]:
        if contador == 1:
            with col9:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia)
                contador = contador + 1
        elif contador == 2:
            with col10:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia)
                contador = contador + 1
        elif contador == 3:
            with col11:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia)
                contador = contador + 1
        elif contador == 4:
            with col12:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia)
                contador = contador + 1
                
@st.cache
def predicao_imagens_semelhantes(foto_com_detectada,imagem_referencia,quantas_imagens,recomendacao,notas,url_color,headers):
    with st.spinner('Carregando Imagens Semelhantes'):
        _, img_encoded = cv2.imencode('.jpg', foto_com_detectada[imagem_referencia-1])
        lista_envio = [quantas_imagens,img_encoded,recomendacao,notas]
        predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
        return predict_ia