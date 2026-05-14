from fastapi import FastAPI
from routes.router import router

app = FastAPI(title="Verificación de Rutas")

app.include_router(router)
