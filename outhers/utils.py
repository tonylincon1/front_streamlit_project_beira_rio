import cv2
import requests
import jsonpickle
import numpy as np
from PIL import Image
import streamlit as st
from rembg import remove
from matplotlib import pyplot as plt
from outhers.conect_data import read_image_from_s3, envia_avaliacao_para_banco, salvar_avaliacoes_pkl


#Elementos Gerais
def process_image_download_file(image_file):
    pilImage = Image.fromarray((image_file).astype(np.uint8))
    st.markdown(pilImage)
    return pilImage

def load_image(image_file):
    img = Image.open(image_file)
    return img

def remove_background(image):
    try:
        image = Image.open(image)
        image = np.array(image)
        image = remove(image)
        image = np.copy(image)
        trans_mask = image[:,:,3] == 0
        image[trans_mask] = [255, 255, 255, 255]
    except:
        image = np.array(image)
        image = remove(image)
        image = np.copy(image)
        trans_mask = image[:,:,3] == 0
        image[trans_mask] = [255, 255, 255, 255]
    return image

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

#Detecção das Imagens Semelhantes
def gerar_uniao_de_imagens_horizontal(image_enviada,image_predita):
    im = np.vstack((image_enviada, image_predita))
    return im

def rename_class(imagem_name, classe_avaliacao,url_change_class,headers):
    lista_envio = [imagem_name,classe_avaliacao]
    requests.post(url_change_class, data=jsonpickle.encode(lista_envio), headers=headers)        
    
def criar_subimagem(predict,contador):
    st.markdown(f"<h6 style='text-align:center'>Essa é a detecção: {contador} <br></h6>", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict).astype(np.uint8))
    st.image(pilImage)

def criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia,url_change_class,headers):
    st.markdown(f"""<p style='text-align:center'>Imagem: {predict[0]}<br>Data: {predict[5].split(" ")[1] + '-' + predict[5].split(" ")[2] + '-' + predict[5].split(" ")[3]}<br>Escala de Semelhança: {round(predict[3],4)}</p>""", unsafe_allow_html=True)
    with st.spinner('Enviando Avaliação'):
        my_slot1 = st.empty()
        my_slot2 = st.empty()
        my_slot3 = st.empty()
        nota = my_slot1.selectbox("Nota (0 = Ruim, 1 = Boa)",[0,1],key=predict[0]+'_value')
        classe_avaliacao = my_slot2.selectbox(
            "Qual a classe dessa imagem?",
            [
                'CLASSE',
                'BOTAS',
                'CASUAL ESPORTIVO FEMININO',
                'CASUAL ESPORTIVO MASCULINO',
                'ESPORTIVO',
                'FLATS',
                'FUTEBOL',
                'MOCASSIM',
                'MOCHILA',
                'RN',
                'SANDALIAS',
                'SANDALIAS DE DEDO',
                'SANDALIAS MASCULINAS',
                'SAPATILHAS',
                'SAPATOS',
                'SCARPINS',
                'SHOPPER',
                'TIRACOLO',
                'TOTE',
            ],
            key=f'{predict[0]}+_classe',
            )
        botao_avaliacao = my_slot3.button('Avaliar Predição',key=predict[0]+'_button')
        st.markdown(f""" <img class="image_predict" src="{predict[4]}">""", unsafe_allow_html=True)
        
        if botao_avaliacao:
            image_enviada = foto_com_detectada[imagem_referencia-1]
            image_predita = read_image_from_s3("beirario-imagens",predict[0])
            fig = gerar_uniao_de_imagens(image_enviada,image_predita)
            salvar_avaliacoes_pkl(fig,nota)
            my_slot1.empty(), my_slot2.empty(), my_slot3.empty()
            if classe_avaliacao != 'CLASSE':
                rename_class(predict[0],classe_avaliacao,url_change_class,headers)
            st.markdown("<p class='avaliacao'>✅ Avaliação enviada!</p>", unsafe_allow_html=True)
            #envia_avaliacao_para_banco(array_imagem_reduzido,nota)
        
def plot_subimagem(predict_ia,init,fim,contador,foto_com_detectada,imagem_referencia,url_change_class,headers):
    col9,col10,col11,col12 = st.columns(4)
    for predict in predict_ia[init:fim]:
        if contador == 1:
            with col9:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia,url_change_class,headers)
                contador = contador + 1
        elif contador == 2:
            with col10:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia,url_change_class,headers)
                contador = contador + 1
        elif contador == 3:
            with col11:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia,url_change_class,headers)
                contador = contador + 1
        elif contador == 4:
            with col12:
                criar_subimagem_predict(predict,contador,foto_com_detectada,imagem_referencia,url_change_class,headers)
                contador = contador + 1
               
@st.cache
def predicao_imagens_semelhantes(foto_com_detectada,imagem_referencia,escala_semelhanca,recomendacao,class_predict,decisao_class,url_color,headers):
    with st.spinner('Carregando Imagens Semelhantes (Esse processo pode demorar de 4 a 10 minutos)'):
        image = foto_com_detectada[imagem_referencia-1]
        _, img_encoded = cv2.imencode('.jpg', image)
        lista_envio = [escala_semelhanca,img_encoded,recomendacao,class_predict,decisao_class]
        predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
        return predict_ia
    
@st.cache
def predicao_classe(foto_com_detectada,imagem_referencia,url_color,headers):
    with st.spinner('Carregando Predição da Classe'):
        """
        Função para realizar a predição da classe de uma imagem utilizando uma rede neural treinada.

        Argumentos:
        foto_com_detectada: lista de imagens onde a detecção foi realizada.
        imagem_referencia: inteiro indicando qual imagem da lista deve ser utilizada para a predição.
        url_color: string com a url da API para realizar a predição.
        headers: dicionário com os headers necessários para a chamada da API.

        Retorno:
        Um json com a predição da classe.
        """
        image = foto_com_detectada[imagem_referencia-1]
        _, img_encoded = cv2.imencode('.jpg', image)
        lista_envio = img_encoded
        predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
        return predict_ia
    
@st.cache
def criar_nomes_imagens(foto_com_detectada,quant_imagens,url_color,headers):
    with st.spinner('Carregando Predição da Classe (Esse processo pode demorar de 4 a 10 minutos)'):
        _, img_encoded = cv2.imencode('.jpg', foto_com_detectada)
        lista_envio = [img_encoded,quant_imagens]
        predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
        return predict_ia