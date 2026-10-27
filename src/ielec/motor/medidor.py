"""Selección y verificación del medidor de energía para vivienda monofásica."""

from ..modelo.entidades import Medidor


def verificar_medidor_monofasico(
    corriente_demanda_a: float,
    corriente_nominal_catalogo_a: int = 50,
) -> Medidor:
    """Verifica que el medidor cubra la corriente de demanda del alimentador."""
    cumple = corriente_nominal_catalogo_a >= corriente_demanda_a
    return Medidor(
        tipo="Monofásico",
        tension_nominal_v="120 V (o 120/240 V compatible)",
        corriente_nominal_a=corriente_nominal_catalogo_a,
        corriente_demanda_a=corriente_demanda_a,
        cumple=cumple,
    )
