"""Orquestador del motor de diseño eléctrico residencial (Módulo 1)."""

from typing import List, Optional
from ..modelo.entidades import (
    DisenoElectrico,
    Espacio,
    TipoSistemaElectrico,
)
from .iluminacion import calcular_iluminacion_vivienda
from .cargas import calcular_cargas_y_demanda
from .ramales import dimensionar_circuitos_ramales
from .acometida import calcular_acometida
from .medidor import verificar_medidor_monofasico
from .validador import validar_diseno_electrico


def disenar_instalacion_electrica(
    nombre_proyecto: str,
    area_construida_m2: float,
    espacios: Optional[List[Espacio]] = None,
    longitud_acometida_m: float = 15.0,
    impedancia_acometida_ohm_km: Optional[float] = 2.4,
    tension_v: float = 120.0,
    sistema: TipoSistemaElectrico = TipoSistemaElectrico.MONOFASICO_120,
    incluir_circuito_bano_20a: bool = True,
    num_circuitos_pequenos_artefactos: int = 2,
    num_circuitos_lavanderia: int = 0,
) -> DisenoElectrico:
    """Ejecuta el diseño eléctrico completo según NTC 2050 2ª ed., RETIE y RETILAP."""
    if sistema != TipoSistemaElectrico.MONOFASICO_120:
        raise NotImplementedError(
            f"El sistema eléctrico '{sistema.value}' no está soportado en la V1. "
            "Consulte docs/trabajo_futuro.md para ver soporte en futuras versiones."
        )
        
    espacios_lista = espacios or []
    
    # 1. Cálculo de iluminación según RETILAP
    calculo_iluminacion = calcular_iluminacion_vivienda(espacios_lista)
    
    # 2. Carga general y demanda según NTC 2050
    (
        carga_alumbrado,
        carga_pa,
        carga_lav,
        carga_total,
        carga_demanda,
    ) = calcular_cargas_y_demanda(
        area_construida_m2=area_construida_m2,
        num_circuitos_pequenos_artefactos=num_circuitos_pequenos_artefactos,
        num_circuitos_lavanderia=num_circuitos_lavanderia,
    )
    
    # 3. Circuitos ramales
    circuitos = dimensionar_circuitos_ramales(
        carga_alumbrado_general_va=carga_alumbrado,
        tension_v=tension_v,
        espacios=espacios_lista,
        incluir_circuito_bano_20a=incluir_circuito_bano_20a,
        incluir_circuito_lavanderia_20a=(num_circuitos_lavanderia > 0),
    )
    
    # 4. Acometida y regulación
    acometida = calcular_acometida(
        potencia_total_instalada_va=carga_total,
        potencia_demanda_va=carga_demanda,
        tension_v=tension_v,
        longitud_m=longitud_acometida_m,
        impedancia_z_ohm_km=impedancia_acometida_ohm_km,
    )
    
    # 5. Medidor
    medidor = verificar_medidor_monofasico(
        corriente_demanda_a=acometida.corriente_demanda_a,
    )
    
    # Construcción de diseño
    diseno = DisenoElectrico(
        nombre_proyecto=nombre_proyecto,
        area_construida_m2=area_construida_m2,
        sistema=sistema,
        carga_alumbrado_general_va=carga_alumbrado,
        carga_pequenos_artefactos_va=carga_pa,
        carga_lavanderia_va=carga_lav,
        carga_total_instalada_va=carga_total,
        carga_demanda_va=carga_demanda,
        circuitos=circuitos,
        iluminacion=calculo_iluminacion,
        acometida=acometida,
        medidor=medidor,
        hallazgos=[],
    )
    
    # 6. Validación normativa
    diseno.hallazgos = validar_diseno_electrico(diseno)
    
    return diseno
