import streamlit as st
from APC_data_handler import read_APC

st.title("Baixe dados da APC em um formato decente")

'''
A APC é um excelente fabricante de hélices,
infelizmente o formato em que os dados deles é disponibilizado é uma :poop:

Esse App pretende resolver isso :smiley:
'''

'''Faça Upload do arquivo .txt ou .dat da APC exemplos de arquivos podem ser encontrados [aqui] 
                                 (https://www.apcprop.com/technical-information/performance-data/)'''

uploaded_file = st.file_uploader("")

if uploaded_file is None:
  st.info("Por favor, faça upload do arquivo")
  st.stop()

model_name = st.text_input("Favor inserir o nome da helice")

if model_name is None:
  st.info("Por favor, nomeie o arquivo")
  st.stop()


model_dict = {model_name : uploaded_file}

df = read_APC(model_dict)

st.dataframe(df)
