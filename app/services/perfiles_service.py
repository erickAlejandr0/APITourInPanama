import uuid
from urllib.parse import urlparse
from supabase import Client
from fastapi import UploadFile
from typing import Optional

def obtener_ruta_storage(url: str, bucket: str) -> str:
    parsed_url = urlparse(url)
    prefix = f"/storage/v1/object/public/{bucket}/"
    if parsed_url.path.startswith(prefix):
        return parsed_url.path[len(prefix):]
    else:
        return parsed_url.path.lstrip("/")

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
        res = supabase.storage.from_(bucket).remove([ruta_borrar])
        if res.error:
            print(f"Error borrando archivo anterior: {res.error}")

    # 3. Subir nueva imagen
    extension = file.filename.split(".")[-1].lower()
    nuevo_nombre = f"{uuid.uuid4()}.{extension}"
    contenido = await file.read()

    res_upload = supabase.storage.from_(bucket).upload(
        nuevo_nombre, contenido, {"contentType": f"image/{extension}"}
    )
    if res_upload.error:
        print(f"Error subiendo archivo: {res_upload.error}")
        return None

    # 4. Obtener URL pública
    nueva_url = supabase.storage.from_(bucket).get_public_url(nuevo_nombre).public_url

    # 5. Actualizar tabla perfil
    res_update = supabase.table("perfil").update({"foto_perfil": nueva_url}).eq("id_usuario", user_id).execute()
    if res_update.error:
        print(f"Error actualizando la BD: {res_update.error}")
        return None

    return nueva_url
