from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional
import io
from src.repositories.imovelRepository import buscar_imovel_por_inscricao
from src.utils.pdfGenerator import gerar_pdf_bytes 
from pydantic import BaseModel


router = APIRouter()


@router.get("/imovel/{inscricao}/pdf")
def gerar_pdf_imovel(
    inscricao: str, 
    campos: Optional[List[str]] = Query(None),
    oficio: Optional[str] = Query("") 
):
    

    resultado = buscar_imovel_por_inscricao(inscricao)
    if not resultado:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")

   
    if campos:
        resultado_filtrado = {k: v for k, v in resultado.items() if k in campos}
    else:
        resultado_filtrado = resultado

    
    resultado_filtrado["OFICIO"] = oficio

    try:
        pdf_bytes = gerar_pdf_bytes(resultado_filtrado)
        if not pdf_bytes: 
            raise HTTPException(status_code=500, detail="Erro ao gerar PDF: bytes vazios")
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}") 
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {e}")

    return StreamingResponse(
        io.BytesIO(pdf_bytes), 
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=imovel_{inscricao}.pdf"}
    )

class PdfRequest(BaseModel):
    camposSelecionados: Optional[List[str]] = None
    oficio: Optional[str] = ""
    observacao: Optional[str] = ""
    destinatario: Optional[str] = ""


@router.post("/imovel/{inscricao}/pdf-com-observacao")
def gerar_pdf_com_observacao(inscricao: str, request: PdfRequest):


    resultado = buscar_imovel_por_inscricao(inscricao)
    if not resultado:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado")

  
    if request.camposSelecionados:
        resultado_filtrado = {k: v for k, v in resultado.items() if k in request.camposSelecionados}
    else:
        resultado_filtrado = resultado

    
    resultado_filtrado["OFICIO"] = request.oficio
    resultado_filtrado["OBSERVACAO"] = request.observacao or ""
    resultado_filtrado["DESTINATARIO"] = request.destinatario or ""

 
    try:
        pdf_bytes = gerar_pdf_bytes(resultado_filtrado)
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="Erro ao gerar PDF: bytes vazios")
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar PDF: {e}")

    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=imovel_{inscricao}.pdf"}
    )
