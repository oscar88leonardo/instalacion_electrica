"""Cálculo y especificación del sistema de puesta a tierra (SPT)."""

from typing import Dict
from ..normativa.consultas import (
    obtener_calibre_minimo_tierra_equipos,
    obtener_calibre_minimo_electrodo_tierra,
)


def dimensionar_puesta_a_tierra(
    capacidad_proteccion_acometida_a: int,
    calibre_fase_acometida_awg: str,
) -> Dict[str, str]:
    """Determina los calibres mínimos de tierra de equipos y electrodo de puesta a tierra.
    
    - Tierra de equipos: NTC 2050 Tabla 250.122
    - Electrodo de tierra: NTC 2050 Tabla 250.66
    - Electrodo: Varilla de acero recubierta de cobre (Copperweld) >= 2.4 m y diametro >= 12.7 mm
    - Resistencia de puesta a tierra maxima: 25 ohm (RETIE Libro 3 Art. 15 / NTC 2050 250.56)
    """
    calibre_tierra_equipos = obtener_calibre_minimo_tierra_equipos(capacidad_proteccion_acometida_a)
    calibre_electrodo = obtener_calibre_minimo_electrodo_tierra(calibre_fase_acometida_awg)
    
    return {
        "conductor_tierra_equipos_awg": calibre_tierra_equipos,
        "conductor_electrodo_tierra_awg": calibre_electrodo,
        "electrodo_tipo": "Varilla de puesta a tierra de acero recubierta de cobre (Copperweld)",
        "electrodo_longitud_min_m": "2.40 m",
        "electrodo_diametro_min_mm": "12.7 mm (1/2 pulgada)",
        "resistencia_maxima_referencia_ohm": "25.0 ohm",
    }
