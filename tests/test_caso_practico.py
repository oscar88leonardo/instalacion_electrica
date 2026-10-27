"""Prueba de aceptación completa contra los valores de referencia del Caso Práctico (86 m²)."""

import pytest
from ielec.modelo.entidades import (
    Espacio,
    TipoEspacio,
    TipoSistemaElectrico,
    TipoCircuito,
    TipoProteccion,
)
from ielec.motor import (
    disenar_instalacion_electrica,
    calcular_carga_alumbrado_general,
    calcular_acometida,
)


@pytest.fixture
def espacios_caso_practico():
    return [
        Espacio(id="alcoba_p", nombre="Alcoba Principal", tipo=TipoEspacio.DORMITORIO_PRINCIPAL, area_m2=14.68),
        Espacio(id="alcoba_1", nombre="Alcoba 1", tipo=TipoEspacio.DORMITORIO_SECUNDARIO, area_m2=10.44),
        Espacio(id="alcoba_2", nombre="Alcoba 2", tipo=TipoEspacio.DORMITORIO_SECUNDARIO, area_m2=10.44),
        Espacio(id="sala", nombre="Sala", tipo=TipoEspacio.SALA, area_m2=14.00),
        Espacio(id="comedor", nombre="Comedor", tipo=TipoEspacio.COMEDOR, area_m2=12.00),
        Espacio(id="cocina", nombre="Cocina", tipo=TipoEspacio.COCINA, area_m2=9.00),
        Espacio(id="bano", nombre="Baño", tipo=TipoEspacio.BANO, area_m2=4.50),
        Espacio(id="pasillo", nombre="Hall", tipo=TipoEspacio.PASILLO, area_m2=10.94),
    ]


def test_carga_alumbrado_general_86m2():
    # Carga alumbrado general: 86 * 33 = 2838 VA
    carga = calcular_carga_alumbrado_general(86.0)
    assert carga == 2838.0


def test_acometida_y_regulacion_caso_practico():
    # Demanda caso práctico: 3996 VA (o 3996.3 VA)
    # Distancia: 15 m
    # Impedancia Z: 2.4 ohm/km
    # Tension: 120 V
    acometida = calcular_acometida(
        potencia_total_instalada_va=5838.0,
        potencia_demanda_va=3996.3,
        tension_v=120.0,
        longitud_m=15.0,
        impedancia_z_ohm_km=2.4,
    )
    
    # 1. Corriente de demanda = 3996.3 / 120 = 33.3 A
    assert acometida.corriente_demanda_a == 33.3
    
    # 2. Protección comercial = 40 A
    assert acometida.capacidad_proteccion_a == 40
    
    # 3. Conductor de fase y neutro = 8 AWG Cu
    assert acometida.calibre_fase_awg == "8"
    assert acometida.calibre_neutro_awg == "8"
    
    # 4. Caída de tensión = 2 * 2.4 * 0.015 * 33.3 = 2.40 V
    assert acometida.caida_tension_v == 2.40
    
    # 5. % Regulación = 2.0% (<= 3%)
    assert acometida.porcentaje_regulacion == 2.0
    assert acometida.cumple_regulacion is True
    
    # 6. Puesta a tierra
    assert acometida.calibre_tierra_equipos_awg == "10"
    assert acometida.calibre_electrodo_tierra_awg == "8"


def test_diseno_completo_caso_practico(espacios_caso_practico):
    diseno = disenar_instalacion_electrica(
        nombre_proyecto="Vivienda 86 m² Caso Práctico",
        area_construida_m2=86.0,
        espacios=espacios_caso_practico,
        longitud_acometida_m=15.0,
        impedancia_acometida_ohm_km=2.4,
        tension_v=120.0,
        sistema=TipoSistemaElectrico.MONOFASICO_120,
        incluir_circuito_bano_20a=True,
        num_circuitos_pequenos_artefactos=2,
    )
    
    # Verificación de cargas
    assert diseno.carga_alumbrado_general_va == 2838.0
    assert diseno.carga_pequenos_artefactos_va == 3000.0
    assert diseno.carga_total_instalada_va == 5838.0
    
    # Verificación de circuitos
    # Alumbrado: ceil(2838 / 1800) = 2 circuitos de 15 A
    # Pequeños artefactos: 2 circuitos de 20 A
    # Baño: 1 circuito de 20 A (GFCI)
    assert len(diseno.circuitos) == 5
    
    c1 = diseno.circuitos[0]
    assert c1.corriente_nominal_a == 15
    assert c1.calibre_fase_awg == "14"
    assert c1.potencia_va == 1419.0  # 2838 / 2
    
    c3 = diseno.circuitos[2]
    assert c3.tipo == TipoCircuito.PEQUENOS_ARTEFACTOS
    assert c3.corriente_nominal_a == 20
    assert c3.calibre_fase_awg == "12"
    assert c3.tipo_proteccion == TipoProteccion.GFCI
    
    c_bano = diseno.circuitos[4]
    assert c_bano.tipo == TipoCircuito.BANO
    assert c_bano.corriente_nominal_a == 20
    assert c_bano.calibre_fase_awg == "12"
    assert c_bano.tipo_proteccion == TipoProteccion.GFCI
    
    # Acometida
    assert diseno.acometida.calibre_fase_awg == "8"
    assert diseno.acometida.capacidad_proteccion_a == 40
    assert diseno.acometida.porcentaje_regulacion == 2.0
    assert diseno.acometida.cumple_regulacion is True
    
    # Medidor
    assert diseno.medidor.cumple is True
    assert diseno.medidor.corriente_nominal_a >= diseno.acometida.corriente_demanda_a
    
    # Iluminación
    assert len(diseno.iluminacion) == len(espacios_caso_practico)
    alcoba_p_calc = next(il for il in diseno.iluminacion if il.espacio_id == "alcoba_p")
    # Para 14.68 m², 100 lux, 800 lm, CU 0.55, MF 0.8:
    # N = (100 * 14.68) / (800 * 0.55 * 0.8) = 1468 / 352 = 4.17
    assert alcoba_p_calc.luminarias_calculadas == 4.17
    assert alcoba_p_calc.luminarias_adoptadas >= 4
