import logging
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path

from app.core.configuracion import configuracion

logger = logging.getLogger('numbyte.correo')

# Carpeta donde quedan los correos cuando se trabaja en modo simulado.
CARPETA_CORREOS_SIMULADOS = Path(__file__).resolve().parents[2] / 'correos_simulados'


class ServicioCorreo:
    """Envío de correos con dos modos.

    - 'simulado': no envía nada real; guarda el correo en la carpeta
      `correos_simulados` y lo imprime en consola. Es el modo por defecto
      para la demostración.
    - 'smtp': envía el correo de verdad usando los datos de configuración.
    """

    def enviar(self, destinatario: str, asunto: str, cuerpo_texto: str, cuerpo_html: str) -> bool:
        if configuracion.correo_modo.lower() == 'smtp':
            return self._enviar_smtp(destinatario, asunto, cuerpo_texto, cuerpo_html)
        return self._enviar_simulado(destinatario, asunto, cuerpo_texto, cuerpo_html)

    def _enviar_simulado(
        self, destinatario: str, asunto: str, cuerpo_texto: str, cuerpo_html: str
    ) -> bool:
        CARPETA_CORREOS_SIMULADOS.mkdir(parents=True, exist_ok=True)
        marca = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        archivo = CARPETA_CORREOS_SIMULADOS / marca

        archivo.with_suffix('.txt').write_text(
            f'Para: {destinatario}\nAsunto: {asunto}\n\n{cuerpo_texto}\n',
            encoding='utf-8',
        )
        archivo.with_suffix('.html').write_text(cuerpo_html, encoding='utf-8')

        logger.info('CORREO SIMULADO -> %s | %s', destinatario, asunto)
        print(
            f'\n===== CORREO SIMULADO =====\nPara: {destinatario}\nAsunto: {asunto}\n'
            f'{cuerpo_texto}\n===========================\n'
        )
        return True

    def _enviar_smtp(
        self, destinatario: str, asunto: str, cuerpo_texto: str, cuerpo_html: str
    ) -> bool:
        mensaje = EmailMessage()
        mensaje['From'] = configuracion.smtp_remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.set_content(cuerpo_texto)
        mensaje.add_alternative(cuerpo_html, subtype='html')

        with smtplib.SMTP(configuracion.smtp_host, configuracion.smtp_puerto) as servidor:
            if configuracion.smtp_usar_tls:
                servidor.starttls()
            if configuracion.smtp_usuario:
                servidor.login(configuracion.smtp_usuario, configuracion.smtp_contrasena)
            servidor.send_message(mensaje)

        logger.info('CORREO SMTP -> %s | %s', destinatario, asunto)
        return True
