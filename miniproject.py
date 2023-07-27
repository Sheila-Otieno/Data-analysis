import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.linear_model import LinearRegression


#title
st.title("Diamond price prediction")

#Image
st.image("diamond.jpg", width=300)

#Displaying the dataset
data= sns.load_dataset("diamonds")

menu = st.sidebar.radio("Menu",["Home","Prediction price"])
if menu=="Home":
    st.write("Shape of the dataset", data.shape)
    st.write("Null values", data.isnull().sum())
    
    st.header("Tabular form of data")
    if st.checkbox("Tabular data"):
        st.table(data.head(150))
    st.header("Statistical summary")
    if st.checkbox("Statistics"):
        st.table(data.describe())
    st.header("Correlation graph")
    if st.checkbox("Correlation graph"):
        fig,ax = plt.subplots()
        sns.heatmap(data.corr(), ax=ax ,cmap="blues")
        st.write(fig)

    st.title("Graphs")
    graph = st.selectbox("Different types of graphs", ["Scatter plot","Bar graph","Histogram"])
    if graph =="Scatter plot":
        value = st.slider("Filter using carat size",0,5)
        data = data.loc[data["carat"] >= value]
        fig, ax = plt.subplots(figsize=(10,5))
        sns.scatterplot(data=data, x="carat", y="price", hue="cut")
        st.pyplot(fig)
    if graph=="Bar graph":
        fig,ax= plt.subplots(figsize=(10,5))
        sns.barplot(data = data, x="cut", y=data.cut.index)
        st.pyplot(fig)
    if graph=="Histogram":
        fig,ax=plt.subplots(figsize=(10,5))
        sns.distplot(data.price, kde=True)
        st.pyplot(fig)

#Prediction of diamond prices
if menu=="Prediction price":
    
    #linear regression model
    lr = LinearRegression()
    X = np.array(data["carat"]).reshape(-1,1)
    y = np.array(data["price"]).reshape(-1,1)
    lr.fit(X,y)
    value = st.number_input("Carat size",0.20, 5.01, step=0.15)
    value = np.array(value).reshape(1,-1)
    prediction = lr.predict(value)[0]
    if st.button("Price prediction in $"):
        st.write(prediction)
