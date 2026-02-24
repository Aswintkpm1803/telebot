import streamlit as st


def login():

    USERNAME = st.secrets["ADMIN_USERNAME"]
    PASSWORD = st.secrets["ADMIN_PASSWORD"]

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:

        st.title("Login Required")

        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("Login"):

            if user == USERNAME and pwd == PASSWORD:

                st.session_state.authenticated = True
                st.rerun()

            else:
                st.error("Invalid username or password")

        st.stop()


def logout():

    st.session_state.authenticated = False
    st.rerun()