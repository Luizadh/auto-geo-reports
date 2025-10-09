import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from src.config.settings import FRONTEND_URL
from src.controllers.pdfController import router as pdf_router
from src.controllers.imovelController import router as imovel_router
from src.controllers.loteController import router as lote_router

FRONTEND_URLS = os.getenv("FRONTEND_URLS", "")
origins = FRONTEND_URLS.split(",") 

app = FastAPI(
    title="Sistema de Consulta de Imóveis",
    description="API para consultar imóveis e gerar PDFs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API funcionando!"}

app.include_router(pdf_router, tags=["PDF"])
app.include_router(imovel_router, tags=["Imóvel"])
app.include_router(lote_router, tags=["PDF"])




