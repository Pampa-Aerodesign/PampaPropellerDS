import streamlit as st
from APC_data_handler import read_APC
import os

st.title("Baixe dados da APC em um formato decente")

'''
A APC é um excelente fabricante de hélices,
infelizmente o formato em que os dados deles é disponibilizado é uma :poop:

Esse App pretende resolver isso :smiley:
'''

if not does_local_db_exist(os.getcwd()+"/database/"):
  generate_json_db()
  


diameter = st.select_slider('Slide to select propeller diameter', options=unique_diameters_list)
