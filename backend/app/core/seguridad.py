from datetime import datetime, timedelta, timezone
import base64
import hashlib
import hmac
import os
import secrets

import jwt

from app.core.configuracion import configuracion


def obtener_hash_contrasena(contrasena: str) -> str:
    """Genera un hash con PBKDF2.

    No es el mecanismo más sofisticado del mundo, pero es seguro,
    no depende de paquetes externos y para este MVP funciona muy bien.
    El formato guardado es: salt$hash
    """
    sal = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac('sha256', contrasena.encode('utf-8'), sal, 120000)
    sal_texto = base64.b64encode(sal).decode('utf-8')
    hash_texto = base64.b64encode(hash_bytes).decode('utf-8')
    return f'{sal_texto}${hash_texto}'


def verificar_contrasena(contrasena_plana: str, contrasena_hash: str) -> bool:
    """Compara una contraseña plana contra el valor guardado."""
    try:
        sal_texto, hash_guardado = contrasena_hash.split('$', 1)
        sal = base64.b64decode(sal_texto.encode('utf-8'))
        nuevo_hash = hashlib.pbkdf2_hmac('sha256', contrasena_plana.encode('utf-8'), sal, 120000)
        nuevo_hash_texto = base64.b64encode(nuevo_hash).decode('utf-8')
        return hmac.compare_digest(nuevo_hash_texto, hash_guardado)
    except Exception:
        return False


def crear_token_acceso(datos: dict) -> str:
    carga = datos.copy()
    expiracion = datetime.now(timezone.utc) + timedelta(
        minutes=configuracion.app_expiracion_token_minutos
    )
    carga.update({'exp': expiracion})
    return jwt.encode(
        carga,
        configuracion.app_llave_secreta,
        algorithm=configuracion.app_algoritmo_jwt,
    )


def generar_token_restablecimiento() -> str:
    """Crea un token aleatorio para el enlace de recuperación."""
    return secrets.token_urlsafe(32)


def hashear_token(token: str) -> str:
    """Devuelve el hash del token para guardarlo sin exponerlo."""
    return hashlib.sha256(token.encode('utf-8')).hexdigest()
