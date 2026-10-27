"""Validador normativo de diseño eléctrico según NTC 2050, RETIE y RETILAP."""

from typing import List
from ..modelo.entidades import (
    DisenoElectrico,
    HallazgoValidacion,
    TipoCircuito,
    TipoProteccion,
)


def validar_diseno_electrico(diseno: DisenoElectrico) -> List[HallazgoValidacion]:
    """Ejecuta las validaciones normativas de la V1 sobre el diseño eléctrico."""
    hallazgos: List[HallazgoValidacion] = []
    
    # 1. Mínimo 2 circuitos de pequeños artefactos
    circuitos_pa = [c for c in diseno.circuitos if c.tipo == TipoCircuito.PEQUENOS_ARTEFACTOS]
    if len(circuitos_pa) < 2:
        hallazgos.append(
            HallazgoValidacion(
                regla_id="NTC_210_11_C1",
                articulo_norma="NTC 2050 Art. 210.11(C)(1)",
                severidad="ERROR",
                mensaje="Se requieren como mínimo dos circuitos ramales de 20 A para pequeños artefactos en cocina/comedor.",
            )
        )
        
    # 2. Circuito exclusivo de baño de 20 A
    circuitos_bano = [c for c in diseno.circuitos if c.tipo == TipoCircuito.BANO]
    if not circuitos_bano:
        hallazgos.append(
            HallazgoValidacion(
                regla_id="NTC_210_11_C3",
                articulo_norma="NTC 2050 Art. 210.11(C)(3)",
                severidad="ERROR",
                mensaje="Se debe suministrar al menos un circuito ramal de 20 A exclusivo para tomacorrientes de cuartos de baño.",
            )
        )
        
    # 3. Verificación de protecciones GFCI en zonas húmedas
    for c in diseno.circuitos:
        if c.tipo in [TipoCircuito.BANO, TipoCircuito.PEQUENOS_ARTEFACTOS, TipoCircuito.LAVANDERIA]:
            if c.tipo_proteccion not in [TipoProteccion.GFCI, TipoProteccion.AFCI_GFCI]:
                hallazgos.append(
                    HallazgoValidacion(
                        regla_id="NTC_210_8_GFCI",
                        articulo_norma="NTC 2050 Art. 210.8",
                        severidad="ERROR",
                        mensaje=f"El circuito {c.codigo} ({c.descripcion}) requiere protección con interruptor de circuito por falla a tierra (GFCI).",
                    )
                )
                
    # 4. Verificación de protecciones AFCI en áreas habitables
    for c in diseno.circuitos:
        if c.tipo == TipoCircuito.ALUMBRADO_Y_TOMAS_GENERALES:
            if c.tipo_proteccion not in [TipoProteccion.AFCI, TipoProteccion.AFCI_GFCI]:
                hallazgos.append(
                    HallazgoValidacion(
                        regla_id="NTC_210_12_AFCI",
                        articulo_norma="NTC 2050 Art. 210.12",
                        severidad="ADVERTENCIA",
                        mensaje=f"El circuito {c.codigo} de alumbrado y tomas generales debe incorporar protección contra falla por arco (AFCI) en unidades de vivienda.",
                    )
                )
                
    # 5. Regulación de tensión en alimentador
    if not diseno.acometida.cumple_regulacion:
        hallazgos.append(
            HallazgoValidacion(
                regla_id="NTC_210_19_REGULACION",
                articulo_norma="NTC 2050 Art. 210.19(A) Nota Informativa",
                severidad="ERROR",
                mensaje=f"La caída de tensión en el alimentador ({diseno.acometida.porcentaje_regulacion}%) supera el límite máximo permitido del 3%.",
            )
        )
        
    # 6. Medidor de energía
    if not diseno.medidor.cumple:
        hallazgos.append(
            HallazgoValidacion(
                regla_id="RETIE_MEDIDOR",
                articulo_norma="RETIE / Normas del Operador de Red",
                severidad="ERROR",
                mensaje=f"La corriente nominal del medidor ({diseno.medidor.corriente_nominal_a} A) es menor a la corriente de demanda ({diseno.medidor.corriente_demanda_a} A).",
            )
        )
        
    return hallazgos
