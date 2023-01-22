from PIL import Image
import streamlit as st
import streamlit_analytics
from outhers.utils import check_password

st.set_page_config(
    page_title="Sobre o Projeto",
    page_icon="👞",
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.image("files/images/logo.png", use_column_width=True)

streamlit_analytics.start_tracking()

if check_password():
    
    st.markdown("""<h1 style="text-align:center">Projeto Beira Rio <br> IA para Reconhecimento de Imagens</h1>""", unsafe_allow_html=True)
    st.markdown("***")

    st.markdown("<h3>1) Objetivo 👞<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">O projeto trata-se do desenvolvimento de um algoritmo para classificação, reconhecimento de calçados semelhantes e avaliação das recomendações. Para isso foi utilizada técnicas de tratamento e padronização de imagens, modelos de machine learning e deep learning e outras ferramentas de desenvolvimento web.</p>""", unsafe_allow_html=True)

    st.markdown("<h3>2) Etapas de Desenvolvimento 👠<br></h3>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Para o desenvolvimento do projeto, foram seguidas as seguintes etapas:</p>""", unsafe_allow_html=True)
    image = Image.open('files/images/Etapas de Desenvolvimento.png')
    st.image(image)
    
    st.markdown("<h4>2.1) Modelo para Classificação<br></h4>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Para o desenvolvimento do modelo de classificação, foram seguidas as seguintes etapas:</p>""", unsafe_allow_html=True)
    st.markdown("""
                <ul style='list-style-type:decimal'>
                    <li>Conhecimento e coleta e preparação dos dados: A primeira etapa do processo foi coletar uma grande quantidade de imagens de calçados das classes desejadas (por exemplo, tênis, sapatos, botas, etc.). Essas imagens foram coletadas do branco de dados da Beira Rio. Em seguida, as imagens foram preparadas para o treinamento, incluindo etapas como redimensionar, dividir em conjuntos de treinamento e validação, e normalizar;</li>
                    <li>Construção da rede: A segunda etapa foi construir a rede neural VGG16. Isso incluiu a escolha da arquitetura, configuração dos hiperparâmetros e compilação da rede;</li>
                    <li>Treinamento da rede: A terceira etapa foi treinar a rede com o conjunto de dados preparado. Isso incluiu o uso de técnicas de otimização, como o algoritmo de otimização Adam, e ajustes de hiperparâmetros para melhorar o desempenho da rede;</li>
                    <li>Avaliação e otimização: Após o treinamento, a rede foi avaliada usando o conjunto de validação e otimizada com base nos resultados. Isso incluiu ajustes adicionais nos hiperparâmetros e ajustes na arquitetura da rede;</li>
                    <li>Implantação: Finalmente, a rede treinada foi implantada em um sistema de classificação de calçados. Isso incluiu a integração da rede com outras partes do sistema, como captura de imagens e interface do usuário.</li>
                </ul>""", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Uma matriz de confusão é uma ferramenta comumente utilizada para avaliar o desempenho de um modelo de aprendizado de máquina. Ela permite visualizar a precisão do modelo ao classificar exemplos em diferentes categorias.</p>""", unsafe_allow_html=True)

    st.markdown("""<p style="text-align:justify">Neste projeto, utilizamos uma matriz de confusão para avaliar o desempenho de um modelo de classificação de imagens. A matriz foi construída com base no conjunto de dados de validação, comparando as classificações do modelo com as classificações corretas.""", unsafe_allow_html=True)

    st.markdown("""<p style="text-align:justify">A matriz de confusão consiste em uma tabela quadrada, onde cada linha representa uma classe real e cada coluna representa uma classe prevista pelo modelo. Cada célula na matriz representa o número de exemplos que foram classificados corretamente (na diagonal principal) ou incorretamente (fora da diagonal principal) pelo modelo.""", unsafe_allow_html=True)
    st.metric(label="Acurácia", value="89%")
    image = Image.open('files/images/Modelo de Classificação.png')
    st.image(image)
    
    st.markdown("<h4>2.2) Modelo para Recomendação<br></h4>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Para o desenvolvimento do projeto, foram seguidas as seguintes etapas:</p>""", unsafe_allow_html=True)
    st.markdown("""
                <ul style='list-style-type:decimal'>
                    <li>Pré-processamento dos dados: A primeira etapa foi o pré-processamento dos dados, incluindo a coleta de imagens de calçados, a preparação de dados e a normalização;</li>
                    <li>Treinamento da VGG16: A segunda etapa foi treinar uma VGG16 com as imagens de calçados para extrair características das imagens, foi utilizado o modelo de classificação com as camadas anteriores para obter as caracteristicas;</li>
                    <li>Cálculo do coeficiente de similaridade: A terceira etapa foi calcular o coeficiente de similaridade entre os conjuntos de características de cada calçado. Foi utilizado o cosseno, que é um dos métodos mais utilizados para medir a similaridade entre vetores;</li>
                    <li>Recomendação: Finalmente, o modelo foi implementado como um sistema de recomendação, onde o usuário pode escolher um calçado e o sistema recomenda calçados similares baseado no coeficiente de similaridade calculado.</li>
                </ul>""", unsafe_allow_html=True)
    
    st.markdown("<h4>2.3) Modelo de Avaliação<br></h4>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">O modelo é baseado em uma VGG16 e é classificado binariamente, onde 0 representa uma recomendação ruim e 1 representa uma recomendação boa. Este processo foi aplicado com sucesso em projetos passados e tem sido usado como referência para projetos futuros.</p>""", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Para o desenvolvimento do projeto, foram seguidas as seguintes etapas:</p>""", unsafe_allow_html=True)
    st.markdown("""
                <ul style='list-style-type:decimal'>
                    <li>Coleta e preparação dos dados: A primeira etapa foi coletar imagens de calçados e criar uma base de dados de recomendações, com informações sobre se a recomendação foi considerada boa ou ruim pelos usuários. Em seguida, os dados foram divididos em conjuntos de treinamento e validação;</li>
                    <li>Treinamento da VGG16: A segunda etapa foi treinar uma VGG16 com as imagens de calçados e suas respectivas recomendações para classificar as recomendações como boas ou ruins;</li>
                    <li>Teste e ajuste de hiperparâmetros: A terceira etapa foi testar o modelo com o conjunto de validação e ajustar hiperparâmetros para melhorar o desempenho do modelo;</li>
                    <li>Implantação: Finalmente, o modelo foi implantado em um sistema de recomendação de calçados, onde ele é usado para avaliar se as recomendações são boas ou ruins para os usuários.</li>
                </ul>""", unsafe_allow_html=True)
    st.metric(label="Acurácia", value="84%")
    image = Image.open('files/images/Modelo de Avaliação.png')
    st.image(image)
    
    st.markdown("<h4>2.4) Modelo de Criação de Novos Calçados<br></h4>", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:justify">Além dos modelos apresentados acima, um modelo também foi implementado para demonstração ao cliente. Foi criado um pipeline de GAN (rede geradora adversária) com o objetivo de gerar novas imagens de calçados a partir de duas imagens de calçados de entrada. Este processo foi aplicado com sucesso em projetos passados e tem sido usado como referência para projetos futuros.</p>""", unsafe_allow_html=True)
    
    st.markdown("""<p style="text-align:justify">Algumas demonstrações do potencial do modelo de criação de novos calçados:</p>""", unsafe_allow_html=True)
    st.markdown("""<p style="text-align:center"><strong>Combinando Características Duas Botas e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
    image = Image.open('files/images/Combinação de Calçados 1.png')
    st.image(image)
    st.markdown("""<p style="text-align:center"><strong>Combinando Características Dois Tênis Esportivos e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
    image = Image.open('files/images/Combinação de Calçados 2.png')
    st.image(image)
    st.markdown("""<p style="text-align:center"><strong>Combinando Características Bota com Scarpin e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
    image = Image.open('files/images/Combinação de Calçados 3.png')
    st.image(image)
    st.markdown("""<p style="text-align:center"><strong>Combinando Características Dois Scarpins e Gerando Novos Calçados</strong></p>""", unsafe_allow_html=True)
    image = Image.open('files/images/Combinação de Calçados 4.png')
    st.image(image)

    st.markdown("<h3>3) Parceria 🥾<br></h3>", unsafe_allow_html=True)
    image = Image.open('files/images/parceria.png')
    st.image(image)
    st.markdown("")
    
streamlit_analytics.stop_tracking()