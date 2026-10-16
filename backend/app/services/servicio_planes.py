"""Servicio de planes (Gratis y Plus).

IMPORTANTE (demostrativo): el plan Plus es una simulación académica. No existe
pasarela de pago, cobro real ni suscripción. El botón "Mejorar a Plus" solo
cambia el estado del usuario en la base de datos local para demostrar el
desbloqueo de funcionalidades.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.modelos import PLAN_GRATIS, PLAN_PLUS, Usuario

# Los usuarios del plan Gratis pueden hacer 1 simulacro por día.
LIMITE_SIMULACROS_GRATIS = 1

BENEFICIOS = [
    {
        'titulo': 'Diagnóstico y práctica ilimitados',
        'descripcion': 'Prueba diagnóstica y práctica por temas sin restricción.',
        'solo_plus': False,
    },
    {
        'titulo': 'Ruta de aprendizaje de 6°',
        'descripcion': 'Lecciones con explicación, ejemplo resuelto y actividades de clic.',
        'solo_plus': False,
    },
    {
        'titulo': '1 simulacro de práctica al día',
        'descripcion': 'Un simulacro completo diario con retroalimentación pedagógica.',
        'solo_plus': False,
    },
    {
        'titulo': 'Analítica avanzada',
        'descripcion': 'Panel detallado con evolución, fortalezas y debilidades por tema.',
        'solo_plus': True,
    },
    {
        'titulo': 'Insignias y misiones exclusivas',
        'descripcion': 'Logros y retos desbloqueados solo con el plan Plus.',
        'solo_plus': True,
    },
    {
        'titulo': 'Todos los videos y recursos',
        'descripcion': 'Acceso a la biblioteca completa de recursos audiovisuales.',
        'solo_plus': True,
    },
    {
        'titulo': 'Simulacros ilimitados',
        'descripcion': 'Practica simulacros completos sin límite diario.',
        'solo_plus': True,
    },
]


class ServicioPlanes:
    def __init__(self, db: Session):
        self.db = db

    def obtener_plan(self, usuario: Usuario) -> dict:
        return {
            'plan': usuario.plan,
            'es_plus': usuario.es_plus,
            'fecha_activacion_plan': (
                usuario.fecha_activacion_plan.isoformat() if usuario.fecha_activacion_plan else None
            ),
            'beneficios': BENEFICIOS,
        }

    def activar_plus(self, usuario: Usuario) -> dict:
        if usuario.plan != PLAN_PLUS:
            usuario.plan = PLAN_PLUS
            usuario.fecha_activacion_plan = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(usuario)
        return self.obtener_plan(usuario)

    def volver_a_gratis(self, usuario: Usuario) -> dict:
        usuario.plan = PLAN_GRATIS
        usuario.fecha_activacion_plan = None
        self.db.commit()
        self.db.refresh(usuario)
        return self.obtener_plan(usuario)
