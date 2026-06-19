import streamlit as st

def init_session():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
