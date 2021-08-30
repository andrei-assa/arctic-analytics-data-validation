import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import data_upload,login,MBA,linearregression,report
#, machine_learning, metadata, data_visualize, redundant, inference # import your pages here


# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Artic Analytics")
t = st.empty    
logedin = login.app(c,conn)

if logedin is not None and logedin[0]:
    st.sidebar.write(logedin)
    #if st.button('Signip'):createnewuser.app()
    #else:st.write('Goodbye')
    # Create a page dropdown 
    page = st.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3"]) 
    if page == "Page 1":
        st.write("oirtortyurto")
        # Display details of page 1
    elif page == "Page 2":
        data_upload.app()
        # Display details of page 2
    elif page == "Page 3":
        st.write("asdasd")
        # Display details of page 3

    # Add all your applications (pages) here
    #app.add_page("Upload Data", data_upload.app)
    app.add_page("Market Basket Analysis", MBA.app)
    app.add_page("Linear regression", linearregression.app)
    app.add_page("Report",report.app)
    #app.add_page("Y-Parameter Optimization",redundant.app)


    #https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030
    # The main app
    app.run()