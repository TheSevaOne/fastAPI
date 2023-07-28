from fastapi import APIRouter, Depends,  Form
import asyncpg
from fastapi import Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi_login import LoginManager
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from pathlib import Path
app_router = APIRouter()
SECRET = b"secret-key"
manager = LoginManager(SECRET, token_url="/login",
                       use_cookie=True)  # todo secret to env var
manager.cookie_name = "web-project"
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@manager.user_loader
def load_user(username: str):
    user = username
    return user


@app_router.on_event("startup")
async def startup():
    app_router.db = await asyncpg.create_pool(user='admin', password='admin', database='test', host='127.0.0.1', port='5432')


@app_router.on_event("shutdown")
async def stop():
    await app_router.db.close()


@app_router.get('/login', response_class=HTMLResponse)
def log_in(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app_router.post("/login", response_class=HTMLResponse)
async def log_in(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    async with app_router.db.acquire() as connection:
        try:
            ok_password, _ = await connection.fetchrow("select password,username from users where username=$1", str(username))
        except:
            return RedirectResponse("", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if ok_password != password:
        raise InvalidCredentialsException
    else:
        access_token = manager.create_access_token(data={"sub": username})
        response = RedirectResponse("/user", status_code=status.HTTP_302_FOUND)
        manager.set_cookie(response, access_token)
        return response


@app_router.get("/logout")
def logout(response: Response):
    response = RedirectResponse('/login', status_code=302)
    response.delete_cookie("web-project")
    return response


@app_router.get('/user', response_class=HTMLResponse)
def user(request: Request, username=Depends(manager)):
    return templates.TemplateResponse("userpage.html", {"request": request, "account_name": username})


@app_router.get("/")
def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app_router.get('/register', response_class=HTMLResponse)
def register(request: Request):
    return templates.TemplateResponse("regpage.html", {"request": request})


@app_router.post('/register', response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    async with app_router.db.acquire() as connection:
        try:
            await connection.execute("insert into users (username, password) VALUES ($1, $2)", str(username), str(password))
            return RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
        except:
            return templates.TemplateResponse("regpage.html", {"request": request, "error": "Пользователь существует"})
