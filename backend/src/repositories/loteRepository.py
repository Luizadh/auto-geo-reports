from src.database.postGresDataAccess import executeQuery

def buscar_geometria_por_cadastro(cadastro: str) -> dict | None:

    query = """
        SELECT gid, ST_AsText(the_geom) AS the_geom,  num_lote
        FROM public.lotesvr
        WHERE cadastro = %s
        LIMIT 1
    """

    try:
        resultados = executeQuery(query, (cadastro,))
        if resultados:
            colunas = ["gid", "the_geom", "num_lote"]
            return dict(zip(colunas, resultados[0]))
        else:
            return None

    except Exception as e:
        print("Erro ao buscar geometria no PostGIS:", e)
        return None