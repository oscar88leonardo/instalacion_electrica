"""Módulo de modelos de datos del sistema ielec."""

from .entidades import (
    TipoSistemaElectrico,
    TipoEspacio,
    TipoProteccion,
    TipoCircuito,
    Espacio,
    CalculoIluminacionEspacio,
    CircuitoRamal,
    Acometida,
    Medidor,
    HallazgoValidacion,
    DisenoElectrico,
)

__all__ = [
    "TipoSistemaElectrico",
    "TipoEspacio",
    "TipoProteccion",
    "TipoCircuito",
    "Espacio",
    "CalculoIluminacionEspacio",
    "CircuitoRamal",
    "Acometida",
    "Medidor",
    "HallazgoValidacion",
    "DisenoElectrico",
]
