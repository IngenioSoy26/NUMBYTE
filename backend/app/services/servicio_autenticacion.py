import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.configuracion import configuracion
from app.core.seguridad import (
    crear_token_acceso,
    generar_token_restablecimiento,
    hashear_token,
    obtener_hash_contrasena,
    verificar_contrasena,
)
from app.models.modelos import TokenRestablecimiento, Usuario
from app.schemas.autenticacion import CredencialesIngreso, UsuarioCrear
from app.services.plantillas_correo import (
    plantilla_bienvenida,
    plantilla_contrasena_actualizada,
    plantilla_restablecer_contrasena,
)
from app.services.servicio_correo import ServicioCorreo

logger = logging.getLogger('numbyte.autenticacion')


class ServicioAutenticacion:
    """Encapsula la lógica de registro, ingreso y recuperación de contraseña."""

    def __init__(self, db: Session):
        self.db = db
        self.correo = ServicioCorreo()

    # --- Utilidades ---

    @staticmethod
    def _ahora_utc() -> datetime:
        """Fecha actual en UTC sin zona horaria (así se guarda en SQLite)."""
        return datetime.now(timezone.utc).replace(tzinfo=None)

    def _enviar_correo_seguro(self, destinatario: str, plantilla: dict) -> None:
        """Envía un correo sin que un fallo rompa el flujo principal."""
        try:
            self.correo.enviar(
                destinatario,
                plantilla['asunto'],
                plantilla['texto'],
                plantilla['html'],
            )
        except Exception as error:  # la entrega depende del servidor SMTP
            logger.warning('No se pudo enviar el correo a %s: %s', destinatario, error)

    # --- Registro e ingreso ---

    def crear_usuario(self, datos: UsuarioCrear) -> Usuario:
        usuario_existente = self.db.query(Usuario).filter(Usuario.correo == datos.correo).first()
        if usuario_existente:
            raise ValueError('Ya existe un usuario registrado con ese correo.')

        usuario = Usuario(
            nombre=datos.nombre,
            correo=datos.correo,
            contrasena_hash=obtener_hash_contrasena(datos.contrasena),
            grado=datos.grado,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)

        self._enviar_correo_seguro(
            usuario.correo,
            plantilla_bienvenida(usuario.nombre, usuario.correo, usuario.grado),
        )
        return usuario

    def autenticar_usuario(self, credenciales: CredencialesIngreso) -> str:
        usuario = self.db.query(Usuario).filter(Usuario.correo == credenciales.correo).first()
        if not usuario or not verificar_contrasena(credenciales.contrasena, usuario.contrasena_hash):
            raise ValueError('Correo o contraseña incorrectos.')

        return crear_token_acceso({'sub': str(usuario.id), 'correo': usuario.correo})

    # --- Recuperación de contraseña ---

    def solicitar_restablecimiento(self, correo: str) -> None:
        """Genera el enlace de recuperación y lo envía al correo del usuario.

        No revelamos si el correo existe: si no hay usuario, no se hace nada.
        """
        usuario = self.db.query(Usuario).filter(Usuario.correo == correo).first()
        if not usuario:
            return

        # Anulamos los tokens anteriores que todavía no se hayan usado.
        self.db.query(TokenRestablecimiento).filter(
            TokenRestablecimiento.usuario_id == usuario.id,
            TokenRestablecimiento.usado.is_(False),
        ).update({'usado': True})

        token_plano = generar_token_restablecimiento()
        registro = TokenRestablecimiento(
            usuario_id=usuario.id,
            token_hash=hashear_token(token_plano),
            expira_en=self._ahora_utc()
            + timedelta(minutes=configuracion.app_expiracion_reset_minutos),
        )
        self.db.add(registro)
        self.db.commit()

        enlace = (
            f'{configuracion.app_url_frontend.rstrip("/")}/restablecer?token={token_plano}'
        )
        self._enviar_correo_seguro(
            usuario.correo,
            plantilla_restablecer_contrasena(
                usuario.nombre, enlace, configuracion.app_expiracion_reset_minutos
            ),
        )

    def restablecer_contrasena(self, token: str, nueva_contrasena: str) -> None:
        """Valida el token y cambia la contraseña del usuario."""
        registro = (
            self.db.query(TokenRestablecimiento)
            .filter(
                TokenRestablecimiento.token_hash == hashear_token(token),
                TokenRestablecimiento.usado.is_(False),
            )
            .first()
        )
        if not registro:
            raise ValueError('El enlace de recuperación no es válido o ya fue utilizado.')

        if registro.expira_en < self._ahora_utc():
            registro.usado = True
            self.db.commit()
            raise ValueError('El enlace de recuperación expiró. Solicita uno nuevo.')

        usuario = self.db.query(Usuario).filter(Usuario.id == registro.usuario_id).first()
        if not usuario:
            raise ValueError('No se encontró el usuario asociado al enlace.')

        usuario.contrasena_hash = obtener_hash_contrasena(nueva_contrasena)
        registro.usado = True
        self.db.commit()

        self._enviar_correo_seguro(
            usuario.correo,
            plantilla_contrasena_actualizada(
                usuario.nombre, self._ahora_utc().strftime('%d/%m/%Y %H:%M')
            ),
        )
