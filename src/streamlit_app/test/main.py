import streamlit as st

# Custom imports 
from multipage import MultiPage
from pages import data_upload,login,MBA,linearregression,report,algorithm_page
#, machine_learning, metadata, data_visualize, redundant, inference # import your pages here


# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()

def algo():

    # Add all your applications (pages) here
    #app.add_page("Upload Data", data_upload.app)
    app.add_page("Market Basket Analysis", MBA.app)
    app.add_page("Linear regression", linearregression.app)
    app.add_page("Report",report.app)
    #app.add_page("Y-Parameter Optimization",redundant.app)
    # The main app to be run to get the side bar
    #app.runforms()
    app.run()
    st.title('Arctic Analytics Algorithms')
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    with col1:
        with st.form("Form1"):
            #st.selectbox("Select flavor", ["Vanilla", "Chocolate"], key=1)
            st.header("Churn Modeling")
            st.write("Predict which of your customers will churn and why with decision trees.  ")
            submitted1 = st.form_submit_button("Get started")

    with col2:
        with st.form("Form2"):
            st.header("Direct Marketing")
            st.write("Predict response to campaigns and increase the conversion rate of your campaign.")
            submitted2 = st.form_submit_button("Get started")
    with col3:
        with st.form("Form3"):
            st.header("Credit Risk Modeling")
            st.write("Model credit default risk by training an Optimized SUpport Vector Machine (SVM model).")
            submitted3 = st.form_submit_button("Get started")
    with col4:
        with st.form("Form4"):
            st.header("Market Basket Analysis")
            st.write("Find products frequently purchased together and turn them into rules for recommendations.")
            submitted4 = st.form_submit_button("Get started")
            if submitted4:
                return "Market Basket Analysis"
    with col5:
        with st.form("Form5"):
            st.header("Predictive Maintenance")
            st.write("Predict equipment failures and schedule maintenance pre-emptively.")
            submitted5 = st.form_submit_button("Get started")
    with col6:
        with st.form("Form6"):
            st.header("Price Risk Clustering")
            st.write("Cluster price developments using X-means to unveil price-risk relationships.")
            submitted6 = st.form_submit_button("Get started")
    
def uploaddata():
    data_upload.app()

def loggedin():
    st.sidebar.write("Welcome "+st.session_state.key)
    algooutput = ""
    if algooutput == "Market Basket Analysis":
        MBA.app()
    else:
        uploaddata()
        algooutput = algo()
        st.sidebar.write(algooutput)
    
    


    #https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030
    
    
# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Arctic Analytics")
t = st.empty()
#with t.container():
    #form = st.form(key='my-form')
    #name = form.text_input('Enter your name')
    #submit = form.form_submit_button('Submit')
    #MBA.app()
    #st.write('Press submit to have your name printed below')

    #if submit:
        #st.write(f'hello {name}')
        #t.empty()

# Initialization of sessionstate so that users dont have to login again
if 'key' not in st.session_state:
   logedin = login.app(c,conn)
   if logedin[0]: 
       st.session_state['key'] = logedin[1]
       loggedin()
else:loggedin()