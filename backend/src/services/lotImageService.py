from src.repositories.loteRepository import buscar_geometria_por_cadastro
from src.utils.lotsLayerPlot.overlayLots import highlight_lot 
import uuid



def processar_lote_para_pdf(inscricao_completa: str):
   
    if not inscricao_completa:
        return False, None
    
    cadastro = inscricao_completa[:8]
    resultado = buscar_geometria_por_cadastro(cadastro)
    print(f"[DEBUG] Cadastro buscado: {cadastro}, resultado: {resultado}")
    if not resultado:
        print(f"[WARN] Nenhum lote encontrado para inscrição {inscricao_completa}")
        return False, None
    
    wkt_geom = resultado["the_geom"]

    unique_id = str(uuid.uuid4().int)[:4]
    output_path = rf"C:\Users\Administrator\Projetos\pdfGeneratorProj\backend\src\cuts\recorte_{inscricao_completa}_{unique_id}.png"


    highlight_lot(wkt_geom, output_path=output_path)
    return True, output_path
