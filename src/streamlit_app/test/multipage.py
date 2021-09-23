"""
This file is the framework for generating multiple Streamlit applications 
through an object oriented framework. 
"""

# Import necessary libraries 
import streamlit as st

# Define the multipage class to manage the multiple apps in our program 
class MultiPage: 
    """Framework for combining multiple streamlit applications."""

    def __init__(self) -> None:
        """Constructor class to generate a list which will store all our applications as an instance variable."""
        self.pages = []
    
    def add_page(self, title, func) -> None: 
        """Class Method to Add pages to the project
        Args:
            title ([str]): The title of page which we are adding to the list of apps 
            
            func: Python function to render this page in Streamlit
        """

        self.pages.append({
          
                "title": title, 
                "function": func
            })
    def runforms(self):
        pagelen = len(self.pages)
        #col = list(range(pagelen))
        #global()['col' % pagelen] = st.columns(1)
        st.write(len(self.pages),self.pages[0]["title"],col1)
        for x,y in enumerate(self.pages):
            st.write(x,y,col)
            #col[x] = st.columns(1)
            #with col[x]:
                #st.header("Churn Modeling")
            if st.button(y["title"]):
                y["function"]()
            #col[x] = st.columns(x)
            #with colx:
                #st.header("Churn Modeling")
    def run(self,data):
        # Drodown to select the page to run  

        page = st.selectbox(
            'App Navigation', 
            self.pages, 
            format_func=lambda page: page['title']
        )
        # run the app function 
        return page['function'](data)