import streamlit as st
def app():
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