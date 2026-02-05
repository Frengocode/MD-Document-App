from fastapi import FastAPI

from src.application.services.auth.router import auth_service_router
from src.application.services.document.router import document_service_router
from src.application.services.user.router import user_router_service

app = FastAPI(title="Document Service")


app.include_router(user_router_service)
app.include_router(auth_service_router)
app.include_router(document_service_router)
