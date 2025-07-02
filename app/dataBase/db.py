import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()  

DATABASE_URL = os.getenv("SUPABASE_DB_URL")

# Función para obtener una nueva conexión
async def connect_db():
    if not DATABASE_URL:
        raise ValueError("SUPABASE_DB_URL no está definido en el entorno")
    return await asyncpg.connect(DATABASE_URL)
