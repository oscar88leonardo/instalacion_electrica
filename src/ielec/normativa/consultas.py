"""Cargador y consultor de tablas normativas YAML (NTC 2050, RETIE, RETILAP)."""

from pathlib import Path
from typing import Any, Dict, Optional
import yaml

_DIRECTORIO_ACTUAL = Path(__file__).resolve().parent
_DIRECTORIO_TABLAS = _DIRECTORIO_ACTUAL / "tablas"
_DIRECTORIO_CONDUCTORES = _DIRECTORIO_ACTUAL / "conductores"

_CACHE_TABLAS: Dict[str, Any] = {}


def _cargar_yaml(ruta: Path) -> Dict[str, Any]:
    ruta_str = str(ruta)
    if ruta_str not in _CACHE_TABLAS:
        if not ruta.exists():
            raise FileNotFoundError(f"No se encontró el archivo de tabla normativa: {ruta}")
        with open(ruta, "r", encoding="utf-8") as f:
            _CACHE_TABLAS[ruta_str] = yaml.safe_load(f)
    return _CACHE_TABLAS[ruta_str]


def obtener_carga_unitaria_vivienda() -> float:
    """Devuelve la densidad de carga de alumbrado general en VA/m2 (NTC 2050 220.12)."""
    datos = _cargar_yaml(_DIRECTORIO_TABLAS / "tabla_220_12_cargas_unitarias.yaml")
    return float(datos["valores"]["unidades_de_vivienda"]["densidad_va_m2"])


def calcular_demanda_alumbrado_general(carga_total_va: float) -> float:
    """Aplica los factores de demanda de NTC 2050 Tabla 220.42.
    
    - Primeros 3000 VA al 100%.
    - De 3001 a 120000 VA al 35%.
    - Excedente a 120000 VA al 25%.
    """
    if carga_total_va <= 3000.0:
        return carga_total_va
    elif carga_total_va <= 120000.0:
        return 3000.0 + (carga_total_va - 3000.0) * 0.35
    else:
        return 3000.0 + (120000.0 - 3000.0) * 0.35 + (carga_total_va - 120000.0) * 0.25


def obtener_ampacidad_cobre(calibre_awg: str, temperatura_c: int = 75) -> int:
    """Obtiene la ampacidad del conductor de cobre según Tabla 310.15(B)(16)."""
    datos = _cargar_yaml(_DIRECTORIO_TABLAS / "tabla_310_15_b_16_ampacidad.yaml")
    cobre = datos.get("cobre", {})
    if calibre_awg not in cobre:
        raise ValueError(f"Calibre AWG '{calibre_awg}' no registrado en la tabla de ampacidad.")
    clave = f"ampacidad_{temperatura_c}c"
    return int(cobre[calibre_awg][clave])


def obtener_proteccion_maxima_240_4d(calibre_awg: str) -> Optional[int]:
    """Obtiene la protección máxima permitida por NTC 2050 240.4(D) para calibres pequeños."""
    datos = _cargar_yaml(_DIRECTORIO_TABLAS / "tabla_310_15_b_16_ampacidad.yaml")
    cobre = datos.get("cobre", {})
    if calibre_awg in cobre:
        return cobre[calibre_awg].get("proteccion_max_240_4d")
    return None


def obtener_calibre_minimo_tierra_equipos(proteccion_amperios: int) -> str:
    """Devuelve el calibre AWG mínimo de Cu para tierra de equipos según Tabla 250.122."""
    datos = _cargar_yaml(_DIRECTORIO_TABLAS / "tabla_250_122_tierra_equipos.yaml")
    for rango in datos["rangos"]:
        if proteccion_amperios <= rango["proteccion_max_amperios"]:
            return str(rango["calibre_min_cobre_awg"])
    return "6"


def obtener_calibre_minimo_electrodo_tierra(calibre_fase_acometida_awg: str) -> str:
    """Devuelve el calibre AWG mínimo de Cu para electrodo según Tabla 250.66."""
    datos = _cargar_yaml(_DIRECTORIO_TABLAS / "tabla_250_66_electrodo_tierra.yaml")
    # Para calibres comunes residenciales (<= 2 AWG como 14, 12, 10, 8, 6, 4, 2 AWG):
    return "8"


def obtener_impedancia_referencia_ohm_km(calibre_awg: str) -> float:
    """Devuelve la impedancia en ohm/km en ducto PVC según la tabla de referencia."""
    datos = _cargar_yaml(_DIRECTORIO_CONDUCTORES / "impedancias_referencia.yaml")
    pvc = datos.get("cobre_conduit_pvc", {})
    if calibre_awg not in pvc:
        raise ValueError(f"Calibre '{calibre_awg}' no registrado en tabla de impedancias de referencia.")
    return float(pvc[calibre_awg]["impedancia_ohm_km"])


def obtener_lux_retilap(tipo_espacio: str) -> int:
    """Devuelve el nivel de iluminancia recomendado por RETILAP para el tipo de espacio."""
    datos = _cargar_yaml(_DIRECTORIO_TABLAS / "tabla_retilap_iluminancia.yaml")
    espacios = datos.get("espacios", {})
    if tipo_espacio in espacios:
        return int(espacios[tipo_espacio]["iluminancia_lux"])
    return 150  # Valor por defecto seguro para áreas residenciales
