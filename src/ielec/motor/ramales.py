"""Cálculo y dimensionamiento de circuitos ramales según NTC 2050."""

import math
from typing import List, Optional
from ..modelo.entidades import CircuitoRamal, TipoCircuito, TipoProteccion, TipoEspacio, Espacio
from .conductores import seleccionar_calibre_cobre_ramal
from .protecciones import determinar_tipo_proteccion


def dimensionar_circuitos_ramales(
    carga_alumbrado_general_va: float,
    tension_v: float = 120.0,
    espacios: Optional[List[Espacio]] = None,
    incluir_circuito_bano_20a: bool = True,
    incluir_circuito_lavanderia_20a: bool = False,
) -> List[CircuitoRamal]:
    """Genera la lista de circuitos ramales mínimos para la vivienda unifamiliar.
    
    1. Circuitos de alumbrado general (15 A, 120 V, 14 AWG Cu).
       Cantidad minima = ceil(carga_alumbrado / (V * 15 A)) = ceil(carga / 1800 VA).
    2. Minimo 2 circuitos de pequenos artefactos (20 A, 120 V, 12 AWG Cu).
    3. Circuito de bano exclusivo (20 A, 120 V, 12 AWG Cu, GFCI, NTC 2050 210.11(C)(3)).
    4. Circuito de lavanderia (20 A, 120 V, 12 AWG Cu, GFCI) si aplica.
    """
    circuitos: List[CircuitoRamal] = []
    num_circuito = 1
    
    # 1. Alumbrado general
    capacidad_circuito_15a_va = tension_v * 15.0  # 1800 VA
    num_circuitos_alumbrado = max(1, math.ceil(carga_alumbrado_general_va / capacidad_circuito_15a_va))
    
    va_por_circuito_alumbrado = round(carga_alumbrado_general_va / num_circuitos_alumbrado, 2)
    calibre_15a = seleccionar_calibre_cobre_ramal(15)
    
    for i in range(num_circuitos_alumbrado):
        tipo_prot = TipoProteccion.AFCI  # Alumbrado y tomas generales residenciales
        circuitos.append(
            CircuitoRamal(
                numero=num_circuito,
                codigo=f"C{num_circuito}",
                descripcion=f"Alumbrado y tomas generales {i+1}",
                tipo=TipoCircuito.ALUMBRADO_Y_TOMAS_GENERALES,
                tension_v=tension_v,
                corriente_nominal_a=15,
                potencia_va=va_por_circuito_alumbrado,
                corriente_diseno_a=round(va_por_circuito_alumbrado / tension_v, 2),
                calibre_fase_awg=calibre_15a,
                calibre_neutro_awg=calibre_15a,
                calibre_tierra_awg=calibre_15a,
                tipo_proteccion=tipo_prot,
                requiere_tr=True,
                espacios_atendidos=[],
            )
        )
        num_circuito += 1
        
    # 2. Pequeños artefactos (mínimo 2 circuitos de 20 A)
    calibre_20a = seleccionar_calibre_cobre_ramal(20)
    for i in range(2):
        circuitos.append(
            CircuitoRamal(
                numero=num_circuito,
                codigo=f"C{num_circuito}",
                descripcion=f"Pequeños artefactos cocina/comedor {i+1}",
                tipo=TipoCircuito.PEQUENOS_ARTEFACTOS,
                tension_v=tension_v,
                corriente_nominal_a=20,
                potencia_va=1500.0,
                corriente_diseno_a=round(1500.0 / tension_v, 2),
                calibre_fase_awg=calibre_20a,
                calibre_neutro_awg=calibre_20a,
                calibre_tierra_awg=calibre_20a,
                tipo_proteccion=TipoProteccion.GFCI,
                requiere_tr=True,
                espacios_atendidos=["cocina", "comedor"],
            )
        )
        num_circuito += 1
        
    # 3. Circuito de lavandería si aplica
    if incluir_circuito_lavanderia_20a:
        circuitos.append(
            CircuitoRamal(
                numero=num_circuito,
                codigo=f"C{num_circuito}",
                descripcion="Lavandería y zona de ropas",
                tipo=TipoCircuito.LAVANDERIA,
                tension_v=tension_v,
                corriente_nominal_a=20,
                potencia_va=1500.0,
                corriente_diseno_a=round(1500.0 / tension_v, 2),
                calibre_fase_awg=calibre_20a,
                calibre_neutro_awg=calibre_20a,
                calibre_tierra_awg=calibre_20a,
                tipo_proteccion=TipoProteccion.GFCI,
                requiere_tr=True,
                espacios_atendidos=["zona_ropas"],
            )
        )
        num_circuito += 1
        
    # 4. Circuito de baño (NTC 2050 210.11(C)(3))
    if incluir_circuito_bano_20a:
        circuitos.append(
            CircuitoRamal(
                numero=num_circuito,
                codigo=f"C{num_circuito}",
                descripcion="Tomacorrientes cuarto de baño",
                tipo=TipoCircuito.BANO,
                tension_v=tension_v,
                corriente_nominal_a=20,
                potencia_va=0.0,  # Conforme a 220.52 no suma potencia de demanda en acometida
                corriente_diseno_a=round(0.0 / tension_v, 2),
                calibre_fase_awg=calibre_20a,
                calibre_neutro_awg=calibre_20a,
                calibre_tierra_awg=calibre_20a,
                tipo_proteccion=TipoProteccion.GFCI,
                requiere_tr=True,
                espacios_atendidos=["bano"],
            )
        )
        num_circuito += 1
        
    return circuitos
