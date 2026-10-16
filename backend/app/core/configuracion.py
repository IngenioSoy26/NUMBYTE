from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """Configuración central de la aplicación.

    Aquí dejamos todo lo que podría cambiar entre ambientes.
    Mantener esto separado del resto del código ayuda bastante
    cuando llega el momento de desplegar.
    """

    app_nombre: str = "NUMBYTE API"
    app_ambiente: str = "desarrollo"
    app_llave_secreta: str = "NUMBYTE_LLAVE_SEGURA_2026_CAMBIAR_EN_PRODUCCION"
    app_algoritmo_jwt: str = "HS256"
    app_expiracion_token_minutos: int = 1440
    app_url_bd: str = "sqlite:///./numbyte.db"
    cors_origenes: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Enlace del frontend, usado para construir links en los correos.
    app_url_frontend: str = "http://127.0.0.1:5173"
    # Minutos de vigencia del enlace para restablecer la contraseña.
    app_expiracion_reset_minutos: int = 30

    # Railway (y otros proveedores) inyectan la conexión como DATABASE_URL.
    # Si está presente, tiene prioridad sobre APP_URL_BD.
    database_url: str = ""

    # --- Envío de correo ---
    # 'simulado' escribe el correo en consola y en la carpeta correos_simulados.
    # 'smtp' envía de verdad usando los datos de abajo.
    correo_modo: str = "simulado"
    smtp_host: str = ""
    smtp_puerto: int = 587
    smtp_usuario: str = ""
    smtp_contrasena: str = ""
    smtp_remitente: str = "NUMBYTE <no-responder@numbyte.local>"
    smtp_usar_tls: bool = True

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')

    @property
    def lista_origenes_cors(self) -> list[str]:
        return [origen.strip() for origen in self.cors_origenes.split(',') if origen.strip()]

    @property
    def url_bd(self) -> str:
        """Cadena de conexión lista para SQLAlchemy.

        Normaliza los prefijos que usan los proveedores gestionados
        (`postgres://` y `postgresql://`) al driver `psycopg` de SQLAlchemy 2.
        """
        url = (self.database_url or self.app_url_bd).strip()
        for prefijo in ('postgres://', 'postgresql://'):
            if url.startswith(prefijo):
                return 'postgresql+psycopg://' + url[len(prefijo):]
        return url

    @property
    def es_sqlite(self) -> bool:
        return self.url_bd.startswith('sqlite')

    @property
    def es_produccion(self) -> bool:
        return self.app_ambiente.strip().lower() in {'produccion', 'production', 'prod'}


configuracion = Configuracion()
