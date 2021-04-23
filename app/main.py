import os

from app.misc import get_unique_diameters_list

import streamlit as st


st.title("Baixe dados da APC em um formato decente")

'''
A APC é um excelente fabricante de hélices,
infelizmente o formato em que os dados deles é disponibilizado é uma :poop:

Esse App pretende resolver isso :smiley:
'''
  
unique_diameters_list = get_unique_diameters_list()

diameter = st.select_slider("Slide to select the propeller's diameter", options=unique_diameters_list)

unique_pitches_list = get_unique_pitches(unique_diameters_list)

pitch = st.select_slider("Slide to select the propeller's diameter", options=unique_pitches_list)
