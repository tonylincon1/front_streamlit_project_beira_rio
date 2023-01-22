from PIL import Image
import streamlit as st
import streamlit_analytics
from outhers.utils import check_password

st.set_page_config(
    page_title="Recomendações",
    page_icon="👞",
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.image("files/images/logo.png", use_column_width=True)

streamlit_analytics.start_tracking()

if check_password():
    st.markdown("""<h1 style="text-align:center">Recomendações</h1>""", unsafe_allow_html=True)
    st.markdown("***")
    
    st.markdown("""<p style="text-align:justify">Nessa seção trazemos algumas recomendações para a utilização da ferramenta e boas práticas para alimentação do banco de dados.</p>""", unsafe_allow_html=True)
    
    st.markdown("<h3>1) Tipos de Arquivos<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Foi apresentado durante o desenvolvimento do projeto que existiam muitos arquivos que não eram especificamente imagens:</p>""", unsafe_allow_html=True)
    image = Image.open('files/images/qualidade_das_imagens.png')
    st.image(image)
    st.markdown("""<p style="text-align:justify">Aproximadamente 19% dos arquivos foram "desperdiçados" por não serem imagens, o que compromete na utilização da solução, portanto, a primeira recomendação que aconselhamos é a utilização dos seguintes tipos de arquivo tanto para a solução quanto para a alimentação do banco de dados:</p>""", unsafe_allow_html=True)
    st.markdown("""
                <ul>
                    <li>JPG;</li>
                    <li>JPEG;</li>
                    <li>PNG;</li>
                    <li>TIFF.</li>
                </ul>""", unsafe_allow_html=True)
    
    st.markdown("<h3>2) Qualidade das Imagens<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">A qualidade das imagens são de extrema importância para o bom funcionamento da solução, portanto também recomendamos que:</p>""", unsafe_allow_html=True)
    st.markdown("""
                <ul>
                    <li>Capture a foto com uma boa iluminação;</li>
                    <li>Tente capturar a foto o mais próximo possível do foco;</li>
                    <li>Pode capturar mais de um objeto por foto, contato que seja visível;</li>
                    <li>Tente capturar mais de 1 ângulo do objeto que está capturando.</li>
                </ul>""", unsafe_allow_html=True)
    
    st.markdown("<h3>3) Como Capturar uma Imagem Detectável<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Como foi falado anteriormente, a qualidade das imagens ajudam na melhoria gradativa do desempenho da solução, para isso, trazemos aqui alguns exemplos de fotos que possuem "alta qualidade". Essa fotos representam imagens que tiveram alto poder de detecção dos objetos.</p>""", unsafe_allow_html=True)
    image = Image.open('files/images/exemplo_imagem_qualidade_1.png')
    st.image(image)
    image = Image.open('files/images/exemplo_imagem_qualidade_2.png')
    st.image(image)
    image = Image.open('files/images/exemplo_imagem_qualidade_3.png')
    st.image(image)
    image = Image.open('files/images/exemplo_imagem_qualidade_4.png')
    st.image(image)
    image = Image.open('files/images/exemplo_imagem_qualidade_5.png')
    st.image(image)
streamlit_analytics.stop_tracking()