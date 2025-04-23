from fastapi import FastAPI
from routers import auth, patients

app = FastAPI()

app.include_router(auth.router)
app.include_router(patients.router)