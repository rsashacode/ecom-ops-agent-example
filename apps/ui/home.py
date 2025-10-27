import os

import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL")
if not API_BASE_URL:
    api_host = os.getenv("API_HOST", "api")
    api_port = os.getenv("API_PORT", "8000")
    API_BASE_URL = f"http://{api_host}:{api_port}"

st.set_page_config(page_title="E-Com Ops Agent", layout="wide")
st.title("E-Com Ops Agent")

user_msg = st.text_input("Ask something")
if st.button("Send", disabled=not user_msg):
    try:
        r = requests.post(f"{API_BASE_URL}/v1/chat", json={"message": user_msg}, timeout=10)
        st.write(r.json())
    except Exception as e:
        st.error(str(e))
