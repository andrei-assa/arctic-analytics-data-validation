import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import graphviz as graphviz
import pandas as pd
import numpy as np

from io import StringIO
#import mimetypes
import os
import sys
from pathlib import Path


this_file = Path(__file__)
root_directory = str(this_file.parent.parent.absolute())
sys.path.insert(0, root_directory)
from validation.validator import DataValidator
from validation.transformer import DataTransformer



columndict = {} #declaring a global variable for it to collect the columns names and type

# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


def go_home():
    st.subheader("Home")


def main():
    """Simple Login App"""
    st.image('arctic_logo.png', width=190)
    #st.title('Arctic Analytics')

    ##################################
    # Left Side Menu
    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        go_home()

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        logged_in = st.sidebar.checkbox("Login")

        if logged_in:
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            logged_in_successfully = login_user(username,check_hashes(password,hashed_pswd))
            if logged_in_successfully:
                st.success("Logged In as {}".format(username))
                options_for_task_dropdown = ["Market Basket Analysis", "Profiles"]
                user_selected_task = st.selectbox("Task", options_for_task_dropdown)
                if user_selected_task == "Add Post":
                    st.subheader("Add Your Post")
                #     Placeholder for some additional stuff

                elif user_selected_task == "Market Basket Analysis":
                    
                    ()

                elif user_selected_task == "Profiles":
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password",type='password')

        if st.button("Signup"):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

def filetypeselecter():
    file_type = mimetypes.guess_type(uploaded_file.name)

    if file_type[0] in ['text/plain', 'text/tab-separated-values', 'text/csv']: #csv types
        uploaded_data_df = pd.read_csv(uploaded_file, nrows=100)

    elif file_type[0] in ['application/json']: # json types
        uploaded_data_df = pd.read_json(uploaded_file, nrows=100)

    elif file_type[0][-5:] in ['sheet', 'excel']: # excel types
        uploaded_data_df = pd.read_excel(uploaded_file, nrows=100)

    else:
        print("This file does not a permitted extension. Please upload either .csv, .tsv, .json, .xls, .xlsx, or .txt")

@st.cache
def load_data(datafile,nrows):
    data = pd.read_csv(datafile, nrows=nrows)
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def market_basket_analysis():
    st.subheader("Market Basket Analysis")
    uploaded_file = st.file_uploader("Choose a file")
    # TODO: Add error handling for empty file

    if uploaded_file is not None: # User uploads new data file.

        # File type handling
        file_name = uploaded_file.name
        file_extension = os.path.splitext(file_name)[1]
        print("\nUploaded File Name: ", file_name, "\tFile Extension: ", file_extension)

        loader_function_dictionary = {'.txt': pd.read_csv, '.tsv': pd.read_csv, '.csv': pd.read_csv, \
            '.json': pd.read_json, '.xls': pd.read_excel, '.xlsx': pd.read_excel}
        loader_function = loader_function_dictionary[file_extension] if file_extension in loader_function_dictionary else \
            "This file does not a permitted extension. Please upload either .csv, .tsv, .json, .xls, .xlsx, or .txt"

        print("\nData loading to frame...")
        uploaded_data_df = loader_function(uploaded_file)
        print("\nData displayed to frame.")

        validator = DataValidator(data=uploaded_data_df)

        if validator.is_valid:
            # TODO: Validator should return a more specific reason why data was not valid.
            
            # Long Format Data --> DataValidator --> DataTransformer --> Short Format Data
            # Short Format Data --> DataValidator --> Done
            # Invalid Data --> DataValidator --> Invalid
            if validator._long_format:
                data_transformer = DataTransformer(data=uploaded_data_df)
                transformed_data = data_transformer.transform()

            elif validator._short_format:
                pass

            else:
                print("Data is of unknown format. Please correct your data format")

            st.write("File is valid.")
            st.subheader("View Data")
            st.write(uploaded_data_df)

            visualize_data(uploaded_data_df)

        else:
            # TODO: Accept user input to fix the problem specified above
            # Allow user to try again?
            st.write("File is not valid")

    else: # Displays sample data (from Cloud) when user hasn't uploaded data.
        DATE_COLUMN = 'date/time'
        DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                    'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

        @st.cache
        def load_data(nrows):
            data = pd.read_csv(DATA_URL, nrows=nrows)
            lowercase = lambda x: str(x).lower()
            data.rename(lowercase, axis='columns', inplace=True)
            data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
            return data

        data_load_state = st.text('Loading data...')
        data = load_data(10000)
        data_load_state.text("Done! (using st.cache)")
        # if st.checkbox('Show raw data'):
        st.subheader('Sample data')
        st.write(data)
        st.subheader('Columns in this dataset')
    

        #Issue #9: Connect the file upload function with the dropdown options to allow for selection of columns types
        #Need a way to select the column name and select the data type --> mapping (dictionary --> {column x: dtype x} )
        
        #Possible option:
        #streamlit.selectbox(column_name) --> 
        #streamlit.selectbox(data_type) --> 
        
        #for column_name, data_type in remap_dtypes_dictionary.items(): data[column_name] = data[column_name].astype(
        #data_type)
        
        for x in data.columns:
            st.subheader(x)
            options = st.multiselect('Specify the column type for ' + x, ['String', 'Int', 'Float'], ['Int', 'String'])
            st.write('You selected:', options)


def visualize_data(data):
    print("Creating visualization...")
    st.subheader('Results')
    
    #Bar Chart
    st.write("### Popular Products")
    to_visualize = data.head()
    st.bar_chart(to_visualize['product_id'])

    st.write("### Products Ordered and Reordered")
    chart_data = pd.DataFrame(data[:20], columns=['add_to_cart_order', 'reordered'])
    st.area_chart(chart_data)

    # We can use seaborn with Streamlit:
    st.write("### Heatmap")
    colormap = sns.color_palette("mako", as_cmap=True)
    fig, ax = plt.subplots(figsize=(10,10))
    st.write(sns.heatmap(data=data[["product_id", "order_id", "add_to_cart_order", "reordered"]].corr(), annot=True,linewidths=0.5, cmap=colormap))
    st.pyplot(fig)

    # We can use graphlib graph object for Market basket analysis lift charts
    st.write("### Product Lift Chart")
    graph = graphviz.Digraph()
    graph.edge('eggs', 'sausages')
    graph.edge('sausages', 'bacon')
    graph.edge('cereal', 'milk')
    graph.edge('milk', 'cereal')
    graph.edge('milk', 'yoghurt')
    graph.edge('jam', 'bread')
    graph.edge('bread', 'bacon')
    graph.edge('bacon', 'sausages')
    graph.edge('bread', 'milk')
    graph.edge('eggs', 'milk')
    graph.edge('cereal', 'black pudding')
    graph.edge('black pudding', 'mushrooms')
    graph.edge('bacon', 'ketchup')

    st.graphviz_chart(graph)

    print("Results visualized.")


if __name__ == '__main__':
    main()