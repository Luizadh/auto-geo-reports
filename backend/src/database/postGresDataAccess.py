from src.config.postGresConnection import get_postGres_connection



def executeQuery(query: str, params: tuple = None):
   
    conn = get_postGres_connection()
    if conn is None:
        print('Não foi possível conectar ao PostgreSQL')
        return None

    try:
        
        with conn.cursor() as cursor:

            if params:
                cursor.execute(query, params)

            else:
                cursor.execute(query)
            
            if query.strip().lower().startswith('select'):
                results = cursor.fetchall()
                return results
            
            else:
                raise ValueError("Execução de queries que alteram o banco não é permitida.")
                
    except Exception as e:
        print(f"Erro ao executar query: {e}")
        return None

    finally:
        conn.close()