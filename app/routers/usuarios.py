from fastapi import APIRouter, HTTPException, Request
import asyncpg
from app.Models.userModel import UsuarioNew, UsuarioRegistrado
from app.dataBase.db import connect_db

router= APIRouter( 
    prefix= "/user",
    tags= ["user"]
)
@router.post("/registrar")
async def reg_usuario(u: UsuarioNew):
    try:
        conn = await connect_db()
        result = await conn.fetchval(
            "SELECT * FROM registrar_usuario($1,$2,$3,$4,$5)",
            u.nombre,u.apellido,u.correo,u.contrasena,u.identificacion
        )
        if result:
            return{"registro": True,
                   "id_usuario": result}
    except Exception as e:
         raise HTTPException(500, f"Error inesperado: {str(e)}")
    except asyncpg.UniqueViolationError as e:
        raise HTTPException(400, f"El correo ya está registrado {str(e)}")

   
@router.post("/auth")
async def auth_usuario(u : UsuarioRegistrado):
    try:
        conn = await connect_db()
        result = await conn.fetchrow(
            "SELECT * FROM autenticar_usuario($1,$2)",
            u.email, u.password
        )
        await conn.close()
        if result:
            return(result)
        raise HTTPException(500,"error al autenticar")
    except Exception as e:
        raise HTTPException(500,f"Error al autenticar{str(e)}")
    

