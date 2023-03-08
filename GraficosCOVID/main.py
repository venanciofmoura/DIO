import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
df = pd.read_csv('https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv')
df = df.rename(columns={ 'date': 'Data', 'state': 'Estado', 'newDeaths': 'Novas Mortes', 'newCases': 'Novos Casos',
                'deaths_per_100k_inhabitants': 'Mortes por 100 mil habitantes', 'totalCases_per_100k_inhabitants':'Total de Casos por 100 mil habitantes'})

df = df[['Data', 'Estado', 'Novas Mortes', 'Novos Casos', 'Mortes por 100 mil habitantes', 'Total de Casos por 100 mil habitantes']]
df['Data'] = pd.to_datetime(df['Data'])


with st.sidebar:
    filter_state = st.multiselect(
        'Qual estado?',
        df['Estado'].drop_duplicates(),
        default='TOTAL'
    )

    filter_columns = st.selectbox(
        'Qual informação?',
        df.columns[2:]
    )

    filter_date = st.date_input(
        'Em qual data?',
        [min(df['Data']),
        datetime.now()]
    )

try:
    df = df[(df['Data'] >= pd.to_datetime(filter_date[0])) & (df['Data'] <= pd.to_datetime(filter_date[1]))]
except:
    df = df[(df['Data'] >= pd.to_datetime(filter_date[0])) & (df['Data'] <= pd.to_datetime(datetime.now()))]

tabela_por_estado = pd.DataFrame()

for estado in filter_state:
    df_filtrado = df[df['Estado'] == estado]
    tabela_por_estado = tabela_por_estado.append(df_filtrado, ignore_index=True)

try:
    tabela_por_estado_agrupado = tabela_por_estado.groupby(by=['Data']).sum().reset_index()
except:
    pass



st.title('DADOS COVID - BRASIL')
st.caption('Selecione os estados, tipo de visualização e a data no menu ao lado')


try:
    fig = px.line(tabela_por_estado, x='Data', y=filter_columns, color='Estado', title=f'{filter_columns} por Estado')
    fig

    fig_agrupado = px.line(tabela_por_estado_agrupado, x='Data', y=filter_columns, title=f'{filter_columns} Consolidado')
    fig_agrupado
except:
    fig = px.line(df, x='Data', y=filter_columns, color='Estado', title=f'{filter_columns} por Estado')
    fig

    fig_agrupado = px.line(df, x='Data', y=filter_columns, title=f'{filter_columns} por Estado')
    fig_agrupado










    