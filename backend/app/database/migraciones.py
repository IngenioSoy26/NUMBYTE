"""Migraciones ligeras para agregar columnas sin borrar datos.

`Base.metadata.create_all` crea las tablas nuevas, pero no agrega columnas a
tablas que ya existían. Como el prototipo evoluciona por fases, aquí añadimos
las columnas faltantes de forma segura.

Las definiciones usan SQL válido tanto en SQLite como en PostgreSQL:

- `BOOLEAN DEFAULT FALSE` funciona en PostgreSQL y en SQLite 3.23+.
- `TIMESTAMP` es equivalente a `DATETIME` y es aceptado por ambos motores.
"""

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

# columnas_nuevas: tabla -> lista de (nombre_columna, definición SQL)
COLUMNAS_NUEVAS: dict[str, list[tuple[str, str]]] = {
    'usuarios': [
        ('plan', "VARCHAR(20) DEFAULT 'gratis'"),
        ('fecha_activacion_plan', 'TIMESTAMP'),
    ],
    'recursos_multimedia': [
        ('grado', "VARCHAR(10) DEFAULT '6'"),
        ('autor', "VARCHAR(150) DEFAULT ''"),
        ('solo_plus', 'BOOLEAN DEFAULT FALSE'),
    ],
}


def aplicar_migraciones_ligeras(motor: Engine):
    inspector = inspect(motor)
    tablas_existentes = set(inspector.get_table_names())

    with motor.begin() as conexion:
        for tabla, columnas in COLUMNAS_NUEVAS.items():
            if tabla not in tablas_existentes:
                continue
            actuales = {columna['name'] for columna in inspector.get_columns(tabla)}
            for nombre, definicion in columnas:
                if nombre in actuales:
                    continue
                conexion.execute(text(f'ALTER TABLE {tabla} ADD COLUMN {nombre} {definicion}'))
