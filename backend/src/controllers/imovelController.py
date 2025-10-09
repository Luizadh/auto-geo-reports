from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.repositories.imovelRepository import buscar_imovel_por_inscricao



router = APIRouter()



@router.get("/imovel/{inscricao}")
def consultar_imovel(
    inscricao: str, 
    campos: Optional[List[str]] = Query(None)  
):
    resultado = buscar_imovel_por_inscricao(inscricao)
    if not resultado:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")

    print("Campos recebidos do frontend:", campos) 

    if campos:
        resultado_filtrado = {k: v for k, v in resultado.items() if k in campos}
        return resultado_filtrado

    return resultado
