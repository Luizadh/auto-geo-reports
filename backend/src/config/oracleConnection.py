
from .settings import ORACLE_CONFIG
import oracledb



if ORACLE_CONFIG.get("lib_dir"):
    try:
        oracledb.init_oracle_client(lib_dir=ORACLE_CONFIG["lib_dir"])
    except Exception as e:
        print(f"Aviso: não foi possível inicializar o Oracle Client: {e}")




def get_oracle_connection():
  
    try:
        conn = oracledb.connect(
            user=ORACLE_CONFIG["user"],
            password=ORACLE_CONFIG["password"],
            dsn=ORACLE_CONFIG["dsn"]
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar no Oracle: {e}")
        return None
