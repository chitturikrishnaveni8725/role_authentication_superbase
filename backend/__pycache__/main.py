from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = FastAPI()




supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


class RegisterModel(BaseModel):
    id: str
    name: str
    email: str
    password: str
    role: str


class LoginModel(BaseModel):
    email: str
    password: str



@app.post("/register")
def register(user: RegisterModel):
    res = supabase.table("profiles").insert(user.dict()).execute()
    return {"message": "User registered", "data": res.data}


@app.post("/login")
def login(user: LoginModel):
    res = supabase.table("profiles") \
        .select("*") \
        .eq("email", user.email) \
        .eq("password", user.password) \
        .execute()

    if not res.data:
        return {"error": "Invalid credentials"}

    logged_user = res.data[0]

    supabase.table("login_entries").insert({
        "id": f"log_{logged_user['id']}_{datetime.now().timestamp()}",
        "user_id": logged_user["id"],
        "email": logged_user["email"],
        "role": logged_user["role"],
        "login_time": str(datetime.now())
    }).execute()

    return {
        "message": "Login success",
        "user": logged_user
    }

@app.get("/logs")
def get_logs():
    res = supabase.table("login_entries").select("*").execute()
    return res.data