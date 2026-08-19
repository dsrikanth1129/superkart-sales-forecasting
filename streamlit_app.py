
import streamlit as st
import requests
import pandas as pd
import io

st.title('SuperKart Sales Forecasting')

# Backend URL (inside Docker network)
BACKEND_URL = 'http://backend:7860'

st.header('Single Prediction')
with st.form('prediction_form'):
    weight = st.number_input('Product Weight', value=12.0)
    sugar = st.selectbox('Sugar Content', ['Low Sugar', 'Regular', 'No Sugar'])
    area = st.number_input('Allocated Area Ratio', value=0.05)
    mrp = st.number_input('Product MRP', value=150.0)
    size = st.selectbox('Store Size', ['Small', 'Medium', 'High'])
    city = st.selectbox('City Type', ['Tier 1', 'Tier 2', 'Tier 3'])
    st_type = st.selectbox('Store Type', ['Food Mart', 'Supermarket Type1', 'Supermarket Type2', 'Departmental Store'])
    char = st.selectbox('Product ID Prefix', ['FD', 'DR', 'NC'])
    age = st.number_input('Store Age (Years)', value=15)
    cat = st.selectbox('Product Category', ['Perishables', 'Non Perishables', 'Others'])
    
    submit = st.form_submit_button('Forecast Sales')

if submit:
    payload = {
        "Product_Weight": weight, "Product_Sugar_Content": sugar, "Product_Allocated_Area": area,
        "Product_MRP": mrp, "Store_Size": size, "Store_Location_City_Type": city,
        "Store_Type": st_type, "Product_Id_char": char, "Store_Age_Years": age, "Product_Type_Category": cat
    }
    response = requests.post(f'{BACKEND_URL}/v1/predict', json=payload)
    st.success(f'Predicted Sales: {response.json()["prediction"]:.2f}')

st.header('Batch Prediction')
uploaded_file = st.file_uploader('Upload CSV for Batch Prediction', type=['csv'])
if uploaded_file:
    files = {'file': uploaded_file.getvalue()}
    response = requests.post(f'{BACKEND_URL}/v1/predictbatch', files=files)
    st.write(pd.DataFrame.from_dict(response.json(), orient='index', columns=['Predicted Sales']))
