"""Modelos de datos Pydantic para el diseño de instalaciones eléctricas residenciales."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class TipoSistemaElectrico(str, Enum):
    MONOFASICO_120 = "MONOFASICO_120"
    BIFASICO_120_240 = "BIFASICO_120_240"
    TRIFASICO_208_120 = "TRIFASICO_208_120"


class TipoEspacio(str, Enum):
    DORMITORIO_PRINCIPAL = "dormitorio_principal"
    DORMITORIO_SECUNDARIO = "dormitorio_secundario"
    SALA = "sala"
    COMEDOR = "comedor"
    COCINA = "cocina"
    BANO = "bano"
    ZONA_ROPAS = "zona_ropas"
    PASILLO = "pasillo"
    EXTERIOR = "exterior"
    OTRO = "otro"


class TipoProteccion(str, Enum):
    TERMOMAGNETICO_ESTANDAR = "TERMOMAGNETICO_ESTANDAR"
    AFCI = "AFCI"
    GFCI = "GFCI"
    AFCI_GFCI = "AFCI_GFCI"


class TipoCircuito(str, Enum):
    ALUMBRADO_Y_TOMAS_GENERALES = "ALUMBRADO_Y_TOMAS_GENERALES"
    PEQUENOS_ARTEFACTOS = "PEQUENOS_ARTEFACTOS"
    LAVANDERIA = "LAVANDERIA"
    BANO = "BANO"
    CARGA_ESPECIAL = "CARGA_ESPECIAL"


class Espacio(BaseModel):
    id: str
    nombre: str
    tipo: TipoEspacio
    area_m2: float = Field(gt=0, description="Área en metros cuadrados")
    perimetro_m: Optional[float] = Field(default=None, description="Perímetro útil en metros")


class CalculoIluminacionEspacio(BaseModel):
    espacio_id: str
    nombre_espacio: str
    tipo_espacio: TipoEspacio
    area_m2: float
    lux_requerido: int
    flujo_luminoso_lumen: float = 800.0
    coeficiente_utilizacion: float = 0.55
    factor_mantenimiento: float = 0.80
    luminarias_calculadas: float
    luminarias_adoptadas: int


class CircuitoRamal(BaseModel):
    numero: int
    codigo: str
    descripcion: str
    tipo: TipoCircuito
    tension_v: float = 120.0
    corriente_nominal_a: int = 15
    potencia_va: float
    corriente_diseno_a: float
    calibre_fase_awg: str = "14"
    calibre_neutro_awg: str = "14"
    calibre_tierra_awg: str = "14"
    tipo_proteccion: TipoProteccion = TipoProteccion.TERMOMAGNETICO_ESTANDAR
    requiere_tr: bool = True
    espacios_atendidos: List[str] = Field(default_factory=list)


class Acometida(BaseModel):
    sistema: TipoSistemaElectrico = TipoSistemaElectrico.MONOFASICO_120
    tension_v: float = 120.0
    potencia_total_instalada_va: float
    potencia_demanda_va: float
    corriente_demanda_a: float
    capacidad_proteccion_a: int
    calibre_fase_awg: str
    calibre_neutro_awg: str
    calibre_tierra_equipos_awg: str
    calibre_electrodo_tierra_awg: str
    longitud_m: float
    impedancia_z_ohm_km: float
    caida_tension_v: float
    porcentaje_regulacion: float
    cumple_regulacion: bool


class Medidor(BaseModel):
    tipo: str = "Monofásico"
    tension_nominal_v: str = "120 V (o 120/240 V compatible)"
    corriente_nominal_a: int = 50
    corriente_demanda_a: float
    cumple: bool


class HallazgoValidacion(BaseModel):
    regla_id: str
    articulo_norma: str
    severidad: str
    mensaje: str


class DisenoElectrico(BaseModel):
    nombre_proyecto: str
    area_construida_m2: float
    sistema: TipoSistemaElectrico
    carga_alumbrado_general_va: float
    carga_pequenos_artefactos_va: float
    carga_lavanderia_va: float
    carga_total_instalada_va: float
    carga_demanda_va: float
    circuitos: List[CircuitoRamal]
    iluminacion: List[CalculoIluminacionEspacio]
    acometida: Acometida
    medidor: Medidor
    hallazgos: List[HallazgoValidacion] = Field(default_factory=list)
