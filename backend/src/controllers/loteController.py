from fastapi import APIRouter, HTTPException
from src.repositories.loteRepository import buscar_geometria_por_cadastro


router = APIRouter()

@router.get("/geometria/{cadastro}")
def consultar_geometria(cadastro: str):
    resultado = buscar_geometria_por_cadastro(cadastro)
    if not resultado:
        raise HTTPException(status_code=404, detail="Geometria não encontrada")
    return resultado
