"""Servicio de aprendizaje: ruta de microaprendizaje y actividades de clic.

Cada tema del módulo (grado 6°) se presenta como un ítem de ruta que reúne:
una lección corta (explicación + ejemplo), una actividad interactiva y un
recurso de video. Al completar cada parte se otorgan puntos y se avanza en las
misiones de gamificación.
"""

import json

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.modelos import (
    ActividadInteractiva,
    ActividadUsuario,
    Leccion,
    LeccionUsuario,
    RecursoMultimedia,
    Usuario,
)
from app.services.servicio_gamificacion import ServicioGamificacion


class ServicioAprendizaje:
    def __init__(self, db: Session):
        self.db = db
        self.gamificacion = ServicioGamificacion(db)

    # --- Ruta ---
    def construir_ruta(self, usuario: Usuario, grado: str) -> dict:
        lecciones = (
            self.db.query(Leccion).filter(Leccion.grado == grado).order_by(Leccion.orden).all()
        )
        actividades = {
            actividad.tema: actividad
            for actividad in self.db.query(ActividadInteractiva)
            .filter(ActividadInteractiva.grado == grado)
            .all()
        }
        recursos = {
            recurso.tema: recurso
            for recurso in self.db.query(RecursoMultimedia)
            .filter(RecursoMultimedia.grado == grado)
            .all()
        }

        lecciones_completadas = {
            fila.leccion_id
            for fila in self.db.query(LeccionUsuario).filter(LeccionUsuario.usuario_id == usuario.id).all()
        }
        actividades_completadas = {
            fila.actividad_id
            for fila in self.db.query(ActividadUsuario)
            .filter(ActividadUsuario.usuario_id == usuario.id, ActividadUsuario.correcta.is_(True))
            .all()
        }

        items = []
        for leccion in lecciones:
            actividad = actividades.get(leccion.tema)
            recurso = recursos.get(leccion.tema)
            leccion_ok = leccion.id in lecciones_completadas
            actividad_ok = bool(actividad and actividad.id in actividades_completadas)
            partes = [leccion_ok, actividad_ok]
            progreso = int((sum(1 for parte in partes if parte) / len(partes)) * 100)

            items.append(
                {
                    'tema': leccion.tema,
                    'orden': leccion.orden,
                    'leccion': self._serializar_leccion(leccion),
                    'actividad': self._serializar_actividad(actividad, usuario) if actividad else None,
                    'recurso': self._serializar_recurso(recurso, usuario) if recurso else None,
                    'leccion_completada': leccion_ok,
                    'actividad_completada': actividad_ok,
                    'progreso': progreso,
                }
            )

        total_items = len(items)
        items_completados = sum(1 for item in items if item['leccion_completada'] and item['actividad_completada'])
        porcentaje = round((items_completados / total_items) * 100, 2) if total_items else 0

        return {
            'grado': grado,
            'total_items': total_items,
            'items_completados': items_completados,
            'porcentaje': porcentaje,
            'items': items,
        }

    # --- Lecciones ---
    def completar_leccion(self, usuario: Usuario, leccion_id: int) -> dict:
        leccion = self.db.query(Leccion).filter(Leccion.id == leccion_id).first()
        if not leccion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Lección no encontrada.')

        ya_completada = (
            self.db.query(LeccionUsuario)
            .filter(LeccionUsuario.usuario_id == usuario.id, LeccionUsuario.leccion_id == leccion.id)
            .first()
        )
        if ya_completada:
            return {
                'puntos_ganados': 0,
                'monedas_ganadas': 0,
                'subio_nivel': False,
                'perfil': self.gamificacion.serializar_perfil(
                    self.gamificacion.obtener_o_crear_perfil(usuario)
                ),
                'insignias_nuevas': [],
                'misiones_completadas': [],
            }

        self.db.add(LeccionUsuario(usuario_id=usuario.id, leccion_id=leccion.id))
        self.db.flush()

        misiones = self.gamificacion.actualizar_misiones(usuario, 'lecciones', 1)
        recompensa = self.gamificacion.construir_recompensa(
            usuario, leccion.puntos, max(leccion.puntos // 4, 1), misiones
        )
        return recompensa

    # --- Actividades ---
    def obtener_actividad(self, usuario: Usuario, actividad_id: int) -> dict:
        actividad = self.db.query(ActividadInteractiva).filter(ActividadInteractiva.id == actividad_id).first()
        if not actividad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Actividad no encontrada.')
        return self._serializar_actividad(actividad, usuario)

    def responder_actividad(self, usuario: Usuario, actividad_id: int, respuestas: dict) -> dict:
        actividad = self.db.query(ActividadInteractiva).filter(ActividadInteractiva.id == actividad_id).first()
        if not actividad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Actividad no encontrada.')
        if actividad.solo_plus and not usuario.es_plus:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Esta actividad es exclusiva del plan Plus.',
            )

        datos = json.loads(actividad.datos or '{}')
        correctas, total = self._calificar(actividad.tipo, datos, respuestas or {})
        puntaje = int(round((correctas / total) * actividad.puntos)) if total else 0
        aprobada = total > 0 and correctas == total

        self.db.add(
            ActividadUsuario(
                usuario_id=usuario.id,
                actividad_id=actividad.id,
                correcta=aprobada,
                puntaje=puntaje,
            )
        )
        self.db.flush()

        misiones = []
        recompensa = {
            'puntos_ganados': 0,
            'monedas_ganadas': 0,
            'subio_nivel': False,
            'perfil': self.gamificacion.serializar_perfil(
                self.gamificacion.obtener_o_crear_perfil(usuario)
            ),
            'insignias_nuevas': [],
            'misiones_completadas': [],
        }
        if aprobada:
            misiones = self.gamificacion.actualizar_misiones(usuario, 'actividades', 1)
            recompensa = self.gamificacion.construir_recompensa(
                usuario, puntaje, max(puntaje // 4, 1), misiones
            )

        return {
            'correcta': aprobada,
            'puntaje': puntaje,
            'total': total,
            'recompensa': recompensa,
        }

    @staticmethod
    def _calificar(tipo: str, datos: dict, respuestas: dict) -> tuple[int, int]:
        if tipo == 'seleccionar':
            opciones = datos.get('opciones', [])
            correcta = next((opcion['id'] for opcion in opciones if opcion.get('correcta')), None)
            seleccion = respuestas.get('seleccion')
            return (1 if seleccion and seleccion == correcta else 0), 1

        if tipo == 'clasificar':
            elementos = datos.get('elementos', [])
            aciertos = 0
            for elemento in elementos:
                if respuestas.get(elemento['id']) == elemento.get('categoria'):
                    aciertos += 1
            return aciertos, len(elementos)

        return 0, max(len(respuestas), 1)

    # --- Serializadores ---
    @staticmethod
    def _serializar_leccion(leccion: Leccion) -> dict:
        return {
            'id': leccion.id,
            'grado': leccion.grado,
            'tema': leccion.tema,
            'titulo': leccion.titulo,
            'subtitulo': leccion.subtitulo,
            'explicacion': leccion.explicacion,
            'ejemplo': leccion.ejemplo,
            'puntos': leccion.puntos,
            'orden': leccion.orden,
        }

    @staticmethod
    def _serializar_actividad(actividad: ActividadInteractiva, usuario: Usuario) -> dict:
        bloqueada = actividad.solo_plus and not usuario.es_plus
        return {
            'id': actividad.id,
            'grado': actividad.grado,
            'tema': actividad.tema,
            'titulo': actividad.titulo,
            'instrucciones': actividad.instrucciones,
            'tipo': actividad.tipo,
            'datos': json.loads(actividad.datos or '{}') if not bloqueada else {},
            'puntos': actividad.puntos,
            'solo_plus': actividad.solo_plus,
            'bloqueada': bloqueada,
        }

    @staticmethod
    def _serializar_recurso(recurso: RecursoMultimedia, usuario: Usuario) -> dict:
        from app.services.servicio_recursos import ServicioRecursos

        return ServicioRecursos._serializar(recurso, usuario)
