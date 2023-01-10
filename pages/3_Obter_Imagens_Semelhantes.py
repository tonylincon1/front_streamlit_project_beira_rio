import cv2
import time
import jsonpickle
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from Entrar import check_password
from outhers.detect_objet import *
from outhers.utils import load_image, criar_subimagem, plot_subimagem, predicao_imagens_semelhantes, predicao_classe

endereco = 'http://127.0.0.1:80'
url_predict_class = f'{endereco}/predict_class'
url_predict_similar = f'{endereco}/predict_recomendation_streamlit'
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
                    
        col7,col8 = st.columns(2)
        with col7:
            imagem_referencia = st.selectbox("Qual a imagem que deseja utilizar como referência?",
                                range(1,quant_detection+1))
        with col8:
            predicao_classe_button = st.button('Predição da Classe')
            @st.cache
            def botao_predicao_classe():
                return True
            predicao_classe_button = botao_predicao_classe()
            
        if predicao_classe_button:
                    
            st.markdown("***")
            predict_class = predicao_classe(foto_com_detectada,imagem_referencia,url_predict_class,headers)
            predict_class = predict_class.text[1:-1]
            
            col9,col10 = st.columns(2)
            
            with col9:
                criar_subimagem(foto_com_detectada[imagem_referencia-1],imagem_referencia)
            
            with col10:
                st.markdown(f"<p class='avaliacao'>A classe predita foi = <strong>{predict_class}</strong></p>", unsafe_allow_html=True)
                decisao_class = st.selectbox(f"Deseja manter a classificação ({predict_class})?",
                                        ('Sim', 'Não'))
                if decisao_class == 'Não':
                    predict_class = st.selectbox("Qual classe mais representa essa imagem?",
                                        ('BOTAS','CASUAL ESPORTIVO FEMININO','CASUAL ESPORTIVO MASCULINO',
                                            'ESPORTIVO','FLATS','FUTEBOL','MOCASSIM','MOCHILA','RN','SANDÁLIAS',
                                            'SANDÁLIAS DE DEDO','SANDÁLIAS MASCULINAS','SAPATILHAS','SAPATOS',
                                            'SCARPINS','SHOPPER','TIRACOLO','TOTE'))
            
                escala_semelhanca = st.selectbox("Escala de semelhança? (Quanto menor o valor, mais próxima a imagem é da enviada)",
                                    (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9), index=2)
                recomendacao = st.selectbox("Deseja considerar o sistema de recomendação?",
                                    ('Sim', 'Não'))
                my_slot1 = st.empty()
                notas = my_slot1.selectbox("Imagens semelhantes com avaliações iguais a?",
                                        (1,2,3,4,5),index=2)
                if recomendacao == 'Não':
                    notas = 1
                    my_slot1.empty()
                
                predicao_semelhantes = st.button('Predição da Imagens Semelhantes')
                @st.cache
                def botao_predicao_imagens_semelhantes():
                    return True
                predicao_semelhantes = botao_predicao_imagens_semelhantes()
                    
            if predicao_semelhantes:
                        
                predict_ia = predicao_imagens_semelhantes(foto_com_detectada,imagem_referencia,escala_semelhanca,recomendacao,notas,predict_class,url_predict_similar,headers)
                    
                if predict_ia.status_code == 200:
                    predict_ia = jsonpickle.decode(predict_ia.text)
                    classe = predict_ia[0][1]
                    predict_ia = predict_ia[1:]
                    predict_ia = pd.DataFrame(predict_ia).iloc[pd.DataFrame(predict_ia).iloc[:,0].drop_duplicates().index]
                    predict_ia = predict_ia.to_numpy()
                    quantas_imagens = len(predict_ia)
                    st.markdown("***")
                    st.markdown(f"<h5 style='text-align:left'>Aqui estão as {len(predict_ia)} imagens semelhantes: <br></h5>", unsafe_allow_html=True)
                    st.markdown(f"""<p class="observacao_predicao" style='text-align:left;'>*Atenção: Caso as predição tenham muitas imagens que não são semelhantes a imagem enviada, isso significa que não temos imagens parecidas no banco de dados que foi utilizado para treinar a inteligência artifical e as imagens que foram devolvidas são imagens "mais próximas" da atual.<br></p>""", unsafe_allow_html=True)
                    df_predict_ia = pd.DataFrame(predict_ia).rename(columns=({0:"Imagem",
                                                                              1:"Classe Predita",
                                                                              2:"Confiança da Classe Predita",
                                                                              3:"Escala de Semelhança",
                                                                              4:"Link da Imagem",
                                                                              5:"Data"}))
                    st.dataframe(df_predict_ia)
                    
                    contador = 1
                    if int(quantas_imagens) > 0 and int(quantas_imagens) < 50:
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
