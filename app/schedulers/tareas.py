from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncpg
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

def iniciar_scheduler():
    print("Iniciando scheduler...")
    scheduler = AsyncIOScheduler()
    # Ejecutar cada hora
    scheduler.add_job(
        eliminar_actividades_expiradas,
        trigger="interval",
        minutes=3,
        id="eliminar_actividades_expiradas",  # opcional: para identificar el job
        replace_existing=True  # reemplaza si ya existe un job con el mismo ID
        
    )
    scheduler.start()
    print("Scheduler iniciado, itinerarios limpiados correctamente")
