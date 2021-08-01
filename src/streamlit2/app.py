"""Streamlit app."""

import streamlit as st

PAGES = {

        "Home": src.pages.home,
        "About": src.pages.about,
        "Services": src.pages.services,
        "Contact": src.pages.contact,
        }

def main():

    """Main entrypoint into app"""
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]
    

