"""Selección y asignación de dispositivos de protección según NTC 2050."""

from typing import List
from ..modelo.entidades import TipoProteccion, TipoCircuito, TipoEspacio

PROTECCIONES_NORMALIZADAS_A = [15, 20, 30, 40, 50, 60, 70, 80, 100]


def seleccionar_breaker_comercial(corriente_diseno_a: float) -> int:
    """Selecciona la capacidad nominal normalizada inmediatamente superior o igual."""
    for capacidad in PROTECCIONES_NORMALIZADAS_A:
        if capacidad >= corriente_diseno_a:
            return capacidad
    return 100


def determinar_tipo_proteccion(
    tipo_circuito: TipoCircuito,
    tipos_espacio_atendidos: List[TipoEspacio],
) -> TipoProteccion:
    """Determina si un circuito ramal requiere AFCI, GFCI o termomagnético estándar.
    
    Reglas NTC 2050:
    - 210.12 (AFCI): obligatorio en dormitorios, salas, comedores, pasillos, etc.
    - 210.8 (GFCI): obligatorio en baños, mesones de cocina, lavandería, exteriores.
    """
    if tipo_circuito == TipoCircuito.BANO:
        return TipoProteccion.GFCI
    elif tipo_circuito == TipoCircuito.PEQUENOS_ARTEFACTOS:
        # Cocina requiere GFCI en mesones
        return TipoProteccion.GFCI
    elif tipo_circuito == TipoCircuito.LAVANDERIA:
        return TipoProteccion.GFCI
    
    # Para circuitos de alumbrado y tomas generales:
    tiene_dormitorio_o_sala = any(
        esp in [
            TipoEspacio.DORMITORIO_PRINCIPAL,
            TipoEspacio.DORMITORIO_SECUNDARIO,
            TipoEspacio.SALA,
            TipoEspacio.COMEDOR,
        ]
        for esp in tipos_espacio_atendidos
    )
    tiene_humedo = any(
        esp in [
            TipoEspacio.BANO,
            TipoEspacio.COCINA,
            TipoEspacio.ZONA_ROPAS,
            TipoEspacio.EXTERIOR,
        ]
        for esp in tipos_espacio_atendidos
    )
    
    if tiene_dormitorio_o_sala and tiene_humedo:
        return TipoProteccion.AFCI_GFCI
    elif tiene_dormitorio_o_sala:
        return TipoProteccion.AFCI
    elif tiene_humedo:
        return TipoProteccion.GFCI
        
    return TipoProteccion.TERMOMAGNETICO_ESTANDAR
