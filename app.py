import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the pre-trained Linear Regression model
loaded_model = pickle.load(open('Countrywise_Product_Sales.sav','rb'))

retail_stock_sales = pd.read_csv("retail_stock_sales.csv")
encoded_retail_stock = pd.read_csv("encoded_retail_stock.csv")

# Function to predict sales based on user input
def predict_sales(country, stockcode, quantity, unit_price):

    count_value = pd.unique(encoded_retail_stock['Country'].values)
    retail_count_value = pd.unique(retail_stock_sales['Country'].values)

    new_country = count_value[np.where(retail_count_value == country)]
    new_country_1 = new_country[0]

    item_value = pd.unique(encoded_retail_stock['StockCode'].values)
    retail_item_value = pd.unique(retail_stock_sales['StockCode'].values)

    new_stockcode = item_value[np.where(retail_item_value == stockcode)]
    new_stockcode_1 = new_stockcode[0]

    stock_value = np.array([new_country_1, new_stockcode_1, quantity, unit_price])
    stock_value_reshape = stock_value.reshape(1,-1)
    prediction = loaded_model.predict([stock_value])
    return prediction[0]

# Streamlit UI
st.title('Countrywise Product Sales Prediction')

# User input fields
country = st.selectbox('Select Country:', pd.unique(retail_stock_sales['Country'].values))
stockcode = st.selectbox('Select StockCode:', pd.unique(retail_stock_sales['StockCode'].values))
quantity = st.number_input('Enter Quantity:', min_value=0, max_value=80000, step=50)
unit_price = st.number_input('Enter Unit Price:', min_value=0.0, max_value=18000.0, step=100.0)

# Predict button
if st.button('Predict Sales'):
    # Make prediction
    prediction = predict_sales(country, stockcode, quantity, unit_price)
    st.success(f'Predicted Sales for {stockcode} in {country} Country: {prediction:.2f}')
