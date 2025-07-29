from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncpg
import asyncio
from app.dataBase.db import connect_db

async def eliminar_actividades_expiradas():
    try:
        conn = await connect_db()
        await conn.execute("SELECT * FROM eliminar_actividades_expiradas()")
        print("Actividades expiradas eliminadas")
    except Exception as e:
        print(f"Error al eliminar actividades expiradas: {e}")
    finally:
        if conn:
            await conn.close()

async def iniciar_scheduler():
    print("Ejecutando limpieza inicial del itinerario en background...")
    asyncio.create_task(eliminar_actividades_expiradas())