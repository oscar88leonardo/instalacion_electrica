"""Cálculo de iluminación según método de cavidad zonal / lúmenes y RETILAP."""

import math
from typing import List
from ..modelo.entidades import Espacio, CalculoIluminacionEspacio
from ..normativa.consultas import obtener_lux_retilap


def calcular_iluminacion_espacio(
    espacio: Espacio,
    flujo_luminoso_lumen: float = 800.0,
    coeficiente_utilizacion: float = 0.55,
    factor_mantenimiento: float = 0.80,
) -> CalculoIluminacionEspacio:
    """Calcula el número de luminarias necesarias para un espacio según RETILAP.
    
    Fórmula: N = (E * A) / (F * CU * MF)
    """
    lux_requerido = obtener_lux_retilap(espacio.tipo.value)
    
    denominador = flujo_luminoso_lumen * coeficiente_utilizacion * factor_mantenimiento
    if denominador <= 0:
        raise ValueError("Los factores de flujo, CU y MF deben ser mayores que cero.")
    
    n_calculado = (lux_requerido * espacio.area_m2) / denominador
    
    # Adopción de cantidad: al menos 1 por espacio habitable
    # Para áreas de dormitorio/estar suele adoptarse 1 o más según distribución funcional
    n_adoptado = max(1, math.ceil(n_calculado)) if n_calculado > 1.3 else max(1, round(n_calculado))
    
    return CalculoIluminacionEspacio(
        espacio_id=espacio.id,
        nombre_espacio=espacio.nombre,
        tipo_espacio=espacio.tipo,
        area_m2=espacio.area_m2,
        lux_requerido=lux_requerido,
        flujo_luminoso_lumen=flujo_luminoso_lumen,
        coeficiente_utilizacion=coeficiente_utilizacion,
        factor_mantenimiento=factor_mantenimiento,
        luminarias_calculadas=round(n_calculado, 2),
        luminarias_adoptadas=n_adoptado,
    )


def calcular_iluminacion_vivienda(
    espacios: List[Espacio],
    flujo_luminoso_lumen: float = 800.0,
    coeficiente_utilizacion: float = 0.55,
    factor_mantenimiento: float = 0.80,
) -> List[CalculoIluminacionEspacio]:
    """Calcula la iluminación para todos los espacios de la vivienda."""
    return [
        calcular_iluminacion_espacio(
            espacio=esp,
            flujo_luminoso_lumen=flujo_luminoso_lumen,
            coeficiente_utilizacion=coeficiente_utilizacion,
            factor_mantenimiento=factor_mantenimiento,
        )
        for esp in espacios
    ]
