from fastapi import APIRouter, Depends, HTTPException, Form
import tool
import asyncpg
from fastapi import Request,status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm

app_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@app_router.on_event("startup")
async def startup():
    app_router.db = await asyncpg.create_pool(user='admin', password='admin', database='test', host='127.0.0.1', port='5432')


@app_router.on_event("shutdown")
async def stop():
     await  app_router.db.close()


@app_router.get('/login', response_class=HTMLResponse)
def log_in(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app_router.post("/login", response_class=HTMLResponse)
async def log_in(username: str = Form(...), password: str = Form(...)):
    async with app_router.db.acquire() as connection:
            ok_password,_= await connection.fetchrow("select password,username from users where username=$1",username)
    if ok_password!= password:
        raise InvalidCredentialsException
    else:
         RedirectResponse("/", status_code=status.HTTP_302_FOUND)


@app_router.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app_router.get("/register", response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("regpage.html", {"request": request})


@app_router.post("/register", response_class=HTMLResponse)
async def register(username: str = Form(...), password: str = Form(...)):
    print(username, password)
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
