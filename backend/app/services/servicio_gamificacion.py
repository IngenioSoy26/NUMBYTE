"""Servicio de gamificación: puntos, monedas, niveles, rachas, insignias y misiones.

Todo el sistema es demostrativo: no existen premios ni dinero real. Las monedas
son un recurso interno de juego y el plan Plus tampoco genera cobros.
"""

from datetime import date, datetime, timezone

from sqlalchemy.orm import Session

from app.models.modelos import (
    ActividadUsuario,
    Insignia,
    InsigniaUsuario,
    LeccionUsuario,
    Mision,
    MisionUsuario,
    PerfilGamificacion,
    ProgresoTema,
    ResultadoEvaluacion,
    Usuario,
)

PUNTOS_POR_NIVEL = 100


class ServicioGamificacion:
    def __init__(self, db: Session):
        self.db = db

    # --- Perfil ---
    def obtener_o_crear_perfil(self, usuario: Usuario) -> PerfilGamificacion:
        perfil = (
            self.db.query(PerfilGamificacion)
            .filter(PerfilGamificacion.usuario_id == usuario.id)
            .first()
        )
        if perfil:
            return perfil

        perfil = PerfilGamificacion(usuario_id=usuario.id, puntos=0, monedas=0, nivel=1)
        self.db.add(perfil)
        self.db.flush()
        # Insignia de bienvenida al crear el perfil de juego.
        insignia_bienvenida = self._otorgar_insignia_si_corresponde(usuario, 'primer_paso')
        if insignia_bienvenida:
            perfil.puntos += insignia_bienvenida['puntos_otorgados']
            perfil.nivel = (perfil.puntos // PUNTOS_POR_NIVEL) + 1
        self.db.commit()
        self.db.refresh(perfil)
        return perfil

    # --- Puntos y niveles ---
    def otorgar_puntos(self, usuario: Usuario, puntos: int, monedas: int) -> dict:
        """Suma puntos/monedas, recalcula el nivel y actualiza la racha diaria."""
        perfil = self.obtener_o_crear_perfil(usuario)
        nivel_anterior = perfil.nivel

        perfil.puntos += max(puntos, 0)
        perfil.monedas += max(monedas, 0)
        perfil.nivel = (perfil.puntos // PUNTOS_POR_NIVEL) + 1
        self._actualizar_racha(perfil)

        self.db.flush()
        insignias_nuevas = self._evaluar_insignias(usuario)
        self.db.commit()
        self.db.refresh(perfil)

        return {
            'subio_nivel': perfil.nivel > nivel_anterior,
            'insignias_nuevas': insignias_nuevas,
        }

    def _actualizar_racha(self, perfil: PerfilGamificacion):
        hoy = datetime.now(timezone.utc).date()
        if perfil.ultima_actividad == hoy:
            return
        if perfil.ultima_actividad is not None:
            diferencia = (hoy - perfil.ultima_actividad).days
            if diferencia == 1:
                perfil.racha_actual += 1
            elif diferencia > 1:
                perfil.racha_actual = 1
        else:
            perfil.racha_actual = 1

        perfil.racha_maxima = max(perfil.racha_maxima, perfil.racha_actual)
        perfil.ultima_actividad = hoy

    # --- Insignias ---
    def _evaluar_insignias(self, usuario: Usuario) -> list[dict]:
        """Revisa las condiciones de todas las insignias y otorga las nuevas."""
        perfil = self.obtener_o_crear_perfil(usuario)
        nuevas: list[dict] = []

        lecciones_completadas = self._contar_lecciones(usuario)
        temas_perfectos = self._temas_perfectos(usuario)
        simulacro_perfecto = self._simulacro_perfecto(usuario)
        total_obtenidas = self._contar_insignias(usuario)

        condiciones = {
            'explorador': lecciones_completadas >= 1,
            'fraccionista': temas_perfectos >= 1,
            'constante': perfil.racha_actual >= 3 or perfil.racha_maxima >= 3,
            'calculadora': simulacro_perfecto,
            'sabio': perfil.nivel >= 5,
            'coleccionista': total_obtenidas >= 5,
            'plus_oro': usuario.es_plus,
        }

        for codigo, cumple in condiciones.items():
            if cumple:
                insignia = self._otorgar_insignia_si_corresponde(usuario, codigo)
                if insignia:
                    nuevas.append(insignia)
                    if insignia.get('puntos_otorgados'):
                        perfil.puntos += insignia['puntos_otorgados']
                        perfil.nivel = (perfil.puntos // PUNTOS_POR_NIVEL) + 1

        return nuevas

    def _otorgar_insignia_si_corresponde(self, usuario: Usuario, codigo: str) -> dict | None:
        insignia = self.db.query(Insignia).filter(Insignia.codigo == codigo).first()
        if not insignia:
            return None
        if insignia.solo_plus and not usuario.es_plus:
            return None

        existente = (
            self.db.query(InsigniaUsuario)
            .filter(
                InsigniaUsuario.usuario_id == usuario.id,
                InsigniaUsuario.insignia_id == insignia.id,
            )
            .first()
        )
        if existente:
            return None

        self.db.add(InsigniaUsuario(usuario_id=usuario.id, insignia_id=insignia.id))
        self.db.flush()
        return {
            'codigo': insignia.codigo,
            'nombre': insignia.nombre,
            'descripcion': insignia.descripcion,
            'icono': insignia.icono,
            'puntos_otorgados': insignia.puntos_otorgados,
            'solo_plus': insignia.solo_plus,
            'obtenida': True,
        }

    # --- Misiones ---
    def actualizar_misiones(self, usuario: Usuario, tipo: str, incremento: int = 1) -> list[dict]:
        """Avanza el progreso de las misiones del tipo indicado y premia las completadas."""
        misiones = self.db.query(Mision).filter(Mision.tipo == tipo).all()
        completadas: list[dict] = []

        for mision in misiones:
            registro = (
                self.db.query(MisionUsuario)
                .filter(
                    MisionUsuario.usuario_id == usuario.id,
                    MisionUsuario.mision_id == mision.id,
                )
                .first()
            )
            if not registro:
                registro = MisionUsuario(usuario_id=usuario.id, mision_id=mision.id, progreso=0)
                self.db.add(registro)
                self.db.flush()

            if registro.completada:
                continue

            registro.progreso = min(registro.progreso + incremento, mision.meta)
            if registro.progreso >= mision.meta:
                registro.completada = True
                registro.fecha_completada = datetime.now(timezone.utc)
                perfil = self.obtener_o_crear_perfil(usuario)
                perfil.puntos += mision.puntos
                perfil.monedas += mision.monedas
                perfil.nivel = (perfil.puntos // PUNTOS_POR_NIVEL) + 1
                completadas.append(self._serializar_mision(mision, registro, usuario))

        self.db.flush()
        return completadas

    # --- Resumen ---
    def resumen(self, usuario: Usuario) -> dict:
        perfil = self.obtener_o_crear_perfil(usuario)
        insignias = self.db.query(Insignia).order_by(Insignia.id).all()
        obtenidas = {
            fila.insignia_id
            for fila in self.db.query(InsigniaUsuario).filter(InsigniaUsuario.usuario_id == usuario.id).all()
        }

        insignias_publicas = [
            {
                'codigo': insignia.codigo,
                'nombre': insignia.nombre,
                'descripcion': insignia.descripcion,
                'icono': insignia.icono,
                'puntos_otorgados': insignia.puntos_otorgados,
                'solo_plus': insignia.solo_plus,
                'obtenida': insignia.id in obtenidas,
            }
            for insignia in insignias
        ]

        misiones = self._listar_misiones(usuario)

        return {
            'perfil': self.serializar_perfil(perfil),
            'insignias': insignias_publicas,
            'misiones': misiones,
            'total_insignias': len(insignias),
            'insignias_obtenidas': len(obtenidas),
        }

    def _listar_misiones(self, usuario: Usuario) -> list[dict]:
        misiones = self.db.query(Mision).order_by(Mision.id).all()
        registros = {
            fila.mision_id: fila
            for fila in self.db.query(MisionUsuario).filter(MisionUsuario.usuario_id == usuario.id).all()
        }
        resultado = []
        for mision in misiones:
            registro = registros.get(mision.id)
            resultado.append(self._serializar_mision(mision, registro, usuario))
        return resultado

    def _serializar_mision(self, mision: Mision, registro: MisionUsuario | None, usuario: Usuario) -> dict:
        return {
            'codigo': mision.codigo,
            'titulo': mision.titulo,
            'descripcion': mision.descripcion,
            'tipo': mision.tipo,
            'meta': mision.meta,
            'puntos': mision.puntos,
            'monedas': mision.monedas,
            'solo_plus': mision.solo_plus,
            'progreso': registro.progreso if registro else 0,
            'completada': bool(registro and registro.completada),
            'bloqueada': mision.solo_plus and not usuario.es_plus,
        }

    @staticmethod
    def serializar_perfil(perfil: PerfilGamificacion) -> dict:
        puntos_nivel_actual = perfil.puntos % PUNTOS_POR_NIVEL
        return {
            'puntos': perfil.puntos,
            'monedas': perfil.monedas,
            'nivel': perfil.nivel,
            'puntos_nivel_actual': puntos_nivel_actual,
            'puntos_siguiente_nivel': PUNTOS_POR_NIVEL,
            'racha_actual': perfil.racha_actual,
            'racha_maxima': perfil.racha_maxima,
        }

    # --- Consultas auxiliares de condiciones ---
    def _contar_lecciones(self, usuario: Usuario) -> int:
        return self.db.query(LeccionUsuario).filter(LeccionUsuario.usuario_id == usuario.id).count()

    def _contar_actividades(self, usuario: Usuario) -> int:
        return (
            self.db.query(ActividadUsuario)
            .filter(ActividadUsuario.usuario_id == usuario.id, ActividadUsuario.correcta.is_(True))
            .count()
        )

    def _contar_insignias(self, usuario: Usuario) -> int:
        return self.db.query(InsigniaUsuario).filter(InsigniaUsuario.usuario_id == usuario.id).count()

    def _temas_perfectos(self, usuario: Usuario) -> int:
        return (
            self.db.query(ProgresoTema)
            .filter(ProgresoTema.usuario_id == usuario.id, ProgresoTema.porcentaje_aciertos >= 100)
            .count()
        )

    def _simulacro_perfecto(self, usuario: Usuario) -> bool:
        return (
            self.db.query(ResultadoEvaluacion)
            .filter(
                ResultadoEvaluacion.usuario_id == usuario.id,
                ResultadoEvaluacion.tipo_evaluacion == 'simulacro',
                ResultadoEvaluacion.porcentaje_aciertos >= 100,
            )
            .first()
            is not None
        )

    def construir_recompensa(self, usuario: Usuario, puntos: int, monedas: int, misiones_completadas: list[dict]) -> dict:
        resultado = self.otorgar_puntos(usuario, puntos, monedas)
        perfil = self.obtener_o_crear_perfil(usuario)
        return {
            'puntos_ganados': puntos,
            'monedas_ganadas': monedas,
            'subio_nivel': resultado['subio_nivel'],
            'perfil': self.serializar_perfil(perfil),
            'insignias_nuevas': resultado['insignias_nuevas'],
            'misiones_completadas': misiones_completadas,
        }
