from fastapi import FastAPI
from router.user_router import user
from router.vehicle_router import vehiculo
from config.db import Base, engine

app = FastAPI(title="SmartPark API")

Base.metadata.create_all(bind=engine)

app.include_router(user)
app.include_router(vehiculo)