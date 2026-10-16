from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

# Planes disponibles. El plan Plus es una demostración: no se cobra dinero real.
PLAN_GRATIS = 'gratis'
PLAN_PLUS = 'plus'


class Usuario(Base):
    __tablename__ = 'usuarios'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    contrasena_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    grado: Mapped[str] = mapped_column(String(10), nullable=False)
    estado_cuenta: Mapped[str] = mapped_column(String(30), default='activa')
    plan: Mapped[str] = mapped_column(String(20), default=PLAN_GRATIS)
    fecha_activacion_plan: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    resultados: Mapped[list['ResultadoEvaluacion']] = relationship(back_populates='usuario')
    progresos: Mapped[list['ProgresoTema']] = relationship(back_populates='usuario')
    perfil_juego: Mapped['PerfilGamificacion | None'] = relationship(
        back_populates='usuario', uselist=False, cascade='all, delete-orphan'
    )

    @property
    def es_plus(self) -> bool:
        return self.plan == PLAN_PLUS


class TokenRestablecimiento(Base):
    """Token de un solo uso para restablecer la contraseña.

    Guardamos solo el hash del token (nunca el valor plano) y dejamos
    la fecha de expiración para limitar su vigencia.
    """

    __tablename__ = 'tokens_restablecimiento'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    token_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    usado: Mapped[bool] = mapped_column(Boolean, default=False)
    expira_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class RecursoMultimedia(Base):
    __tablename__ = 'recursos_multimedia'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    tema: Mapped[str] = mapped_column(String(80), nullable=False)
    grado: Mapped[str] = mapped_column(String(10), default='6')
    autor: Mapped[str] = mapped_column(String(150), default='')
    descripcion: Mapped[str] = mapped_column(Text, default='')
    solo_plus: Mapped[bool] = mapped_column(Boolean, default=False)


class Pregunta(Base):
    __tablename__ = 'preguntas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    enunciado: Mapped[str] = mapped_column(Text, nullable=False)
    grado: Mapped[str] = mapped_column(String(10), nullable=False)
    tema: Mapped[str] = mapped_column(String(80), nullable=False)
    competencia: Mapped[str] = mapped_column(String(120), nullable=False)
    dba: Mapped[str] = mapped_column(String(180), nullable=False)
    nivel_dificultad: Mapped[str] = mapped_column(String(20), nullable=False)
    tipo_pregunta: Mapped[str] = mapped_column(String(30), default='seleccion_multiple')
    explicacion: Mapped[str] = mapped_column(Text, nullable=False)
    justificacion_pedagogica: Mapped[str] = mapped_column(Text, nullable=False)

    opciones: Mapped[list['OpcionRespuesta']] = relationship(
        back_populates='pregunta', cascade='all, delete-orphan'
    )


class OpcionRespuesta(Base):
    __tablename__ = 'opciones_respuesta'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pregunta_id: Mapped[int] = mapped_column(ForeignKey('preguntas.id'), nullable=False)
    identificador: Mapped[str] = mapped_column(String(5), nullable=False)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    es_correcta: Mapped[bool] = mapped_column(Boolean, default=False)
    explicacion_distractor: Mapped[str] = mapped_column(Text, default='')
    tipo_error: Mapped[str] = mapped_column(String(120), default='')

    pregunta: Mapped['Pregunta'] = relationship(back_populates='opciones')


class ResultadoEvaluacion(Base):
    __tablename__ = 'resultados_evaluacion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    tipo_evaluacion: Mapped[str] = mapped_column(String(30), nullable=False)
    grado: Mapped[str] = mapped_column(String(10), nullable=False)
    tema_principal: Mapped[str] = mapped_column(String(80), default='General')
    cantidad_preguntas: Mapped[int] = mapped_column(Integer, nullable=False)
    respuestas_correctas: Mapped[int] = mapped_column(Integer, nullable=False)
    respuestas_incorrectas: Mapped[int] = mapped_column(Integer, nullable=False)
    porcentaje_aciertos: Mapped[float] = mapped_column(Float, nullable=False)
    puntaje: Mapped[float] = mapped_column(Float, nullable=False)
    tiempo_utilizado_segundos: Mapped[int] = mapped_column(Integer, default=0)
    fortalezas: Mapped[str] = mapped_column(Text, default='')
    debilidades: Mapped[str] = mapped_column(Text, default='')
    interpretacion_pedagogica: Mapped[str] = mapped_column(Text, default='')
    recomendaciones: Mapped[str] = mapped_column(Text, default='')
    detalle_temas: Mapped[str] = mapped_column(Text, default='{}')
    detalle_competencias: Mapped[str] = mapped_column(Text, default='{}')
    fecha: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario: Mapped['Usuario'] = relationship(back_populates='resultados')
    respuestas: Mapped[list['RespuestaUsuario']] = relationship(
        back_populates='resultado', cascade='all, delete-orphan'
    )


class RespuestaUsuario(Base):
    __tablename__ = 'respuestas_usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resultado_id: Mapped[int] = mapped_column(ForeignKey('resultados_evaluacion.id'), nullable=False)
    pregunta_id: Mapped[int] = mapped_column(ForeignKey('preguntas.id'), nullable=False)
    opcion_seleccionada_id: Mapped[int | None] = mapped_column(ForeignKey('opciones_respuesta.id'))
    es_correcta: Mapped[bool] = mapped_column(Boolean, default=False)

    resultado: Mapped['ResultadoEvaluacion'] = relationship(back_populates='respuestas')


class ProgresoTema(Base):
    __tablename__ = 'progreso_tema'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    tema: Mapped[str] = mapped_column(String(80), nullable=False)
    competencia: Mapped[str] = mapped_column(String(120), nullable=False)
    intentos: Mapped[int] = mapped_column(Integer, default=0)
    porcentaje_aciertos: Mapped[float] = mapped_column(Float, default=0)
    porcentaje_errores: Mapped[float] = mapped_column(Float, default=0)
    fortalezas: Mapped[str] = mapped_column(Text, default='')
    debilidades: Mapped[str] = mapped_column(Text, default='')
    fecha_actualizacion: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario: Mapped['Usuario'] = relationship(back_populates='progresos')


class PerfilGamificacion(Base):
    """Estado de juego del estudiante: puntos, monedas, nivel y racha."""

    __tablename__ = 'perfiles_gamificacion'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), unique=True, nullable=False)
    puntos: Mapped[int] = mapped_column(Integer, default=0)
    monedas: Mapped[int] = mapped_column(Integer, default=0)
    nivel: Mapped[int] = mapped_column(Integer, default=1)
    racha_actual: Mapped[int] = mapped_column(Integer, default=0)
    racha_maxima: Mapped[int] = mapped_column(Integer, default=0)
    ultima_actividad: Mapped[date | None] = mapped_column(Date, nullable=True)

    usuario: Mapped['Usuario'] = relationship(back_populates='perfil_juego')


class Insignia(Base):
    __tablename__ = 'insignias'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default='')
    icono: Mapped[str] = mapped_column(String(10), default='*')
    puntos_otorgados: Mapped[int] = mapped_column(Integer, default=0)
    solo_plus: Mapped[bool] = mapped_column(Boolean, default=False)


class InsigniaUsuario(Base):
    __tablename__ = 'insignias_usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    insignia_id: Mapped[int] = mapped_column(ForeignKey('insignias.id'), nullable=False)
    fecha_obtenida: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class Mision(Base):
    """Reto con una meta concreta que otorga puntos al completarse."""

    __tablename__ = 'misiones'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    titulo: Mapped[str] = mapped_column(String(120), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, default='')
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    meta: Mapped[int] = mapped_column(Integer, default=1)
    puntos: Mapped[int] = mapped_column(Integer, default=0)
    monedas: Mapped[int] = mapped_column(Integer, default=0)
    solo_plus: Mapped[bool] = mapped_column(Boolean, default=False)


class MisionUsuario(Base):
    __tablename__ = 'misiones_usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    mision_id: Mapped[int] = mapped_column(ForeignKey('misiones.id'), nullable=False)
    progreso: Mapped[int] = mapped_column(Integer, default=0)
    completada: Mapped[bool] = mapped_column(Boolean, default=False)
    fecha_completada: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Leccion(Base):
    """Microaprendizaje: explicación breve + ejemplo resuelto por tema."""

    __tablename__ = 'lecciones'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grado: Mapped[str] = mapped_column(String(10), nullable=False)
    tema: Mapped[str] = mapped_column(String(80), nullable=False)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    subtitulo: Mapped[str] = mapped_column(String(200), default='')
    explicacion: Mapped[str] = mapped_column(Text, nullable=False)
    ejemplo: Mapped[str] = mapped_column(Text, default='')
    puntos: Mapped[int] = mapped_column(Integer, default=20)
    orden: Mapped[int] = mapped_column(Integer, default=1)


class ActividadInteractiva(Base):
    """Actividad de refuerzo basada en clics (clasificar, seleccionar, emparejar)."""

    __tablename__ = 'actividades_interactivas'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    grado: Mapped[str] = mapped_column(String(10), nullable=False)
    tema: Mapped[str] = mapped_column(String(80), nullable=False)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    instrucciones: Mapped[str] = mapped_column(Text, default='')
    tipo: Mapped[str] = mapped_column(String(30), default='clasificar')
    datos: Mapped[str] = mapped_column(Text, default='{}')
    puntos: Mapped[int] = mapped_column(Integer, default=15)
    solo_plus: Mapped[bool] = mapped_column(Boolean, default=False)


class LeccionUsuario(Base):
    """Registro de las lecciones que un estudiante ya completó."""

    __tablename__ = 'lecciones_usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    leccion_id: Mapped[int] = mapped_column(ForeignKey('lecciones.id'), nullable=False)
    fecha_completada: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class ActividadUsuario(Base):
    """Registro de los intentos del estudiante en actividades interactivas."""

    __tablename__ = 'actividades_usuario'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    actividad_id: Mapped[int] = mapped_column(ForeignKey('actividades_interactivas.id'), nullable=False)
    correcta: Mapped[bool] = mapped_column(Boolean, default=False)
    puntaje: Mapped[int] = mapped_column(Integer, default=0)
    fecha_intento: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
