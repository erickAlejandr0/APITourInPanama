import uuid
from urllib.parse import urlparse
from supabase import Client
from fastapi import UploadFile
from typing import Optional
from urllib.parse import unquote

def obtener_ruta_storage(url: str, bucket: str) -> str:
    parsed_url = urlparse(url)
    # Normalizar el path para quitar doble slash
    path = parsed_url.path.replace('//', '/')
    prefix = f"/storage/v1/object/public/{bucket}/"

    if path.startswith(prefix):
        ruta = path[len(prefix):]
    else:
        ruta = path.lstrip("/")

    return unquote(ruta)
    

async def cargar_nueva_foto(
    supabase: Client,
    bucket: str,
    user_id: str,
    file: UploadFile,
) -> Optional[str]:
    # 1. Obtener imagen actual
    perfil = supabase.table("perfil").select("foto_perfil").eq("id_usuario", user_id).single().execute()
    imagen_actual = perfil.data["foto_perfil"] if perfil.data else None

    # 2. Borrar si hay imagen previa
    if imagen_actual:
        ruta_borrar = obtener_ruta_storage(imagen_actual, bucket)
        print(f"ruta a borrar: {ruta_borrar}")
        try:
            res = supabase.storage.from_(bucket).remove([ruta_borrar])
            # res puede ser lista de nombres eliminados, si quieres imprimir:
            print(f"Archivos eliminados: {res}")
        except Exception as e:
            print(f"Error borrando archivo anterior: {e}")

    # 3. Subir nueva imagen
    extension = file.filename.split(".")[-1].lower()
    nuevo_nombre = f"{uuid.uuid4()}.{extension}"
    contenido = await file.read()

    try:
        res_upload = supabase.storage.from_(bucket).upload(
            nuevo_nombre, contenido, {"contentType": f"image/{extension}"}
        )
        # Aquí también puedes verificar si res_upload es error o no según doc
    except Exception as e:
        print(f"Error subiendo archivo: {e}")
        return None

    # 4. Obtener URL pública
    nueva_url = supabase.storage.from_(bucket).get_public_url(nuevo_nombre)

    # 5. Actualizar tabla perfil
    try:
        res_update = supabase.table("perfil").update({"foto_perfil": nueva_url}).eq("id_usuario", user_id).execute()
    except Exception as e:
        print(f"Error actualizando la BD: {e}")
        return None

    return nueva_url
