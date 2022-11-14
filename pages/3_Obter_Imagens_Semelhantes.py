import streamlit as st
import numpy as np
from PIL import Image
from outhers.detect_objet import *
import requests
import jsonpickle
from Entrar import check_password

endereco = 'http://e84a-34-122-72-86.ngrok.io'
url_color = f'{endereco}/predict_recomendation'
url_gray = f'{endereco}/predict_recomendation_gray'
content_type = 'image/jpeg'
headers = {'content-type': content_type}

def load_image(image_file):
    img = Image.open(image_file)
    return img

def criar_subimagem(predict,contador):
    st.markdown(f"<h6 style='text-align:center'>Essa é a detecão: {contador} <br></h6>", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict).astype(np.uint8))
    st.image(pilImage)
    
def criar_subimagem_predict(predict,contador):
    st.markdown(f"""<p style='text-align:center'>Imagem: {predict[0]}<br>Data: {predict[2].split(" ")[1] + '-' + predict[2].split(" ")[2] + '-' + predict[2].split(" ")[3]}<br></p>""", unsafe_allow_html=True)
    pilImage = Image.fromarray((predict[1]).astype(np.uint8))
    st.image(pilImage)

def plot_subimagem(predict_ia,init,fim,contador):
    col9,col10,col11,col12 = st.columns(4)
    for predict in predict_ia[init:fim]:
        if contador == 1:
            with col9:
                criar_subimagem_predict(predict,contador)
                contador = contador + 1
        elif contador == 2:
            with col10:
                criar_subimagem_predict(predict,contador)
                contador = contador + 1
        elif contador == 3:
            with col11:
                criar_subimagem_predict(predict,contador)
                contador = contador + 1
        elif contador == 4:
            with col12:
                criar_subimagem_predict(predict,contador)
                contador = contador + 1

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
                                (6, 10, 20, 30, 40, 50))
        
        if st.button("Obter Imagens Semelhantes"):
            _, img_encoded = cv2.imencode('.jpg', foto_com_detectada[imagem_referencia-1])
            lista_envio = [quantas_imagens,img_encoded]
            predict_ia = requests.post(url_color, data=jsonpickle.encode(lista_envio), headers=headers)
            if predict_ia.status_code == 200:
                st.markdown("***")
                st.markdown(f"<h5 style='text-align:left'>Aqui estão as {int(quantas_imagens)} imagens semelhantes nos aspectos de <u style='color:red;'>cor e formato</u>: <br></h5>", unsafe_allow_html=True)
                predict_ia = jsonpickle.decode(predict_ia.text)
                
                contador = 1
                if int(quantas_imagens) == 6:
                    plot_subimagem(predict_ia,0,4,contador)
                    plot_subimagem(predict_ia,4,8,contador)
                elif int(quantas_imagens) == 10:
                    plot_subimagem(predict_ia,0,4,contador)
                    plot_subimagem(predict_ia,4,8,contador)
                    plot_subimagem(predict_ia,8,12,contador)
                elif int(quantas_imagens) == 20:
                    plot_subimagem(predict_ia,0,4,contador)
                    plot_subimagem(predict_ia,4,8,contador)
                    plot_subimagem(predict_ia,8,12,contador)
                    plot_subimagem(predict_ia,12,16,contador)
                    plot_subimagem(predict_ia,16,20,contador)
                elif int(quantas_imagens) == 30:
                    plot_subimagem(predict_ia,0,4,contador)
                    plot_subimagem(predict_ia,4,8,contador)
                    plot_subimagem(predict_ia,8,12,contador)
                    plot_subimagem(predict_ia,12,16,contador)
                    plot_subimagem(predict_ia,16,20,contador)
                    plot_subimagem(predict_ia,20,24,contador)
                    plot_subimagem(predict_ia,24,28,contador)
                    plot_subimagem(predict_ia,28,32,contador)
                elif int(quantas_imagens) == 40:
                    plot_subimagem(predict_ia,0,4,contador)
                    plot_subimagem(predict_ia,4,8,contador)
                    plot_subimagem(predict_ia,8,12,contador)
                    plot_subimagem(predict_ia,12,16,contador)
                    plot_subimagem(predict_ia,16,20,contador)
                    plot_subimagem(predict_ia,20,24,contador)
                    plot_subimagem(predict_ia,24,28,contador)
                    plot_subimagem(predict_ia,28,32,contador)
                    plot_subimagem(predict_ia,32,36,contador)
                    plot_subimagem(predict_ia,36,40,contador)
                elif int(quantas_imagens) == 50:
                    plot_subimagem(predict_ia,0,4,contador)
                    plot_subimagem(predict_ia,4,8,contador)
                    plot_subimagem(predict_ia,8,12,contador)
                    plot_subimagem(predict_ia,12,16,contador)
                    plot_subimagem(predict_ia,16,20,contador)
                    plot_subimagem(predict_ia,20,24,contador)
                    plot_subimagem(predict_ia,24,28,contador)
                    plot_subimagem(predict_ia,28,32,contador)
                    plot_subimagem(predict_ia,32,36,contador)
                    plot_subimagem(predict_ia,36,40,contador)
                    plot_subimagem(predict_ia,40,44,contador)
                    plot_subimagem(predict_ia,44,48,contador)
                    plot_subimagem(predict_ia,48,50,contador)
                
            else:
                st.markdown(f"<h5 style='text-align:center; color:red'>Olá, houve algum problema, por favor contacte o administrador!<br></h5>", unsafe_allow_html=True)
