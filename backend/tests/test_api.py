import os
import re
from pathlib import Path

os.environ['APP_URL_BD'] = 'sqlite:///./numbyte_test.db'
os.environ['CORS_ORIGENES'] = 'http://localhost:5173'

from fastapi.testclient import TestClient

from app.main import aplicacion


def obtener_token_demo(cliente: TestClient) -> str:
    respuesta = cliente.post(
        '/api/autenticacion/ingresar',
        json={'correo': 'estudiante@numbyte.com', 'contrasena': 'Numbyte2026*'},
    )
    assert respuesta.status_code == 200
    return respuesta.json()['access_token']


def test_salud():
    with TestClient(aplicacion) as cliente:
        respuesta = cliente.get('/salud')
        assert respuesta.status_code == 200
        assert respuesta.json()['estado'] == 'ok'


def test_registro_usuario():
    with TestClient(aplicacion) as cliente:
        respuesta = cliente.post(
            '/api/autenticacion/registro',
            json={
                'nombre': 'Aprendiz Nuevo',
                'correo': 'aprendiz_nuevo@numbyte.com',
                'contrasena': 'ClaveSegura123',
                'grado': '9',
            },
        )
        assert respuesta.status_code == 201
        assert respuesta.json()['correo'] == 'aprendiz_nuevo@numbyte.com'


def test_generar_y_calificar_evaluacion():
    with TestClient(aplicacion) as cliente:
        token = obtener_token_demo(cliente)
        cabeceras = {'Authorization': f'Bearer {token}'}

        generacion = cliente.post(
            '/api/evaluaciones/generar',
            headers=cabeceras,
            json={
                'tipo_evaluacion': 'diagnostico',
                'grado': '10',
                'cantidad_preguntas': 3,
            },
        )
        assert generacion.status_code == 200
        preguntas = generacion.json()['preguntas']
        assert len(preguntas) >= 1

        respuestas = []
        for pregunta in preguntas:
            respuestas.append(
                {
                    'pregunta_id': pregunta['id'],
                    'opcion_id': pregunta['opciones'][0]['id'],
                }
            )

        calificacion = cliente.post(
            '/api/evaluaciones/calificar',
            headers=cabeceras,
            json={
                'tipo_evaluacion': 'diagnostico',
                'grado': '10',
                'tiempo_utilizado_segundos': 120,
                'respuestas': respuestas,
            },
        )
        assert calificacion.status_code == 200
        cuerpo = calificacion.json()
        assert 'porcentaje_aciertos' in cuerpo
        assert 'interpretacion_pedagogica' in cuerpo


def test_resumen_progreso():
    with TestClient(aplicacion) as cliente:
        token = obtener_token_demo(cliente)
        cabeceras = {'Authorization': f'Bearer {token}'}
        respuesta = cliente.get('/api/progreso/resumen', headers=cabeceras)
        assert respuesta.status_code == 200
        assert 'tarjetas' in respuesta.json()


def _ultimo_correo_simulado() -> str:
    """Devuelve el texto del correo simulado más reciente que traiga un enlace."""
    carpeta = Path(__file__).resolve().parents[1] / 'correos_simulados'
    archivos = sorted(carpeta.glob('*.txt'), key=lambda p: p.stat().st_mtime, reverse=True)
    for archivo in archivos:
        contenido = archivo.read_text(encoding='utf-8')
        if 'token=' in contenido:
            return contenido
    raise AssertionError('No se encontró un correo simulado con enlace de recuperación.')


def test_recuperacion_y_restablecimiento_contrasena():
    correo = 'recuperacion_test@numbyte.com'
    with TestClient(aplicacion) as cliente:
        # Registramos (si ya existe, el registro responde 400 y continuamos).
        cliente.post(
            '/api/autenticacion/registro',
            json={
                'nombre': 'Usuario Recuperación',
                'correo': correo,
                'contrasena': 'ClaveInicial123',
                'grado': '8',
            },
        )

        # 1) Solicitar el enlace de recuperación.
        solicitud = cliente.post('/api/autenticacion/recuperar', json={'correo': correo})
        assert solicitud.status_code == 200

        # 2) El correo simulado contiene el token del enlace.
        coincidencia = re.search(r'token=([A-Za-z0-9_\-]+)', _ultimo_correo_simulado())
        assert coincidencia is not None
        token = coincidencia.group(1)

        # 3) Restablecer con el token.
        restablecer = cliente.post(
            '/api/autenticacion/restablecer',
            json={'token': token, 'nueva_contrasena': 'NuevaClave2026*'},
        )
        assert restablecer.status_code == 200

        # 4) El token es de un solo uso.
        reintento = cliente.post(
            '/api/autenticacion/restablecer',
            json={'token': token, 'nueva_contrasena': 'OtraClave2026*'},
        )
        assert reintento.status_code == 400

        # 5) Se puede ingresar con la nueva contraseña.
        ingreso = cliente.post(
            '/api/autenticacion/ingresar',
            json={'correo': correo, 'contrasena': 'NuevaClave2026*'},
        )
        assert ingreso.status_code == 200


def test_recuperacion_correo_no_registrado_responde_igual():
    with TestClient(aplicacion) as cliente:
        respuesta = cliente.post(
            '/api/autenticacion/recuperar',
            json={'correo': 'no_existe_numbyte@numbyte.com'},
        )
        assert respuesta.status_code == 200
