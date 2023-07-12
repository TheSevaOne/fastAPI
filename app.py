from fastapi import FastAPI, Depends, HTTPException
import tool
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
app=FastAPI()
@app.post("/login")
def log_in(input: OAuth2PasswordRequestForm=Depends()):
    user=input.username
    psswd=input.password
    user=to




