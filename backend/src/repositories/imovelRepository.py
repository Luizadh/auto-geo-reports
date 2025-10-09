from src.database.oracleDataAccess import executeQuery

def buscar_imovel_por_inscricao(inscricao: str) -> dict | None:
    
    query = """
        SELECT
            INSCRICAO,
            PROPRIETARIO,
            CPFCGC,
            LOCALIZIMOVEL,
            NUMERO,
            BAIRRO,
            LOTEAMENTO,
            AREADOLOTE,
            AREACONSTRUIDA,
            TIPOIMOVEL,
            LOTE
        FROM GEOCONSULTA.GEO_IMOBILIARIO
        WHERE INSCRICAO = :1
    """

    try:
        resultados = executeQuery(query, (inscricao,))
        if resultados:
            colunas = [
                "INSCRICAO",
                "PROPRIETARIO",
                "CPFCGC",
                "LOCALIZIMOVEL",
                "NUMERO",
                "BAIRRO",
                "LOTEAMENTO",
                "AREADOLOTE",
                "AREACONSTRUIDA",
                "TIPOIMOVEL",
                "LOTE",
            ]
            return dict(zip(colunas, resultados[0]))
        else:
            return None

    except Exception as e:
        print("Erro ao buscar imóvel no Oracle:", e)
        return None
