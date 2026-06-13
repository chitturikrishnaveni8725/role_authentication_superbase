import streamlit as st
import requests
import pandas as pd

# from dotenv import load_dotenv
# import os
# load_dotenv()

# BASE_URL = os.getenv("BASE_URL")
BASE_URL = st.secrets["BASE_URL"]
# BASE_URL = "http://127.0.0.1:8000"

if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "Register"



def go(page):
    st.session_state["page"] = page
    st.rerun()


def register_page():

    st.title("🔐 Role-Based Authentication System")

    st.header("Register")

    user_id = st.text_input("User ID")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Select Role",
        ["student", "trainer", "manager", "admin"]
    )

    if st.button("Register"):

        res = requests.post(
            f"{BASE_URL}/register",
            json={
                "id": user_id,
                "name": name,
                "email": email,
                "password": password,
                "role": role
            }
        )

        st.success("Registration Successful")

        st.json(res.json())

        go("Login")

    st.write("Already have an account?")

    if st.button("Go to Login"):
        go("Login")


def login_page():

    st.title(" Role-Based Authentication System")

    st.header("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        res = requests.post(
            f"{BASE_URL}/login",
            json={
                "email": email,
                "password": password
            }
        )

        data = res.json()

        if "user" in data:

            st.session_state["user"] = data["user"]

            st.success("Login Successful")

            go("Dashboard")

        else:
            st.error(data["error"])

    st.write("Don't have an account?")

    if st.button("Go to Register"):
        go("Register")


def dashboard_page():

    user = st.session_state["user"]

    if not user:
        st.warning("Please Login First")
        go("Login")
        return

    st.title(" Dashboard")

    st.subheader("Logged-in User")

    st.write(user)

    if user["role"] == "student":
        st.success("🎓 Student Dashboard")

    elif user["role"] == "trainer":
        st.success("👨‍🏫 Trainer Dashboard")

    elif user["role"] == "manager":
        st.success(" Manager Dashboard")

    elif user["role"] == "admin":
        st.success(" Admin Dashboard")

    
    st.subheader("Login Entries")

    res = requests.get(f"{BASE_URL}/logs")

    logs = res.json()

    if logs:

        df = pd.DataFrame(logs)

        st.dataframe(df)

    else:
        st.info("No Login Entries Found")

    
    if st.button("Logout"):

        st.session_state["user"] = None

        go("Login")


if st.session_state["page"] == "Register":
    register_page()

elif st.session_state["page"] == "Login":
    login_page()

elif st.session_state["page"] == "Dashboard":
    dashboard_page()