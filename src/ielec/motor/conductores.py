"""Selección y verificación de conductores eléctricos según NTC 2050."""

from typing import Optional
from ..normativa.consultas import (
    obtener_ampacidad_cobre,
    obtener_proteccion_maxima_240_4d,
)

CALIBRES_AWG_ORDENADOS = ["14", "12", "10", "8", "6", "4", "2"]


def seleccionar_calibre_cobre_ramal(
    corriente_nominal_circuito_a: int,
    temperatura_terminales_c: int = 75,
) -> str:
    """Selecciona el calibre mínimo de Cu para circuito ramal respetando NTC 2050 240.4(D).
    
    15 A -> 14 AWG
    20 A -> 12 AWG
    30 A -> 10 AWG
    """
    for calibre in CALIBRES_AWG_ORDENADOS:
        ampacidad = obtener_ampacidad_cobre(calibre, temperatura_terminales_c)
        limite_240_4d = obtener_proteccion_maxima_240_4d(calibre)
        
        capacidad_efectiva = (
            min(ampacidad, limite_240_4d) if limite_240_4d is not None else ampacidad
        )
        
        if capacidad_efectiva >= corriente_nominal_circuito_a:
            return calibre
            
    return "2"


def seleccionar_calibre_acometida(
    corriente_diseno_a: float,
    temperatura_terminales_c: int = 60,
    capacidad_proteccion_a: Optional[int] = None,
) -> str:
    """Selecciona el calibre mínimo de Cu para la acometida.
    
    Conforme a NTC 2050 Art. 110.14(C)(1)(a), las terminaciones de equipos para
    circuitos de 100 A o menos se basan en la columna de 60 °C de la Tabla 310.15(B)(16).
    Asimismo, la ampacidad debe coordinar con la protección asignada (Art. 230.42 / 240.4).
    """
    corriente_objetivo = max(corriente_diseno_a, float(capacidad_proteccion_a or 0))
    for calibre in CALIBRES_AWG_ORDENADOS:
        ampacidad = obtener_ampacidad_cobre(calibre, temperatura_terminales_c)
        if ampacidad >= corriente_objetivo:
            return calibre
    return "2"
