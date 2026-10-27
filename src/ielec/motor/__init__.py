"""Módulo del motor de diseño eléctrico (Módulo 1)."""

from .disenador import disenar_instalacion_electrica
from .cargas import calcular_carga_alumbrado_general, calcular_cargas_y_demanda
from .ramales import dimensionar_circuitos_ramales
from .acometida import calcular_acometida
from .iluminacion import calcular_iluminacion_espacio, calcular_iluminacion_vivienda
from .tierra import dimensionar_puesta_a_tierra
from .medidor import verificar_medidor_monofasico
from .validador import validar_diseno_electrico

__all__ = [
    "disenar_instalacion_electrica",
    "calcular_carga_alumbrado_general",
    "calcular_cargas_y_demanda",
    "dimensionar_circuitos_ramales",
    "calcular_acometida",
    "calcular_iluminacion_espacio",
    "calcular_iluminacion_vivienda",
    "dimensionar_puesta_a_tierra",
    "verificar_medidor_monofasico",
    "validar_diseno_electrico",
]
