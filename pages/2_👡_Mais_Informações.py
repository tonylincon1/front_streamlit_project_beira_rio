import streamlit as st
import pandas as pd
import numpy as np
import base64

st.set_page_config(
    page_title="IA Calçados Beira Rio",
    page_icon="👞",
)

st.title('Uber pickups in NYC')

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

with open("pages/Projeto Beira Rio - IA para Reconhecimento de Imagens.pdf","rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="500" type="application/pdf"></iframe>'
      
st.markdown(pdf_display, unsafe_allow_html=True)