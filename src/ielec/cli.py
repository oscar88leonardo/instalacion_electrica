"""Interfaz de línea de comandos (CLI) para ielec."""

import json
from pathlib import Path
from typing import Optional
import typer
import yaml
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .modelo.entidades import Espacio, TipoEspacio, TipoSistemaElectrico
from .motor import disenar_instalacion_electrica

app = typer.Typer(
    name="ielec",
    help="Herramienta de diseño de instalaciones eléctricas residenciales según NTC 2050 y RETIE.",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main():
    """Herramienta de diseño eléctrico según NTC 2050, RETIE y RETILAP."""
    pass


@app.command(name="calcular")
def calcular(
    archivo_proyecto: Path = typer.Argument(
        ...,
        help="Ruta al archivo de configuración proyecto.yaml",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    salida_json: Optional[Path] = typer.Option(
        None,
        "--salida-json",
        "-o",
        help="Ruta opcional para guardar el diseño calculado en formato JSON",
    ),
):
    """Calcula la instalación eléctrica completa a partir de un archivo YAML."""
    with open(archivo_proyecto, "r", encoding="utf-8") as f:
        datos = yaml.safe_load(f)
        
    p = datos.get("proyecto", {})
    ac = datos.get("acometida", {})
    espacios_data = datos.get("espacios", [])
    circuitos_esp = datos.get("circuitos_especiales_normativos", {})
    
    nombre_proyecto = p.get("nombre", "Proyecto Residencial")
    area_construida = float(p.get("area_construida_exterior_m2", 0.0))
    sistema_str = p.get("sistema", "MONOFASICO_120")
    tension_v = float(p.get("tension_nominal_v", 120.0))
    longitud_acometida = float(ac.get("longitud_m", 15.0))
    z_acometida = ac.get("impedancia_z_ohm_km")
    if z_acometida is not None:
        z_acometida = float(z_acometida)
        
    pa_info = circuitos_esp.get("pequenos_artefactos", {})
    cant_pa = int(pa_info.get("cantidad", 2))
    
    bano_info = circuitos_esp.get("bano", {})
    inc_bano = bool(bano_info.get("incluir_circuito_exclusivo_20a", True))
    
    lav_info = circuitos_esp.get("lavanderia", {})
    inc_lav = bool(lav_info.get("incluir_circuito_20a", False))
    
    espacios = [
        Espacio(
            id=e["id"],
            nombre=e["nombre"],
            tipo=TipoEspacio(e["tipo"]),
            area_m2=float(e["area_m2"]),
            perimetro_m=float(e.get("perimetro_m", 0.0)) if e.get("perimetro_m") else None,
        )
        for e in espacios_data
    ]
    
    diseno = disenar_instalacion_electrica(
        nombre_proyecto=nombre_proyecto,
        area_construida_m2=area_construida,
        espacios=espacios,
        longitud_acometida_m=longitud_acometida,
        impedancia_acometida_ohm_km=z_acometida,
        tension_v=tension_v,
        sistema=TipoSistemaElectrico(sistema_str),
        incluir_circuito_bano_20a=inc_bano,
        num_circuitos_pequenos_artefactos=cant_pa,
        num_circuitos_lavanderia=1 if inc_lav else 0,
    )
    
    # Renderizado en consola con Rich
    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]PROYECTO:[/bold cyan] {diseno.nombre_proyecto}\n"
            f"[bold]Área construida exterior:[/bold] {diseno.area_construida_m2} m² | "
            f"[bold]Sistema:[/bold] {diseno.sistema.value} (120 V, 60 Hz)\n"
            f"[bold]Carga alumbrado general:[/bold] {diseno.carga_alumbrado_general_va:,.1f} VA | "
            f"[bold]Total instalada:[/bold] {diseno.carga_total_instalada_va:,.1f} VA | "
            f"[bold green]Demanda calculada:[/bold green] {diseno.carga_demanda_va:,.1f} VA",
            title="[bold yellow]⚡ MEMORIA DE DISEÑO ELÉCTRICO RESIDENCIAL (NTC 2050 / RETIE)[/bold yellow]",
        )
    )
    
    # Cuadro de cargas
    tabla_circuitos = Table(title="CUADRO DE CARGAS Y CIRCUITOS RAMALES", header_style="bold magenta")
    tabla_circuitos.add_column("Circuito", style="cyan", justify="center")
    tabla_circuitos.add_column("Descripción")
    tabla_circuitos.add_column("Tipo", style="blue")
    tabla_circuitos.add_column("VA", justify="right")
    tabla_circuitos.add_column("A (120V)", justify="right")
    tabla_circuitos.add_column("Protección", justify="center")
    tabla_circuitos.add_column("Conductor (Cu)", justify="center")
    tabla_circuitos.add_column("Tipo Protección", style="green")
    
    for c in diseno.circuitos:
        tabla_circuitos.add_row(
            c.codigo,
            c.descripcion,
            c.tipo.value,
            f"{c.potencia_va:,.1f}",
            f"{c.corriente_diseno_a:.1f}",
            f"{c.corriente_nominal_a} A",
            f"{c.calibre_fase_awg} AWG",
            f"{c.tipo_proteccion.value}" + (" [TR]" if c.requiere_tr else ""),
        )
    console.print(tabla_circuitos)
    
    # Acometida y regulación
    tabla_acometida = Table(title="ALIMENTADOR, REGULACIÓN Y PUESTA A TIERRA", header_style="bold green")
    tabla_acometida.add_column("Parámetro", style="bold")
    tabla_acometida.add_column("Valor Calculado", style="cyan")
    tabla_acometida.add_column("Criterio / Norma", style="dim")
    
    tabla_acometida.add_row("Corriente de demanda", f"{diseno.acometida.corriente_demanda_a:.1f} A", "I = S_demanda / 120 V")
    tabla_acometida.add_row("Interruptor termomagnético acometida", f"{diseno.acometida.capacidad_proteccion_a} A", "Comercial normalizado")
    tabla_acometida.add_row("Conductor de fase y neutro", f"{diseno.acometida.calibre_fase_awg} AWG Cu", "NTC 2050 Tabla 310.15(B)(16) a 60°C")
    tabla_acometida.add_row("Distancia de acometida", f"{diseno.acometida.longitud_m:.1f} m", "Longitud de ruta")
    tabla_acometida.add_row("Caída de tensión (ΔV)", f"{diseno.acometida.caida_tension_v:.2f} V", f"Z = {diseno.acometida.impedancia_z_ohm_km} Ω/km")
    tabla_acometida.add_row(
        "% Regulación de tensión",
        f"{diseno.acometida.porcentaje_regulacion:.2f}%" + (" [bold green]✓ CUMPLE[/bold green]" if diseno.acometida.cumple_regulacion else " [bold red]✗ NO CUMPLE[/bold red]"),
        "NTC 2050 210.19(A) (Límite ≤ 3.0%)",
    )
    tabla_acometida.add_row("Tierra de equipos (alimentador)", f"{diseno.acometida.calibre_tierra_equipos_awg} AWG Cu", "NTC 2050 Tabla 250.122")
    tabla_acometida.add_row("Conductor electrodo de tierra", f"{diseno.acometida.calibre_electrodo_tierra_awg} AWG Cu", "NTC 2050 Tabla 250.66")
    tabla_acometida.add_row("Medidor de energía", f"{diseno.medidor.tipo} {diseno.medidor.corriente_nominal_a} A" + (" [bold green]✓ CUMPLE[/bold green]" if diseno.medidor.cumple else " [bold red]✗[/bold red]"), "I_nominal >= I_demanda")
    console.print(tabla_acometida)
    
    # Iluminación
    if diseno.iluminacion:
        tabla_lux = Table(title="CÁLCULO DE ILUMINACIÓN SEGÚN RETILAP (MÉTODO DE LÚMENES)", header_style="bold yellow")
        tabla_lux.add_column("Espacio", style="cyan")
        tabla_lux.add_column("Área (m²)", justify="right")
        tabla_lux.add_column("Lux Requerido", justify="right")
        tabla_lux.add_column("Luminarias Calculadas", justify="right")
        tabla_lux.add_column("Luminarias Adoptadas", justify="center", style="bold green")
        
        for il in diseno.iluminacion:
            tabla_lux.add_row(
                il.nombre_espacio,
                f"{il.area_m2:.2f}",
                f"{il.lux_requerido} lx",
                f"{il.luminarias_calculadas:.2f}",
                str(il.luminarias_adoptadas),
            )
        console.print(tabla_lux)
        
    # Hallazgos normativos
    if diseno.hallazgos:
        console.print("[bold yellow]Hallazgos de Validación Normativa:[/bold yellow]")
        for h in diseno.hallazgos:
            color = "red" if h.severidad == "ERROR" else "yellow"
            console.print(f"  [{color}]• [{h.severidad}] {h.articulo_norma}:[/{color}] {h.mensaje}")
    else:
        console.print("[bold green]✓ Todas las validaciones normativas de la V1 fueron superadas exitosamente.[/bold green]")
        
    console.print()
    
    if salida_json:
        with open(salida_json, "w", encoding="utf-8") as f:
            f.write(diseno.model_dump_json(indent=2))
        console.print(f"[bold green]Diseño exportado exitosamente a:[/bold green] {salida_json}")


if __name__ == "__main__":
    app()
