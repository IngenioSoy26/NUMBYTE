"""Plantillas de los correos automáticos de NUMBYTE.

Cada función devuelve el asunto, el cuerpo en texto plano y el cuerpo en HTML.
"""


def _envolver_html(titulo: str, contenido: str) -> str:
    """Aplica el diseño institucional común a todos los correos."""
    return f"""<!DOCTYPE html>
<html lang="es">
  <body style="margin:0;padding:24px;background:#f2f7fb;font-family:Segoe UI,Arial,sans-serif;color:#1f2a37;">
    <div style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:20px;overflow:hidden;box-shadow:0 18px 50px rgba(6,42,99,0.08);">
      <div style="background:linear-gradient(135deg,#0d4ba0,#16c6df);padding:24px;text-align:center;">
        <h1 style="margin:0;color:#ffffff;font-size:22px;letter-spacing:1px;">NUMBYTE</h1>
      </div>
      <div style="padding:28px;">
        <h2 style="margin:0 0 16px;color:#062a63;font-size:19px;">{titulo}</h2>
        {contenido}
      </div>
      <div style="padding:18px;text-align:center;background:#f8fbff;color:#6b7a90;font-size:12px;">
        NUMBYTE &middot; Fortalecimiento de matem&aacute;ticas 6&deg; a 11&deg;<br />
        &copy; IngenioSoy - Todos los Derechos Reservados
      </div>
    </div>
  </body>
</html>"""


def plantilla_bienvenida(nombre: str, correo: str, grado: str) -> dict:
    asunto = 'Bienvenido a NUMBYTE'
    texto = (
        f'Hola {nombre},\n\n'
        'Tu cuenta en NUMBYTE quedó creada correctamente.\n\n'
        f'Correo registrado: {correo}\n'
        f'Grado: {grado}\n\n'
        'Ya puedes ingresar y comenzar a fortalecer tus matemáticas.\n\n'
        'Equipo NUMBYTE'
    )
    contenido = f"""
        <p style="margin:0 0 14px;line-height:1.6;">Hola <strong>{nombre}</strong>,</p>
        <p style="margin:0 0 14px;line-height:1.6;">
          Tu cuenta en NUMBYTE qued&oacute; creada correctamente.
        </p>
        <table style="width:100%;border-collapse:collapse;margin:0 0 18px;">
          <tr><td style="padding:8px 0;color:#6b7a90;">Correo registrado</td>
              <td style="padding:8px 0;text-align:right;font-weight:600;">{correo}</td></tr>
          <tr><td style="padding:8px 0;color:#6b7a90;">Grado</td>
              <td style="padding:8px 0;text-align:right;font-weight:600;">{grado}</td></tr>
        </table>
        <p style="margin:0;line-height:1.6;">
          Ya puedes ingresar y comenzar a fortalecer tus matem&aacute;ticas.
        </p>
    """
    return {'asunto': asunto, 'texto': texto, 'html': _envolver_html(asunto, contenido)}


def plantilla_restablecer_contrasena(nombre: str, enlace: str, minutos_vigencia: int) -> dict:
    asunto = 'Restablece tu contraseña de NUMBYTE'
    texto = (
        f'Hola {nombre},\n\n'
        'Recibimos una solicitud para restablecer tu contraseña de NUMBYTE.\n\n'
        f'Abre este enlace para crear una nueva contraseña (válido por {minutos_vigencia} minutos):\n'
        f'{enlace}\n\n'
        'Si no solicitaste este cambio, ignora este correo.\n\n'
        'Equipo NUMBYTE'
    )
    contenido = f"""
        <p style="margin:0 0 14px;line-height:1.6;">Hola <strong>{nombre}</strong>,</p>
        <p style="margin:0 0 18px;line-height:1.6;">
          Recibimos una solicitud para restablecer tu contrase&ntilde;a de NUMBYTE.
        </p>
        <div style="text-align:center;margin:0 0 18px;">
          <a href="{enlace}"
             style="display:inline-block;padding:14px 26px;border-radius:999px;background:linear-gradient(135deg,#0d4ba0,#16c6df);color:#ffffff;text-decoration:none;font-weight:600;">
            Crear nueva contrase&ntilde;a
          </a>
        </div>
        <p style="margin:0 0 14px;line-height:1.6;color:#6b7a90;font-size:13px;">
          El enlace es v&aacute;lido por {minutos_vigencia} minutos y solo puede usarse una vez.
        </p>
        <p style="margin:0;line-height:1.6;color:#6b7a90;font-size:13px;">
          Si no solicitaste este cambio, ignora este correo.
        </p>
    """
    return {'asunto': asunto, 'texto': texto, 'html': _envolver_html(asunto, contenido)}


def plantilla_contrasena_actualizada(nombre: str, fecha: str) -> dict:
    asunto = 'Tu contraseña de NUMBYTE fue actualizada'
    texto = (
        f'Hola {nombre},\n\n'
        f'Tu contraseña de NUMBYTE se cambió correctamente el {fecha}.\n\n'
        'Si no realizaste este cambio, comunícate de inmediato con el equipo NUMBYTE.\n\n'
        'Equipo NUMBYTE'
    )
    contenido = f"""
        <p style="margin:0 0 14px;line-height:1.6;">Hola <strong>{nombre}</strong>,</p>
        <p style="margin:0 0 14px;line-height:1.6;">
          Tu contrase&ntilde;a de NUMBYTE se cambi&oacute; correctamente el <strong>{fecha}</strong>.
        </p>
        <p style="margin:0;line-height:1.6;color:#b42318;">
          Si no realizaste este cambio, comun&iacute;cate de inmediato con el equipo NUMBYTE.
        </p>
    """
    return {'asunto': asunto, 'texto': texto, 'html': _envolver_html(asunto, contenido)}
