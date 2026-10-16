from fastapi import APIRouter

router = APIRouter(tags=['Salud'])


@router.get('/salud')
def verificar_salud():
    return {'estado': 'ok', 'mensaje': 'NUMBYTE API está funcionando correctamente.'}
