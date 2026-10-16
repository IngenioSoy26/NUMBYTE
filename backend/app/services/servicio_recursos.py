"""Servicio de recursos multimedia (videos y material complementario).

Los recursos apuntan a contenido externo (YouTube). No se descarga ni
redistribuye material protegido: solo se muestra el enlace y se atribuye al
autor. Los recursos marcados como 'solo_plus' se muestran bloqueados para los
usuarios del plan Gratis.
"""

import re

from sqlalchemy.orm import Session

from app.models.modelos import RecursoMultimedia, Usuario


class ServicioRecursos:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, usuario: Usuario, grado: str | None = None) -> list[dict]:
        consulta = self.db.query(RecursoMultimedia)
        if grado:
            consulta = consulta.filter(RecursoMultimedia.grado == grado)
        recursos = consulta.order_by(RecursoMultimedia.tema).all()
        return [self._serializar(recurso, usuario) for recurso in recursos]

    def listar_por_tema(self, usuario: Usuario, tema: str, grado: str | None = None) -> dict | None:
        consulta = self.db.query(RecursoMultimedia).filter(RecursoMultimedia.tema == tema)
        if grado:
            consulta = consulta.filter(RecursoMultimedia.grado == grado)
        recurso = consulta.first()
        return self._serializar(recurso, usuario) if recurso else None

    @staticmethod
    def _serializar(recurso: RecursoMultimedia, usuario: Usuario) -> dict:
        bloqueado = recurso.solo_plus and not usuario.es_plus
        return {
            'id': recurso.id,
            'titulo': recurso.titulo,
            'url': recurso.url,
            'tipo': recurso.tipo,
            'tema': recurso.tema,
            'grado': recurso.grado,
            'autor': recurso.autor,
            'descripcion': recurso.descripcion,
            'solo_plus': recurso.solo_plus,
            'bloqueado': bloqueado,
            'url_embed': None if bloqueado else extraer_url_embed(recurso.url),
        }


def extraer_url_embed(url: str) -> str | None:
    """Convierte un enlace de YouTube con video específico en URL embebible.

    Devuelve None cuando el enlace no contiene un video concreto (por ejemplo,
    enlaces de búsqueda), ya que esos no se pueden incrustar en un iframe.
    """
    if not url:
        return None

    patrones = [
        r'youtube\.com/watch\?v=([A-Za-z0-9_-]{6,})',
        r'youtube\.com/embed/([A-Za-z0-9_-]{6,})',
        r'youtu\.be/([A-Za-z0-9_-]{6,})',
    ]
    for patron in patrones:
        coincidencia = re.search(patron, url)
        if coincidencia:
            return f'https://www.youtube.com/embed/{coincidencia.group(1)}'
    return None
