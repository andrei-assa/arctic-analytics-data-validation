import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO


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



def main():
    """Simple Login App"""

    st.title('Artic Analytics')

    menu = ["Home","Login","SignUp"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.checkbox("Login"):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:

                st.success("Logged In as {}".format(username))

                task = st.selectbox("Task",["Add Post","Market Basket Analysis","Profiles"])
                if task == "Add Post":
                    st.subheader("Add Your Post")

                elif task == "Market Basket Analysis":
                    st.subheader("Market Basket Analysis")

                    uploaded_file = st.file_uploader("Choose a file")
                    if uploaded_file is not None:
                        # To read file as bytes:
                        bytes_data = uploaded_file.getvalue()
                        st.write(bytes_data)

                        # To convert to a string based IO:
                        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                        st.write(stringio)

                        # To read file as string:
                        string_data = stringio.read()
                        #st.write(string_data)

                        # Can be used wherever a "file-like" object is accepted:
                        dataframe = pd.read_csv(uploaded_file,nrows=100)
                        st.write(dataframe)

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

                    #if st.checkbox('Show raw data'):
                    st.subheader('Raw data')
                    st.write(data)
                    st.subheader('Columns in this dataset')

                    for x in data.columns:
                        st.subheader(x)
                        options = st.multiselect('Specify the column type for '+x,['String', 'Int', 'Float'], ['Int', 'String'])
                        st.write('You selected:', options)


                elif task == "Profiles":
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



if __name__ == '__main__':
    main()