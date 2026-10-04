"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""
import os
from contextlib import asynccontextmanager  # EUREKA

import py_eureka_client.eureka_client as eureka_client  # EUREKA
from fastapi import FastAPI

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")  # EUREKA


@asynccontextmanager  # EUREKA
async def lifespan(app: FastAPI):
    # Démarrage : enregistrement dans Eureka
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="NOTIFICATION",
        instance_host="localhost",
        instance_port=PORT,
        instance_id=f"notification:{PORT}",
    )
    yield
    # Arrêt : désenregistrement propre
    await eureka_client.stop_async()


app = FastAPI(
    lifespan=lifespan,  # EUREKA
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
)

app.include_router(notification.router)


# Bonus : health check
@app.get("/health")  # EUREKA
def health():
    return {"status": "UP"}


# TODO (students): if you add other routers, include them here.


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)