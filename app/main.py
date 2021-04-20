import os

from app.misc import get_unique_diameters_list
from database_handler.Build_JSON_db import build_json_db(), does_local_db_exist

import streamlit as st


st.title("Baixe dados da APC em um formato decente")

'''
A APC é um excelente fabricante de hélices,
infelizmente o formato em que os dados deles é disponibilizado é uma :poop:

Esse App pretende resolver isso :smiley:
'''

if not does_local_db_exist(os.getcwd()+"/data/"):
  build_json_db()
  
unique_diameters_list = get_unique_diameters_list()

diameter = st.select_slider("Slide to select the propeller's diameter", options=unique_diameters_list)

pitches_list = get_pitches()
pitch = st.select_slider("Slide to select the propeller's diameter", options=pitches_list)