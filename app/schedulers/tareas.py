from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncpg
import asyncio
from app.dataBase.db import connect_db


async def eliminar_actividades_expiradas():
    try:
        conn = await connect_db()
        await conn.execute("SELECT * FROM eliminar_actividades_expiradas();")
        print("Actividades expiradas eliminadas")
    except Exception as e:
        print(f"Error al eliminar actividades expiradas: {e}")
    finally:
        if conn:
            await conn.close()

def iniciar_scheduler():
    scheduler = AsyncIOScheduler()
    # Ejecutar cada hora
    scheduler.add_job(eliminar_actividades_expiradas, "interval", hours=1)
    scheduler.start()
