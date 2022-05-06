import numpy as np
import streamlit as st

import sqlite3
import pandas as pd 
from sqlite3.dbapi2 import DatabaseError
from PIL import Image

con= sqlite3.connect('ecsel_database.db')
df_participants=pd.read_excel(r'C:\Users\Ayala\Downloads\participants')
df_countries=pd.read_excel(r'C:\Users\Ayala\Downloads\countries.xlsx')
df_projects=pd.read_excel(r'C:\Users\Ayala\Downloads\projects.xlsx')

df_projects.to_sql('projects', con, if_exists='replace', index= False)
df_countries.to_sql('countries', con, if_exists='replace', index= False)
df_participants.to_sql('participants', con, if_exists='replace', index= False)

con.close()
df_projects.head()
