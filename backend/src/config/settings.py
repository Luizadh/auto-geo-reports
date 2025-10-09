
import os
from pathlib import Path
from dotenv import load_dotenv



def find_dotenv(max_levels=4):
    p = Path(__file__).resolve()
    for _ in range(max_levels):
        candidate = p.parent / ".env"
        if candidate.exists():
            return str(candidate)
        p = p.parent
    return None



env_path = find_dotenv()
if env_path:
    print(f"Carregando .env de: {env_path}")
    load_dotenv(dotenv_path=env_path)
else:
    print("nao encontrou .env")
    pass




ORACLE_CONFIG = {
    "user": os.getenv("ORACLE_USER"),
    "password": os.getenv("ORACLE_PASSWORD"),
    "dsn": os.getenv("ORACLE_DSN"),
    "lib_dir": os.getenv("ORACLE_LIB_DIR")
}
 

POSTGRES_CONFIG = {
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": int(os.getenv("PG_PORT", 5432)),
    "dbname": os.getenv("PG_DB")
}


FRONTEND_URL = os.getenv("FRONTEND_URL")
PDF_OUTPUT_DIR = os.getenv("PDF_OUTPUT_DIR")
PDF_LOGO_PATH = os.getenv("PDF_LOGO_PATH")
