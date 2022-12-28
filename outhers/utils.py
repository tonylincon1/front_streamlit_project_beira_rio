import cv2
import boto3
import requests
import jsonpickle
import numpy as np
from PIL import Image
import streamlit as st
from matplotlib import pyplot as plt

#Elementos Gerais

def process_image_download_file(image_file):
    pilImage = Image.fromarray((image_file).astype(np.uint8))
    st.markdown(pilImage)
    return pilImage

def load_image(image_file):
    img = Image.open(image_file)
    return img

def read_image_from_s3(bucket, key):
    """Load image file from s3.

    Parameters
    ----------
    bucket: string
        Bucket name
    key : string
        Path in s3

    Returns
    -------
    np array
        Image array
    """
    session = boto3.Session(aws_access_key_id="AKIA4NNAOZHLTIHZSIRV",aws_secret_access_key="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")
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket)
    object = bucket.Object(key)
    response = object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    im = np.array(im).astype(np.uint8)
    im = cv2.resize(im, (224,224))
    return im

#Detecção das Imagens Semelhantes

def gerar_uniao_de_imagens(image_enviada,image_predita):
    images = [image_enviada.astype(np.uint8),image_predita]
    fig, axes = plt.subplots(1,2, figsize=(5,5))
    for i,ax in enumerate(axes.flat):
        ax.imshow(images[i])
        ax.axis('off')
    fig.canvas.draw()
    im = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    #Verificar como transformar imagem plt em array
    return im
    
def criar_subimagem(predict,contador):
    st.markdown(f"<h6 style='text-align:center'>Essa é a detecão: {contador} <br></h6>", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict).astype(np.uint8))
    st.image(pilImage)

def criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia):
    st.markdown(f"""<p style='text-align:center'>Imagem: {predict[0]}<br>Data: {predict[2].split(" ")[1] + '-' + predict[2].split(" ")[2] + '-' + predict[2].split(" ")[3]}<br></p>""", unsafe_allow_html=True)
    nota = st.selectbox("Nota (1 = Ruim e 5 = Ótima)",[1,2,3,4,5],key=predict[0]+'_value')
    botao_avaliacao = st.button('Avaliar Predição',key=predict[0]+'_button')
    #pilImage = Image.fromarray((predict[1]).astype(np.uint8))
    st.markdown(f""" <img class="image_predict" src="{predict[1]}">""", unsafe_allow_html=True)
    
    if botao_avaliacao:
        st.markdown(predict[0], unsafe_allow_html=True)
        image_enviada = foto_com_detectada[imagem_referencia-1]
        image_predita = read_image_from_s3("beirario-imagens",predict[0])
        fig = gerar_uniao_de_imagens(image_enviada,image_predita)
        st.markdown(fig.shape)
        #Transformar imagem em array
        #Reduzir dimensionalidade da imagem
        #Enviar array da imagem + nota avaliada para banco ou armazenamento previo
        st.markdown(nota, unsafe_allow_html=True)
        
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
def predicao_imagens_semelhantes(foto_com_detectada,imagem_referencia,quantas_imagens,url_color,headers):
    with st.spinner('Carregando Imagens Semelhantes'):
        _, img_encoded = cv2.imencode('.jpg', foto_com_detectada[imagem_referencia-1])
        lista_envio = [quantas_imagens,img_encoded]
        predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
        return predict_ia