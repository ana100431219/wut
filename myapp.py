import sqlite3 
import pandas as pd 
import streamlit as st
from sqlite3.dbapi2 import DatabaseError
from PIL import Image

#colnames={c:c for c in list(df_countries)}

database = 'CreateDB.db'
selects= {
'country':
'''SELECT Acronym FROM countries WHERE Country = "{}" ''',

'grants':
'''SELECT SUM (o.ecContribution) AS grants
  FROM organizations o JOIN projects p ON o.projectID==p.projectID
  WHERE o.country = '{}'
  GROUP BY p.year''',

'participants':
'''SELECT shortName, name, activityType, organizationURL, COUNT(ecContribution) n_projects, SUM(ecContribution)   #maybe this is incomplete
  FROM organizations
  WHERE country = '{}'
  GROUP BY name ORDER BY SUM(ecContribution) DESC''',

'coordinators':
'''SELECT o.shortName, o.name, p.acronym, p.keywords
  FROM organizations o JOIN projects p ON o.projectID = p.projectID
  WHERE o.country='{}' AND o.role = 'coordinator' '''
}

#Title
image=Image.open('KDT-JU.png')
st.image(image)
st.title('Partner search tool')


#Select country
conn=sqlite3.connect(database)
df_countries= pd.read_sql('SELECT * FROM countries', conn)  #for get all data from table countries
countries=list(df_countries.Country) #for selectbox

ct= st.selectbox('Select country', countries)
country = df_countries[df_countries.Country== ct].Acronym.item()

st.write(f'You selected: {country}-{ct}')

dfs={}
for key, sel in selects.items():
  dfs[key]=pd.read_sql(sel.format(country), conn)

df_grants_year = pd.read_sql('''SELECT j.year, SUM(p.ecContribution) AS grants
    FROM participants p JOIN projects j ON p.projectID==j.projectID
    WHERE p.country='{}'
    GROUP BY j.year '''.format(country), conn)


#grants
st.subheader(f'Yearly EC contribution in {ct} (€)')
st.bar_chart(dfs['grants'])

#participants
st.subheader(f'Participants in {ct}')
st.dataframe(dfs['participants'])
csv_p=dfs['participants'].to_csv().encode('utf-8')
st.download_button(
    label= 'Download participants data as CSV',
    data=csv_p,
    file_name=f'{country}_participants.csv',
    mime='text/csv',
)
