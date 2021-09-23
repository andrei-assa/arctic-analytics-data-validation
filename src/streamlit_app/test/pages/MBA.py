import streamlit as st

def app(data):
    st.title('Running Market Basket Analysis..........')
    st.dataframe(data)
    return(data)