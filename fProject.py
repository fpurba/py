import streamlit as st
import pandas as pd
import datetime

st.title('Peta Sebaran Covid-19 di Indonesia')


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load data into the dataframe.
data_raw = pd.read_csv('C:\\Users\\Purba\\Desktop\\fProject\\covid_19_indonesia_time_series_all.csv')
# Clean data
data_clean = data_raw[['Date', 'Location', 'Longitude', 'Latitude', 'New Cases', 'New Deaths', 'New Recovered']]
data_clean = data_clean.loc[data_clean['Location'] != 'Indonesia']
data_clean['Date'] = pd.to_datetime(data_clean['Date'])
data_clean = data_clean.set_index('Date')
data_clean['New Active Cases'] = (data_clean['New Cases'] - data_clean['New Deaths'] - data_clean['New Recovered']).cumsum()
data_clean['Total Cases'] = data_clean['New Cases'].cumsum()
data_clean['Total Death'] = data_clean['New Deaths'].cumsum()
data_clean['Total Recovered'] = data_clean['New Recovered'].cumsum()
data_clean['Total Active Cases'] = data_clean['New Active Cases'].cumsum()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Loading data...done!")

if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(data_raw)
    st.subheader('Data Clean')
    st.write(data_clean)
    st.write('Sumber data: https://www.kaggle.com/datasets/hendratno/covid19-indonesia')
    
col1, col2 = st.columns(2)

cases = data_clean['New Cases'].sum()
cases_txt = '{:,.0f}'.format(cases)
col1.subheader('Terkonfirmasi')
col1.success(cases_txt)
    
death = data_clean['New Deaths'].sum()
death_txt = '{:,.0f}'.format(death)
col2.subheader('Meninggal')
col2.success(death_txt)

col3, col4 = st.columns(2)

recovered = data_clean['New Recovered'].sum()
recovered_txt = '{:,.0f}'.format(recovered)
col3.subheader('Sembuh')
col3.success(recovered_txt)

active = cases - death - recovered
active_txt = '{:,.0f}'.format(active)
col4.subheader('Kasus Aktif')
col4.success(active_txt)

st.subheader('Perkembangan Kasus Terkonfirmasi Positif Covid-19 Per-Hari')
col5, col6 = st.columns(2)
start_date = col5.date_input('Start Date', datetime.date(2021, 6, 1))
end_date = col6.date_input('End Date', datetime.date(2021, 12, 3))
chart = data_clean['New Cases'].resample('W').sum().loc[start_date :end_date]
st.area_chart(chart)

st.subheader('Perkembangan Kasus Meninggal Per-Hari')
chart = data_clean['New Deaths'].resample('W').sum().loc[start_date :end_date]
st.area_chart(chart)

st.subheader('Perkembangan Kasus Sembuh Per-Hari')
chart = data_clean['New Recovered'].resample('W').sum().loc[start_date :end_date]
st.area_chart(chart)

with st.sidebar:
    st.header('Final Project Pelatihan Python Digitalent Kominfo')
    st.write('''
        **Kelompok M:**\n
        Fero Ronaldo - Ferri Purba - Galih Pandu
         ''')