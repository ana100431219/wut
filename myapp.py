
acronyms=list(df_countries.Acronym) 
countries=list(df_countries.Country)
answer= input("Please, input the name of an acronym or a country: ")
while answer.upper() not in acronyms and answer.title() not in countries : 
    answer= input("Please, input the name of an acronym or a country ")
if answer.upper() in acronyms :
  answer_acronym = answer.upper()
  answer_name = df_countries[df_countries.Acronym==answer_acronym]
elif answer.title() in countries:
  answer_name = answer.title()
  answer_acronym = df_countries[df_countries.Country== answer_name].Acronym.item()

print('Selected:{}-{}'.format(answer_acronym,answer_name))    

df_selcountry=df_participants[df_participants.country==answer_acronym]
df_projyear=df_projects[["projectID","year"]]
df_selcountry=pd.merge(df_selcountry,df_projyear,how="left",on="projectID")

df_ECcontr_year=df_selcountry[["ecContribution","year"]].groupby(by="year").sum()
df_ECcontr_year=df_selcountry.groupby('year').sum().ecContribution
df_ECcontr_year.plot(kind='bar', title='Total EU contribution in {ct} (M€)')

df_ECcontr_year.describe()

df_best=df_selcountry.groupby(['shortName','name','activityType','organizationURL']).agg({'ecContribution':['count', 'sum']}).sort_values([("ecContribution","sum")],ascending=False)
df_best.to_excel("country_participants.xlsx")
df_best.head()


#colnames={c:c for c in list(df)}
database = con
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
ct= st.selectbox('Select country', ['Spain', 'France', 'Germany'])
country=pd.read_sql(selects['country'].format(ct), conn)
country=country.Acronym.item()
st.write(f'You selected: {country}-{ct}')

#other selects
dfs={}
for key,sel in selects.items():
  dfs[key]=pd.read_sql(sel.format(country), conn)

df_grants_year = pd.read_sql('''SELECT p.year, SUM(o.ecContribution) AS grants
    FROM organizations o JOIN projects p ON o.projectID==p.projectID
    WHERE o.country='{}'
    GROUP BY p.year '''.format(country), conn)
conn.close()

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

#coordinators
st.subheader(f'Project coordinators in {ct}')
st.dataframe(dfs['coordinators'])
csv_c=dfs['coordinators'].to_csv().encode('utf-8')
