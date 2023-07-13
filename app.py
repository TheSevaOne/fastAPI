from fastapi import APIRouter, Depends, HTTPException, Form
import tool
import asyncpg
from fastapi import Request

from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@app_router.post("/login")
async def log_in(input: OAuth2PasswordRequestForm = Depends()):
    user = input.username
    psswd = input.password
    if tool.find_user(user)[0] != psswd:
        raise InvalidCredentialsException

@app_router.get("/")
def home(request:Request):
     return templates.TemplateResponse("base.html", {"request": request})

@app_router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("regpage.html", {"request": request})


@app_router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    return templates.TemplateResponse("login.html",{"status":"registration completed","username":username})
