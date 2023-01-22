import jsonpickle
from PIL import Image
import streamlit as st
import streamlit_analytics
from outhers.detect_objet import *
from outhers.utils import gerar_uniao_de_imagens_horizontal, criar_nomes_imagens, remove_background, check_password

endereco = 'http://generateimages.insidergic.com.br'
url_create_new_images = f'{endereco}/create_new_images'
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

streamlit_analytics.start_tracking()

if check_password():
    st.markdown("""<h1 style="text-align:center">Criador de Calçados</h1>""", unsafe_allow_html=True)
    st.markdown("""<h4 style="text-align:justify;color:red;">*Essa aba ficará funcional até o dia 16/02/2023. Para mais informações por favor entrar em contato com administrador.</h4>""", unsafe_allow_html=True)
    st.markdown("***")
    calcado_1_pre_tratado = False
    calcado_2_pre_tratado = False
    st.markdown("""<p style="text-align:justify">Essa aba foi criada para  criado um pipeline de GAN (rede geradora adversária) com o objetivo de gerar novas imagens de calçados a partir de duas imagens de calçados de entrada. Este processo foi aplicado com sucesso em projetos passados e tem sido usado como referência para projetos futuros.</p>""", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Algumas demonstrações do potencial do modelo de criação de novos calçados:</p>""", unsafe_allow_html=True)
    
    coldemo1,coldemo2 = st.columns(2)
    with coldemo1:
        st.markdown("""<p style="text-align:center"><strong>Combinando Características Duas Botas e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
        image = Image.open('files/images/Combinação de Calçados 1.png')
        st.image(image)
        st.markdown("""<p style="text-align:center"><strong>Combinando Características Dois Tênis Esportivos e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
        image = Image.open('files/images/Combinação de Calçados 2.png')
        st.image(image)
    with coldemo2:
        st.markdown("""<p style="text-align:center"><strong>Combinando Características Bota com Scarpin e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
        image = Image.open('files/images/Combinação de Calçados 3.png')
        st.image(image)
        st.markdown("""<p style="text-align:center"><strong>Combinando Características Dois Scarpins e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
        image = Image.open('files/images/Combinação de Calçados 4.png')
        st.image(image)

    st.markdown("***")
    
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<h3>1) Importe o primeiro calçado 👞<br></h3>", unsafe_allow_html=True)
        calcado_1 = st.file_uploader("Selecione a foto que deseja", type=['png', 'jpg', 'jpeg','jfif'], key='calcado_1', accept_multiple_files=False)
        if calcado_1:
            st.markdown(f"<h5 style='text-align:center'>Você importou a imagem: {calcado_1.name}<br></h5>", unsafe_allow_html=True)
            st.image(calcado_1)
            with st.spinner('Removendo Fundo da Imagem'):
                calcado_1 = remove_background(calcado_1)
            st.markdown(f"<h5 style='text-align:center'>Calçado sem Fundo<br></h5>", unsafe_allow_html=True)
            st.image(calcado_1)
            calcado_1_pre_tratado = True
    
    with col2:
        st.markdown("<h3>2) Importe o segundo calçado 👞<br></h3>", unsafe_allow_html=True)
        calcado_2 = st.file_uploader("Selecione a foto que deseja", type=['png', 'jpg', 'jpeg','jfif'], key='calcado_2', accept_multiple_files=False)
        if calcado_2:
            st.markdown(f"<h5 style='text-align:center'>Você importou a imagem: {calcado_2.name}<br></h5>", unsafe_allow_html=True)
            st.image(calcado_2)
            with st.spinner('Removendo Fundo da Imagem'):
                calcado_2 = remove_background(calcado_2)
            st.markdown(f"<h5 style='text-align:center'>Calçado sem Fundo<br></h5>", unsafe_allow_html=True)
            st.image(calcado_2)
            calcado_2_pre_tratado = True
            
    if calcado_1_pre_tratado == True and calcado_2_pre_tratado == True:
        st.markdown(f"<h5 style='text-align:center'>Calçados de Referência para Criação<br></h5>", unsafe_allow_html=True)
        im = gerar_uniao_de_imagens_horizontal(calcado_1,calcado_2)
        st.image(im, width=800)
        quant_imagens = st.selectbox(f"Quantas referências você precisa?",
                                        (1,2,3,4),index=1)
        criar_calcados = st.button('Criar Novas Referências')
        if criar_calcados:
            novos_calcados = criar_nomes_imagens(im,quant_imagens,url_create_new_images,headers)
            if novos_calcados.status_code == 200:
                novos_calcados = jsonpickle.decode(novos_calcados.text)
                if quant_imagens == 1:
                    st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 1<br></h5>", unsafe_allow_html=True)
                    st.image(novos_calcados[0])
                elif quant_imagens == 2:
                    col3,col4 = st.columns(2)
                    with col3:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 1<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[0])
                    with col4:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 2<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[1])
                elif quant_imagens == 3:
                    col3,col4 = st.columns(2)
                    with col3:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 1<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[0])
                    with col4:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 2<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[1])
                    st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 3<br></h5>", unsafe_allow_html=True)
                    st.image(novos_calcados[2])
                elif quant_imagens == 4:
                    col3,col4 = st.columns(2)
                    with col3:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 1<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[0])
                    with col4:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 2<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[1])
                    col5,col6 = st.columns(2)
                    with col5:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 3<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[2])
                    with col6:
                        st.markdown(f"<h5 style='text-align:center'>Novos Calçados Gerados: 4<br></h5>", unsafe_allow_html=True)
                        st.image(novos_calcados[3])
            else:
                    st.markdown(f"<h5 style='text-align:center; color:red'>Houve algum problema na criação de novos calçados. Por favor contacte o administrador!<br></h5>", unsafe_allow_html=True)
streamlit_analytics.stop_tracking()