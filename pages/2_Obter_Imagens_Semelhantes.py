import jsonpickle
import numpy as np
import pandas as pd
import streamlit as st
from outhers.detect_objet import *
from outhers.utils import load_image, criar_subimagem, plot_subimagem, predicao_imagens_semelhantes, predicao_classe, check_password

endereco = 'http://127.0.0.1:80'
url_predict_class = f'{endereco}/predict_class'
url_predict_similar = f'{endereco}/predict_recomendation'
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

if 'botao_1' not in st.session_state:
    st.session_state['botao_1'] = False
if 'botao_2' not in st.session_state:
    st.session_state['botao_2'] = False
    
def write_variable():
    st.session_state['botao_1'] = False
    st.session_state['botao_2'] = False

if check_password():
    st.markdown("""<h1 style="text-align:center">Obter Imagens Semelhantes</h1>""", unsafe_allow_html=True)
    st.markdown("***")

    st.markdown("<h3>1) Importe aqui a imagem dos seus calçados 👞<br></h3>", unsafe_allow_html=True)
    
    foto_predict = st.file_uploader("Selecione a foto que deseja", type=['png', 'jpg', 'jpeg','jfif'], accept_multiple_files=False, on_change=write_variable)

    if foto_predict:
        st.markdown(f"<h5 style='text-align:center'>Você importou a imagem: {foto_predict.name}<br></h5>", unsafe_allow_html=True)
        st.image(foto_predict, width=600)
        foto_predict = np.array(load_image(foto_predict))
        remove_background_image = st.selectbox("Deseja remover o background da imagem?",
                                                ('Sim','Não'),index=0)
        st.markdown("***")
        
        #Retorno detecção
        with st.spinner('Carregando Detecções'):
            foto_com_detectada = trat_detect_objet_extract(foto_predict,remove_background_image)
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
                    
        imagem_referencia = st.selectbox("Qual a imagem que deseja utilizar como referência?",
                            range(1,quant_detection+1))
        if st.button("Predição da Classe"):
            st.session_state.botao_1 = True
        if st.session_state.botao_1:
            st.markdown("***")
            predict_class = predicao_classe(foto_com_detectada,imagem_referencia,url_predict_class,headers)
            predict_class = predict_class.text[1:-1]
            
            col9,col10 = st.columns(2)
            
            with col9:
                criar_subimagem(foto_com_detectada[imagem_referencia-1],imagem_referencia)
            
            with col10:
                st.markdown(f"<p class='avaliacao' style='font-size:45px'>A classe predita foi = <strong>{predict_class}</strong></p>", unsafe_allow_html=True)
                decisao_class = st.selectbox(f"Deseja manter a classificação ({predict_class}) ou fazer uma busca por semelhantes em uma classe especifica?",
                                        ('Sim', 'Não'))
                if decisao_class == 'Não':
                    predict_class = st.selectbox("Qual classe mais representa essa imagem?",
                                        ('BOTAS','CASUAL ESPORTIVO FEMININO','CASUAL ESPORTIVO MASCULINO',
                                            'ESPORTIVO','FLATS','FUTEBOL','MOCASSIM','MOCHILA','RN','SANDALIAS',
                                            'SANDALIAS DE DEDO','SANDALIAS MASCULINAS','SAPATILHAS','SAPATOS',
                                            'SCARPINS','SHOPPER','TIRACOLO','TOTE'))
            
                escala_semelhanca = st.slider("Escala de semelhança? (Quanto maior o valor, mais próxima a imagem é da enviada, abaixo de 0.88 já temos pouca semelhança)", 0.5, 0.99, value=0.88)
                recomendacao = st.selectbox("Deseja considerar o sistema de recomendação?",
                                    ('Sim', 'Não'), index=0)
                
                if st.button('Predição da Imagens Semelhantes'):
                    st.session_state.botao_2 = True
                    
            if st.session_state.botao_2:
                predict_ia = predicao_imagens_semelhantes(foto_com_detectada,imagem_referencia,escala_semelhanca,recomendacao,predict_class,decisao_class,url_predict_similar,headers)
                if predict_ia.status_code == 200:
                    predict_ia = jsonpickle.decode(predict_ia.text)
                    if len(predict_ia) > 0:
                        classe = predict_ia[0][1]
                        predict_ia = predict_ia
                        predict_ia = pd.DataFrame(predict_ia).iloc[pd.DataFrame(predict_ia).iloc[:,0].drop_duplicates().index]
                        predict_ia = predict_ia.to_numpy()
                        quantas_imagens = len(predict_ia)
                        
                        st.markdown("***")
                        st.markdown(f"<h5 style='text-align:left'>Aqui estão as {len(predict_ia)} imagens semelhantes: <br></h5>", unsafe_allow_html=True)
                        df_predict_ia = pd.DataFrame(predict_ia).rename(columns=({0:"Imagem",
                                                                                    1:"Classe Predita",
                                                                                    2:"Confiança da Classe Predita",
                                                                                    3:"Escala de Semelhança",
                                                                                    4:"Link da Imagem",
                                                                                    5:"Data"}))
                        st.dataframe(df_predict_ia)
                        contador = 1
                        if int(quantas_imagens) > 0 and int(quantas_imagens) < 50:
                            plot_subimagem(predict_ia,0,4,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,4,8,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,8,12,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,12,16,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,16,20,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,20,24,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,24,28,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,28,32,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,32,36,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,36,40,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,40,44,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,44,48,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                            plot_subimagem(predict_ia,48,50,contador,foto_com_detectada,imagem_referencia,url_change_class_image,headers)
                    else:
                        st.markdown(f"<h5 style='text-align:center; color:red'>Não existem imagens semelhantes para a escala de semelhança de {escala_semelhanca} para essa imagem!<br></h5>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h5 style='text-align:center; color:red'>Houve algum problema na predição ou não existem imagens semelhantes para essa imagem. Por favor contacte o administrador!<br></h5>", unsafe_allow_html=True)