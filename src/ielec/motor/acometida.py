"""Dimensionamiento de acometida y cálculo de regulación (caída de tensión)."""

from typing import Optional
from ..modelo.entidades import Acometida, TipoSistemaElectrico
from ..normativa.consultas import (
    obtener_impedancia_referencia_ohm_km,
    obtener_calibre_minimo_tierra_equipos,
    obtener_calibre_minimo_electrodo_tierra,
)
from .conductores import seleccionar_calibre_acometida
from .protecciones import seleccionar_breaker_comercial


def calcular_acometida(
    potencia_total_instalada_va: float,
    potencia_demanda_va: float,
    tension_v: float = 120.0,
    longitud_m: float = 15.0,
    impedancia_z_ohm_km: Optional[float] = None,
    calibre_forzado_awg: Optional[str] = None,
    limite_regulacion_porc: float = 3.0,
) -> Acometida:
    """Calcula y verifica el alimentador / acometida de la vivienda unifamiliar.
    
    1. Corriente de demanda: I = S_demanda / V
    2. Capacidad de proteccion: breaker comercial (ej. 40 A para 33.3 A)
    3. Calibre: conductor de Cu (ej. 8 AWG)
    4. Caida de tension monofasica: DeltaV = 2 * Z * (L/1000) * I
    5. % Regulacion: (DeltaV / V) * 100 <= 3%
    """
    if tension_v <= 0:
        raise ValueError("La tensión debe ser mayor a cero.")
    if longitud_m <= 0:
        raise ValueError("La longitud del alimentador debe ser mayor a cero.")
        
    corriente_demanda_a = round(potencia_demanda_va / tension_v, 2)
    
    # Capacidad del breaker comercial
    capacidad_proteccion = seleccionar_breaker_comercial(corriente_demanda_a)
    
    # Selección de calibre
    calibre_seleccionado = calibre_forzado_awg or seleccionar_calibre_acometida(
        corriente_diseno_a=corriente_demanda_a,
        capacidad_proteccion_a=capacidad_proteccion,
    )
    
    # Impedancia eficaz Z (ohm/km)
    if impedancia_z_ohm_km is not None:
        z = impedancia_z_ohm_km
    else:
        z = obtener_impedancia_referencia_ohm_km(calibre_seleccionado)
        
    # Caída de tensión monofásica a dos hilos (Fase + Neutro): DeltaV = 2 * Z * L(km) * I
    distancia_km = longitud_m / 1000.0
    caida_tension_v = round(2.0 * z * distancia_km * corriente_demanda_a, 2)
    porcentaje_reg = round((caida_tension_v / tension_v) * 100.0, 2)
    cumple_reg = porcentaje_reg <= limite_regulacion_porc
    
    # Conductores de tierra
    tierra_equipos = obtener_calibre_minimo_tierra_equipos(capacidad_proteccion)
    electrodo_tierra = obtener_calibre_minimo_electrodo_tierra(calibre_seleccionado)
    
    return Acometida(
        sistema=TipoSistemaElectrico.MONOFASICO_120,
        tension_v=tension_v,
        potencia_total_instalada_va=round(potencia_total_instalada_va, 2),
        potencia_demanda_va=round(potencia_demanda_va, 2),
        corriente_demanda_a=corriente_demanda_a,
        capacidad_proteccion_a=capacidad_proteccion,
        calibre_fase_awg=calibre_seleccionado,
        calibre_neutro_awg=calibre_seleccionado,
        calibre_tierra_equipos_awg=tierra_equipos,
        calibre_electrodo_tierra_awg=electrodo_tierra,
        longitud_m=longitud_m,
        impedancia_z_ohm_km=z,
        caida_tension_v=caida_tension_v,
        porcentaje_regulacion=porcentaje_reg,
        cumple_regulacion=cumple_reg,
    )
