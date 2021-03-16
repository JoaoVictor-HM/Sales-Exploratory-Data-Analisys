import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import altair as at



data = pd.read_csv('sales_data_sample.csv')


# Getting the Years and Months from Sales

data['ORDERDATE'] = pd.to_datetime(data['ORDERDATE'])
 
data['year'] = data['ORDERDATE'].dt.year
data['month'] = data['ORDERDATE'].dt.month

unique_years = sorted(data['year'].unique())
unique_months = sorted(data['month'].unique())



st.title('Sales Study Project')

st.markdown("""
### This app provides simple webscraping of Sales data
 
 **Python libraries:** base64, pandas, streamlit, altair

 #### General Informations

""")
st.write(data)

st.write("""

#### Filtered Data

""")

#Constructing and Applying the Filters
total_per_country = []
for country in data.COUNTRY.unique():
    total_per_country.append(data.loc[(data['COUNTRY'] == country), 'SALES'].sum())

st.sidebar.header('User Input Features')
selected_country = st.sidebar.selectbox('Country', list(data['COUNTRY'].unique()))
selected_years = st.sidebar.multiselect('Years', unique_years, unique_years)
selected_months = st.sidebar.multiselect('Months', unique_months, unique_months)

filtered_df = data[data.COUNTRY.eq(selected_country) & data.year.isin(selected_years) & data.month.isin(selected_months)]
st.write(filtered_df)

#Buttons

for year in selected_years:
    
    total_per_month = []
    for month in selected_months:
        total_per_month.append(filtered_df.loc[((filtered_df['year'] == year) & (filtered_df['month'] == month)), 'SALES'].sum())
    if st.button('Total Sales in ' + str(selected_country) + ' in ' + str(year)):
        source = pd.DataFrame({'month': selected_months, 'total_sales':total_per_month})
        chart = at.Chart(source).mark_line().encode(x='month', y='total_sales')
        st.write(chart)


if st.button('Total Sales Per Country'):
    source = pd.DataFrame({'country': data['COUNTRY'].unique(), 'total_sales':total_per_country})
    chart = at.Chart(source).mark_bar().encode(x='country', y='total_sales')
    st.write(chart)



    




