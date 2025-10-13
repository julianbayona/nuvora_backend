from fastapi import APIRouter

user = APIRouter()

@user.get("/")
def root():
    return{"message": "Hi"}