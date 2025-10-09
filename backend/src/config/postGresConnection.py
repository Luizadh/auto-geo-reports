from .settings import POSTGRES_CONFIG
import psycopg2



def get_postGres_connection():
    try:
        conn = psycopg2.connect(
            user=POSTGRES_CONFIG["user"],
            password=POSTGRES_CONFIG["password"],
            host=POSTGRES_CONFIG["host"],
            port=POSTGRES_CONFIG["port"],
            dbname=POSTGRES_CONFIG["dbname"]
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no PostgreSQL: {e}")
        return None
