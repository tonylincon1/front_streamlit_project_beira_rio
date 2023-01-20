import cv2
import boto3
import numpy as np
import pandas as pd
from PIL import Image
import mysql.connector
import streamlit as st
from pickle import load
from mysql.connector import errorcode

config = {
  'host':'chicodelivery.com',
  'user':'chicod46_root',
  'password':'poss-supt-kirs-op',
  'database':'chicod46_imagens_beirario',
  'client_flags': [mysql.connector.ClientFlag.SSL],
}
        
def select_table(tabela):
    try:
        conn = mysql.connector.connect(**config)
        print("Connection established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()
        
    cursor.execute(f"""
    SELECT 
    *
    FROM 
    {tabela};""")

    rows = cursor.fetchall()
    rows = pd.DataFrame(rows)
    return rows

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
    