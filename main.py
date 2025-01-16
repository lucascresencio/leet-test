from fastapi import FastAPI

from api import root, registration 

app = FastAPI()


app.include_router(root.router)
app.include_router(registration.router, prefix="/registration", tags=["registration"])