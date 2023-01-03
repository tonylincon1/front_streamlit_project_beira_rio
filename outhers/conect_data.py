import cv2
import boto3
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from pickle import load

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

def envia_avaliacao_para_banco():
    pass

def salvar_avaliacoes_pkl(array_imagem_reduzido,nota):
    """Essa função é somente para armazenar no processo de teste, porém quando conectarmos com o banco será removida"""
    try:
        data_pickle = load(open('outhers/datapickle.pkl', 'rb'))
        data = pd.DataFrame([[array_imagem_reduzido.astype(np.uint8),nota]],columns=["data","nota"])
        data_armazen = pd.concat([data_pickle,data])
        data_armazen.to_pickle('outhers/datapickle.pkl')
    except:
        data = pd.DataFrame([[array_imagem_reduzido.astype(np.uint8),nota]],columns=["data","nota"])
        data.to_pickle('outhers/datapickle.pkl')
    