import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import mimetypes
import sys
from pathlib import Path

this_file = Path(__file__)
root_directory = str(this_file.parent.parent.absolute())
sys.path.insert(0, root_directory)
from validation.validator import DataValidator


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

    st.title('Artic Analytics')

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
    if uploaded_file is not None:

        # TODO: Implement file type handling
        # File type handling (Note: may change to Strategy pattern)
        st.write(uploaded_file.name)
        data_load_state = st.text('Loading data...')
        uploaded_data_df = load_data(uploaded_file,100)
        data_load_state.text("Done! (using st.cache)")
        # if st.checkbox('Show raw data'):
        #uploaded_data_df = pd.read_csv(uploaded_file, nrows=100)

        validator = DataValidator(
            data=uploaded_data_df
            )
        if validator.is_valid:
            # TODO: Validator should return a more specific reason why data was not valid.
            st.write("File is valid")
            st.write(uploaded_data_df)
            st.subheader('Raw data')
            for x in uploaded_data_df.columns:
                st.subheader(x)
                options = st.multiselect('Specify the column type for ' + x, ['String', 'Int', 'Float'], ['Int', 'String'])
                #st.write('You selected:', options)
                columndict[x] = options
            st.write('You selected:', columndict)

        else:
            # TODO: Accept user input to fix the problem specified above
            # Allow user to try again?
            st.write("File is not valid")


    
    #Issue #9: Connect the file upload function with the dropdown options to allow for selection of columns types
    #Need a way to select the column name and select the data type --> mapping (dictionary --> {column x: dtype x} )
    
    #Possible option:
    #streamlit.selectbox(column_name) --> 
    #streamlit.selectbox(data_type) --> 
    
    #for column_name, data_type in remap_dtypes_dictionary.items(): data[column_name] = data[column_name].astype(
    #data_type)
    


if __name__ == '__main__':
    main()