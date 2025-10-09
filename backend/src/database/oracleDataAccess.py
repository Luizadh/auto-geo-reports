from src.config.oracleConnection import get_oracle_connection  

def executeQuery(query: str, params: tuple = None):
   
    conn = get_oracle_connection()
    if conn is None:
        print('Não foi possível conectar ao Oracle')
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or {})

          
            if query.strip().lower().startswith('select'): 
                results = cursor.fetchall() 
                return results
            else:
                raise ValueError("Execução de queries que alteram o banco não é permitida.")
                

    except Exception as e:
        print(f"Erro ao executar query: {e}")
        return None

    finally:
        if conn:
            conn.close()