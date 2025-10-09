import io
import os
import locale
from PIL import Image as PILImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from typing import Dict
from src.services.lotImageService import processar_lote_para_pdf
from .cutImage import cropImage



def gerar_pdf_bytes(dados: Dict) -> bytes:
   
   
    dados_header = {
        
        "DESTINATARIO": dados.get("DESTINATARIO", "DEFENSORIA PÚBLICA DO ESTADO DO RIO DE JANEIRO"),
        "OBSERVACAO": dados.get("OBSERVACAO",""),
        "OFICIO": dados.get("OFICIO", "")

    }


    mapper = {
        "INSCRICAO": "Inscrição Municipal",
        "PROPRIETARIO": "Proprietário",
        "CPFCGC": "CPF/CGC",
        "LOCALIZIMOVEL": "Logradouro",
        "NUMERO": "Número",
        "BAIRRO": "Bairro",
        "LOTEAMENTO": "Loteamento",
        "AREADOLOTE": "Área do Lote",
        "AREACONSTRUIDA": "Área Construída",
        "TIPOIMOVEL": "Tipo do Imóvel",
        "LOTE": "SUBLOTE",
    }


    # print("DADOS:", dados)
    # oficio = dados.get("OFICIO", "N/A")
    # oficioExercicio = oficio.split("/")
    # oficio = oficioExercicio[0]
    # exercicio = oficioExercicio[1] if len(oficioExercicio) > 1 else ""

    
    lote_ok, mapa_path = processar_lote_para_pdf(dados.get("INSCRICAO"))

    def formatar_dados_para_pdf(json_backend: dict, mapeamento: dict = mapper) -> dict:
        resultado_formatado = {}
        
        
        for key, value in json_backend.items():
            label = mapeamento.get(key)
           
           
            if label:
                resultado_formatado[label] = value
        return resultado_formatado


    dados = formatar_dados_para_pdf(dados, mapper)


    buffer = io.BytesIO() 
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=30,  
        leftMargin=60,  
        rightMargin=60, 
        bottomMargin=30,  
    )


    elementos = []
    estilos = getSampleStyleSheet()
    estilos["Normal"].fontSize = 11

   
    logo_path = r"C:\Users\Administrator\Projetos\pdfGeneratorProj\backend\data\pdfImages\IPPULOGO.png"
    
    
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=96, height=57)
    
    
    else:
        logo = Paragraph("LOGO", estilos["Normal"])

    
    # cabecalho_data = [
    #     ["Ofício", "Exercício", "Folha", "Ass."],
    #     [oficio, exercicio, "", ""]
    # ]



    # tabela_cabecalho = Table(cabecalho_data, colWidths=[80, 80, 50, 50])
    


    # tabela_cabecalho.setStyle(TableStyle([
    #     ('GRID', (0,0), (-1,-1), 1, colors.black),
    #     ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    #     ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    #     ('TOPPADDING', (0,0), (-1,-1), 10), 
    # ]))
    

    cabecalho_layout = Table(
     [[logo, ""]], 
    colWidths=[135, 350]
)
 

    cabecalho_layout.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),   
    ('ALIGN', (0, 0), (0, 0), 'LEFT'),     
    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),    
    ]))
    elementos.append(cabecalho_layout)
    elementos.append(Spacer(1, -10))



    linha = Table([[""]], colWidths=[cabecalho_layout._argW[0] + cabecalho_layout._argW[1]])  
    linha.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,0), 1, colors.black),  
    ]))
    elementos.append(Spacer(1, -10))
    elementos.append(linha)



    elementos.append(Spacer(1, 10))
    

   
    estilo_direita = estilos["Normal"].clone('direita')
    estilo_direita.alignment = TA_RIGHT


    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8') 
    except locale.Error:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252') 
    


    data_atual = datetime.now().strftime("%d de %B de %Y")


    elementos.append(Paragraph(f"Volta Redonda, {data_atual}", estilo_direita))
    elementos.append(Spacer(1, 30))


 
    elementos.append(Paragraph(f"<i>A </i> <i><b>{dados_header.get('DESTINATARIO','')}</b></i>,", estilos["Normal"]))
    elementos.append(Spacer(1, 10))


    estilo_com_recuo = ParagraphStyle(
      name="NormalRecuo",
      parent=estilos["Normal"], 
      firstLineIndent=20 
)
   
    elementos.append(Paragraph(
        f"<i>Atendendo a solicitação no </i> <i><b>{dados_header.get('OFICIO','')} </b></i> "
    f"<i>ao(a) {dados_header.get('DESTINATARIO','')} segue as informações do imóvel objeto conforme Cadastro Fazendário e Geoprocessamento do IPPU:</i>", estilo_com_recuo))
    elementos.append(Spacer(1, 20))

    inscricao = str(dados.get("Inscrição Municipal", ""))
    if len(inscricao) == 12:
        dados["Inscrição Municipal"] = f"{inscricao[0]}.{inscricao[1:4]}.{inscricao[4:8]}.{inscricao[8:11]}-{inscricao[11]}"


    for chave, valor in dados.items():
        if chave == "Número":
            try:
                valor_formatado = str(int(valor))
            except (ValueError, TypeError):
                valor_formatado = str(valor).lstrip("0") or "0"

        elif isinstance(valor, str):
            valor_formatado = valor.title()

        else:
            valor_formatado = str(valor)
            if chave in ["Área do Lote", "Área Construída"]:
                try:
                    valor_formatado = f"{float(valor):.2f}".replace(".", ",") + " m²"
                except (ValueError, TypeError):
                    valor_formatado = str(valor) + " m²"
        
        elementos.append(Paragraph(f"<b>{chave}:</b> {valor_formatado}", estilos["Normal"]))
        elementos.append(Spacer(1, 5))


    
    elementos.append(Spacer(1, 20))

  
    
   
    #  mapa_path = r"C:\Users\Administrator\Projetos\pdfGeneratorProj\backend\src\cuts\recorte_teste2.png"
    
    if lote_ok and mapa_path and os.path.exists(mapa_path): 
        try:
            mapa = cropImage(mapa_path, max_width=450, max_height=500)   
            elementos.append(mapa)
            elementos.append(Spacer(1, 4))
        except Exception as e:
            print(f"[ERROR] Erro ao carregar mapa: {e}")
            elementos.append(Paragraph("<b>Erro ao carregar mapa</b>", estilos["Normal"]))
    else:
        elementos.append(Paragraph("<b>Localização não encontrada.</b>", estilos["Normal"]))

    observacao = dados_header.get("OBSERVACAO", "")
    if observacao:
        elementos.append(Spacer(1, 10))
        elementos.append(Paragraph(f"<b>Observação:</b> {observacao}", estilos["Normal"]))

   
    def draw_footer(canvas, doc):
        canvas.saveState()
        footer_text = "Departamento de Informação e Tecnologia/IPPU"
        canvas.setFont("Helvetica", 10)
        canvas.drawString(60, 20, footer_text)  
        canvas.restoreState()


    doc.build(elementos, onFirstPage=draw_footer)
    buffer.seek(0) 
    return buffer.read()  
    