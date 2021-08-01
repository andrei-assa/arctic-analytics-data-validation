import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import sys
from pathlib import Path
this_file = Path(__file__)
root_directory = str(this_file.parent.parent.absolute())
sys.path.insert(0, root_directory)

# Open Issues:
# #9 Connect the file upload function with the dropdown options to allow for selection of columns types --> Andrei
    # --> Implement two drop-down boxes to allow remapping of column types and pass dictionary to backend
# #7 Expand the validation, provide more detailed information in the case of errors / invalid data --> Tasha
# #10 Aggregate column types into dictionary and store these in case other modules need to use them. --> Hardeep

# New potential issues
# Fix login process

# CI / CD --> Jenkins / Travis

# pyspark ? --> Improve ML workflow / create pipelines
# mlxtend.frequent_patterns --> apriori, association_rules

# networkx
# heatmap or matrix with embedded circles to represent lift / support / conviction

from validation.validator import DataValidator

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


"""
class App(object):
    def __init__(self, title):
        self.title = st.title(title)

        # Composition
        self.left_side_menu = LeftSideMenu() 


"""



class LeftSideMenu(self):

    def __init__(self):
        # Left Side Menu
        menu = ["Home","Login","SignUp"]
        choice = st.sidebar.selectbox("Menu",menu)
        if choice == "Home":
            go_home()
        elif choice == "Login":
            st.subheader("Login Section")
            username = st.sidebar.text_input("User Name")
            password = st.sidebar.text_input("Password",type='password')
        



class App(object):

    def __init__(self, title):
        self.title = st.title(title) 
        self.left_side_menu = LeftSideMenu()


def main():
    """Simple Login App"""

        if st.sidebar.button("Login"):
            create_usertable()
            hashed_pswd = make_hashes(password)
            logged_in_successfully = login_user(username,check_hashes(password,hashed_pswd))
            if logged_in_successfully:
                st.success("Logged In as {}".format(username))
                options_for_task_dropdown = ["Add Post", "Market Basket Analysis", "Profiles"]
                user_selected_task = st.selectbox("Task", options_for_task_dropdown)
                if user_selected_task == "Add Post":
                    st.subheader("Add Your Post")
                #     Placeholder for some additional stuff

                elif user_selected_task == "Market Basket Analysis":
                    market_basket_analysis()

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




def market_basket_analysis():
    st.subheader("Market Basket Analysis")
    uploaded_file = st.file_uploader("Choose a file")
    # TODO: Add error handling for empty file
    if uploaded_file is not None:

        # TODO: Implement file type handling
        # File type handling

        # import mimetypes

        ### Text ### --> pd.read_csv
        # mime = mimetypes.guess_type(file)
        # mimetypes.guess_type("alcohol.csv")
        # mimetypes.guess_type("this_is_a_text_file.txt")
        # Out[10]: ('text/plain', None)
        # In[11]: mimetypes.guess_type("this_is_a_tab_delimited_file.tsv")
        # Out[11]: ('text/tab-separated-values', None)
        # Out[2]: ('text/csv', None)

        ### JSON ### --> pd.read_json
        # mimetypes.guess_type("/Users/andrei_assa/1617287125679.json")
        # Out[3]: ('application/json', None)

        ### Excel ### --> pd.read_excel
        # In[7]: mimetypes.guess_type("Book1.xlsx")
        # Out[7]: ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', None)
        # mimetypes.guess_type("no_extension_excel.xls")
        # Out[9]: ('application/vnd.ms-excel', None)
        # --> if the file has multiple sheets, prompt the user to select the desired sheet

        ### No extension ### --> You are on your own
        # mimetypes.guess_type("no_extension_excel")
        # Out[8]: (None, None)

        # Issue #10: Aggregate the columns types into a dict that can be passed on to other python files
        # Get the dtypes from the dataframe and store them.
        # Use Cases:
        # 1. Store the schema of the uploaded file
        # 2. Pass dtypes to validator


        # Consider using "Strategy" design pattern by selecting relevant I/O function based on file type (see below)

        # loader_function_dictionary = {".xlsx" : pd.read_excel, ".csv": pd.read_csv}
        # loader_function = loader_function_dictionary.get(file_extension)
        # if it is excel, loader_function = pd.read_excel, etc, if the extension does not exist, it is None.
        # if loader function is not None:
            # uploaded_data_df = loader_function(uploaded_file)
        #

        # If the I/O function is valid, then try to load the file

        uploaded_data_df = pd.read_csv(uploaded_file, nrows=100)
        # Issue #7 -->
        validator = DataValidator(
            data=uploaded_data_df
            )
        if validator.is_valid:
            # TODO: Validator should return a more specific reason why data was not valid.
            st.write("File is valid")
            st.write(uploaded_data_df)
        else:
            # TODO: Accept user input to fix the problem specified above
            # Allow user to try again?
            st.write("File is not valid")
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
    st.subheader('Raw data')
    st.write(data)
    st.subheader('Columns in this dataset')

    for x in data.columns:
        st.subheader(x)
        options = st.multiselect('Specify the column type for ' + x, ['String', 'Int', 'Float'], ['Int', 'String'])
        st.write('You selected:', options)


if __name__ == '__main__':
    main()
