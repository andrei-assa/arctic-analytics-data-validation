import streamlit as st
import hashlib



def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


# DB  Functions
def create_usertable(c):
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(c,conn,username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def login_user(c,username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


def view_all_users():
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
def loginuser(c,conn, username,password):
    create_usertable(c)
    hashed_pswd = make_hashes(password)

    logged_in_successfully = login_user(c,username,check_hashes(password,hashed_pswd))
    if logged_in_successfully:
        st.success("Logged In as {}".format(username))
        return(True,username)
    else:
        st.warning("Incorrect Username/Password or signup for new user")
        if st.button('SignUp'):
            signupnewuser(c,conn,username,password)
        
def signupnewuser(c,conn,username,password):
    create_usertable(c)
    add_userdata(c,conn,username,make_hashes(password))
    st.success("You have successfully created a valid Account")
    st.info("Go to Login Menu to login")
    
def app(c,conn):
    text_input_container1 = st.empty()
    with text_input_container1.container():
        form = st.form(key='login-form')
        username = form.text_input("User Name")
        password = form.text_input("Password",type='password')
        submit = form.form_submit_button('Login')

    if submit:
        status,uname = loginuser(c,conn, username,password)
        if status is True:
            text_input_container1.empty()
            return(status,uname)
        
    


  