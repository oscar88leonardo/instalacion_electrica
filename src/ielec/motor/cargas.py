"""Cálculo de cargas eléctricas y demanda según NTC 2050 Art. 220."""

from typing import Tuple
from ..normativa.consultas import (
    obtener_carga_unitaria_vivienda,
    calcular_demanda_alumbrado_general,
)


def calcular_carga_alumbrado_general(area_construida_m2: float) -> float:
    """Calcula la carga unitaria de alumbrado general según NTC 2050 220.12."""
    if area_construida_m2 <= 0:
        raise ValueError("El área construida debe ser mayor a cero.")
    densidad = obtener_carga_unitaria_vivienda()
    return round(area_construida_m2 * densidad, 2)


def calcular_cargas_y_demanda(
    area_construida_m2: float,
    num_circuitos_pequenos_artefactos: int = 2,
    num_circuitos_lavanderia: int = 0,
) -> Tuple[float, float, float, float, float]:
    """Calcula las cargas instaladas y la carga de demanda residencial."""
    carga_alumbrado = calcular_carga_alumbrado_general(area_construida_m2)
    carga_pequenos_artefactos = num_circuitos_pequenos_artefactos * 1500.0
    carga_lavanderia = num_circuitos_lavanderia * 1500.0
    
    carga_total_instalada = (
        carga_alumbrado + carga_pequenos_artefactos + carga_lavanderia
    )
    
    carga_demanda = calcular_demanda_alumbrado_general(carga_total_instalada)
    
    return (
        round(carga_alumbrado, 2),
        round(carga_pequenos_artefactos, 2),
        round(carga_lavanderia, 2),
        round(carga_total_instalada, 2),
        round(carga_demanda, 2),
    )
