import sqlite3 as sql
import pandas as pd 
from PIL import Image
import pandas as pd 

con= sqlite3.connect('ecsel_database.db')

df_participants=pd.read_excel('participants.xlsx')
df_countries=pd.read_excel('countries.xlsx')
df_projects=pd.read_excel('projects.xlsx')

df_projects.to_sql('projects', con, if_exists='replace', index= False)
df_countries.to_sql('countries', con, if_exists='replace', index= False)
df_participants.to_sql('participants', con, if_exists='replace', index= False)

con.close()
df_projects.head()
