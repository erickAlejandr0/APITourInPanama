from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncpg
import asyncio
from app.dataBase.db import connect_db

async def eliminar_actividades_expiradas(retries=3, delay=5):
    conn = None
    for intento in range(retries):
        try:
            conn = await connect_db()
            await conn.execute("SELECT * FROM eliminar_actividades_expiradas()")
            print("Actividades expiradas eliminadas")
            break  
        except Exception as e:
            print(f"[ERROR] Intento {intento+1}/{retries} fallido: {e}")
            if intento < retries - 1:
                await asyncio.sleep(delay)
        finally:
            if conn:
                await conn.close()

async def iniciar_scheduler():
    print("Ejecutando limpieza inicial del itinerario en background...")
    asyncio.create_task(eliminar_actividades_expiradas())