"""Pruebas unitarias para consultas y carga de tablas normativas YAML."""

from ielec.normativa.consultas import (
    obtener_carga_unitaria_vivienda,
    calcular_demanda_alumbrado_general,
    obtener_ampacidad_cobre,
    obtener_proteccion_maxima_240_4d,
    obtener_calibre_minimo_tierra_equipos,
    obtener_calibre_minimo_electrodo_tierra,
    obtener_impedancia_referencia_ohm_km,
    obtener_lux_retilap,
)


def test_carga_unitaria_vivienda():
    densidad = obtener_carga_unitaria_vivienda()
    assert densidad == 33.0


def test_factores_demanda_ntc_220_42():
    assert calcular_demanda_alumbrado_general(2500) == 2500.0
    assert calcular_demanda_alumbrado_general(3000) == 3000.0
    assert round(calcular_demanda_alumbrado_general(5838), 1) == 3993.3


def test_ampacidad_cobre_y_limite_240_4d():
    assert obtener_ampacidad_cobre("14", 75) == 20
    assert obtener_proteccion_maxima_240_4d("14") == 15
    
    assert obtener_ampacidad_cobre("12", 75) == 25
    assert obtener_proteccion_maxima_240_4d("12") == 20
    
    assert obtener_ampacidad_cobre("8", 75) == 50
    assert obtener_proteccion_maxima_240_4d("8") is None


def test_tierra_equipos_250_122():
    assert obtener_calibre_minimo_tierra_equipos(15) == "14"
    assert obtener_calibre_minimo_tierra_equipos(20) == "12"
    assert obtener_calibre_minimo_tierra_equipos(40) == "10"


def test_electrodo_tierra_250_66():
    assert obtener_calibre_minimo_electrodo_tierra("8") == "8"


def test_impedancia_referencia_8awg():
    z = obtener_impedancia_referencia_ohm_km("8")
    assert z == 2.4


def test_lux_retilap():
    assert obtener_lux_retilap("dormitorio_principal") == 100
    assert obtener_lux_retilap("cocina") == 300
    assert obtener_lux_retilap("sala") == 150
