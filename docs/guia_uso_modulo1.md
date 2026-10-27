# Guía de Uso del Módulo 1 (Motor de Diseño Eléctrico)

Esta guía explica cómo utilizar el **Módulo 1** de `ielec`, cómo está estructurado el archivo de entrada `proyecto.yaml`, qué significa cada parámetro y cómo diligenciarlo correctamente para diseñar una instalación eléctrica residencial bajo **NTC 2050 (2ª ed.)**, **RETIE 2026** y **RETILAP**.

---

## 1. ¿Qué hace el Módulo 1?

El Módulo 1 toma la información del proyecto desde un archivo YAML y realiza automáticamente la cadena completa de cálculos de ingeniería eléctrica:
1. **Cálculo de iluminación (RETILAP):** determina el número de luminarias necesarias por espacio mediante el método de lúmenes / cavidad zonal ($N = \frac{E \cdot A}{F \cdot CU \cdot MF}$).
2. **Cargas de alumbrado general (NTC 2050 220.12):** calcula la potencia a razón de $33\ \text{VA/m}^2$ sobre el área exterior construida.
3. **Cargas de demanda (NTC 2050 220.42):** suma los circuitos obligatorios de pequeños artefactos y lavandería ($1500\ \text{VA}$ cada uno) y aplica los factores de demanda ($100\%$ a los primeros $3000\ \text{VA}$ y $35\%$ al excedente hasta $120000\ \text{VA}$).
4. **Dimensionamiento de circuitos ramales (NTC 2050 210.11 / 210.24):** define la cantidad mínima de circuitos de alumbrado y tomas generales ($15\ \text{A}$), pequeños artefactos ($20\ \text{A}$), lavandería ($20\ \text{A}$) y baño ($20\ \text{A}$).
5. **Asignación de protecciones (NTC 2050 210.8, 210.12, 406.12):** asigna interruptores AFCI en áreas habitables, GFCI en zonas húmedas y exige tomacorrientes Tamper Resistant (TR).
6. **Alimentador y regulación (NTC 2050 210.19(A) / 230.42):** calcula la corriente de demanda ($I = \frac{S}{120\ \text{V}}$), selecciona el disyuntor comercial, el calibre del conductor de fase y neutro (considerando ampacidad a $60\ ^\circ\text{C}$ según Art. 110.14(C)) y calcula la caída de tensión en voltios y porcentaje ($\%Reg \le 3\%$).
7. **Puesta a tierra (NTC 2050 250.122 / 250.66):** selecciona el conductor de tierra de equipos y el conductor del electrodo de puesta a tierra.
8. **Medidor:** verifica que la capacidad nominal cubra la corriente de demanda.
9. **Validador normativo:** audita que el diseño cumpla todas las reglas aplicables.

---

## 2. Cómo ejecutar el Módulo 1

Desde la raíz del proyecto, ejecuta el comando CLI en la terminal:

```bash
PYTHONPATH=src python3 -m ielec.cli calcular ruta/a/tu/proyecto.yaml
```

Por ejemplo, con el caso práctico de 86 m²:
```bash
PYTHONPATH=src python3 -m ielec.cli calcular ejemplos/caso_practico_86m2/proyecto.yaml
```

### Exportar los resultados a formato JSON
Si deseas guardar el resultado estructurado para interoperabilidad con otros sistemas o con el Módulo 2 de dibujo:
```bash
PYTHONPATH=src python3 -m ielec.cli calcular ejemplos/caso_practico_86m2/proyecto.yaml --salida-json diseno.json
```

---

## 3. Estructura y Diligenciamiento de `proyecto.yaml`

El archivo de configuración se organiza en **4 bloques principales**:
- `proyecto`
- `acometida`
- `circuitos_especiales_normativos`
- `espacios`

A continuación se detalla cada campo:

### 3.1 Bloque `proyecto`
Contiene los metadatos generales de la edificación y las características del sistema eléctrico.

```yaml
proyecto:
  nombre: "Vivienda Unifamiliar Caso Práctico"
  descripcion: "Vivienda residencial de un piso según caso práctico de referencia"
  sistema: "MONOFASICO_120"
  tension_nominal_v: 120.0
  frecuencia_hz: 60
  area_construida_exterior_m2: 86.0
```

| Campo | Tipo | Obligatorio | Descripción y Pautas de Diligenciamiento |
|---|---|---|---|
| `nombre` | Texto | Sí | Nombre o identificador del proyecto (se imprimirá en el reporte y rótulo). |
| `descripcion` | Texto | No | Resumen u observaciones del proyecto. |
| `sistema` | Texto | Sí | Para la Versión 1 (V1) debe ser **`MONOFASICO_120`** (1 Fase + 1 Neutro + 1 Tierra). |
| `tension_nominal_v` | Decimal | Sí | Tensión de fase a neutro. En Colombia para sistemas monofásicos es **`120.0`** V. |
| `frecuencia_hz` | Entero | Sí | Frecuencia de la red eléctrica (**`60`** Hz en Colombia). |
| `area_construida_exterior_m2` | Decimal | Sí | **Área construida exterior en $\text{m}^2$:** base para el cálculo de alumbrado general ($33\ \text{VA/m}^2$, NTC 2050 220.12). Se mide por el perímetro exterior. **Excluye:** patios abiertos sin techar, garajes abiertos o zonas sin terminar. |

---

### 3.2 Bloque `acometida`
Define la longitud de la ruta del alimentador y los parámetros para evaluar la caída de tensión.

```yaml
acometida:
  longitud_m: 15.0
  tipo_canalizacion: "ducto_pvc"
  impedancia_z_ohm_km: 2.4
  caida_tension_max_admisible_porc: 3.0
```

| Campo | Tipo | Obligatorio | Descripción y Pautas de Diligenciamiento |
|---|---|---|---|
| `longitud_m` | Decimal | Sí | Longitud física de la ruta del cable de acometida en metros (desde el medidor o punto de entrega hasta el tablero de distribución de la vivienda). |
| `tipo_canalizacion` | Texto | Sí | Tipo de ducto o tubería empleada (típicamente `"ducto_pvc"` en acometidas subterráneas residenciales). |
| `impedancia_z_ohm_km` | Decimal | No | Impedancia eficaz $Z$ del conductor en $\Omega/\text{km}$. Si no se indica, el motor toma el valor de referencia de la tabla de conductores según el calibre seleccionado. En el caso práctico de referencia se utilizó **`2.4`** $\Omega/\text{km}$ para conductor 8 AWG en ducto PVC. |
| `caida_tension_max_admisible_porc` | Decimal | Sí | Límite máximo de regulación según NTC 2050 210.19(A) Nota Informativa. Para alimentadores es **`3.0`**%. |

---

### 3.3 Bloque `circuitos_especiales_normativos`
Configura los circuitos obligatorios exigidos por la norma NTC 2050 adicionales al alumbrado general.

```yaml
circuitos_especiales_normativos:
  pequenos_artefactos:
    cantidad: 2
    potencia_unitaria_va: 1500.0
  bano:
    incluir_circuito_exclusivo_20a: true
  lavanderia:
    incluir_circuito_20a: false
```

| Subsección / Campo | Tipo | Valor habitual | Explicación Normativa |
|---|---|---|---|
| `pequenos_artefactos.cantidad` | Entero | `2` | NTC 2050 Art. 210.11(C)(1) exige **al menos dos** circuitos ramales de $20\ \text{A}$ para tomacorrientes de cocina, despensa y comedor. |
| `pequenos_artefactos.potencia_unitaria_va` | Decimal | `1500.0` | NTC 2050 Art. 220.52(A) fija en **$1500\ \text{VA}$** la carga de cada circuito de pequeños artefactos para el cálculo de demanda de la acometida. |
| `bano.incluir_circuito_exclusivo_20a` | Booleano | `true` | NTC 2050 Art. 210.11(C)(3) exige al menos un circuito de $20\ \text{A}$ exclusivo para tomas de cuarto de baño con protección GFCI. Conforme al Art. 220.52 no adiciona potencia a la demanda general. |
| `lavanderia.incluir_circuito_20a` | Booleano | `true` o `false` | NTC 2050 Art. 210.11(C)(2) exige un circuito ramal de $20\ \text{A}$ para zona de lavandería/planchado ($1500\ \text{VA}$ según 220.52(B)). Si la vivienda cuenta con zona de ropas o lavadora, debe colocarse en `true`. En el caso práctico base de 86 m² está en `false` porque no se desglosó dicho circuito independiente. |

---

### 3.4 Bloque `espacios`
Lista de cada una de las dependencias o recintos de la vivienda. Esta información alimenta el cálculo de iluminación según RETILAP y la asignación de protecciones especiales (AFCI / GFCI).

```yaml
espacios:
  - id: "alcoba_principal"
    nombre: "Alcoba Principal"
    tipo: "dormitorio_principal"
    area_m2: 14.68
  - id: "alcoba_1"
    nombre: "Alcoba 1"
    tipo: "dormitorio_secundario"
    area_m2: 10.44
  - id: "sala"
    nombre: "Sala"
    tipo: "sala"
    area_m2: 14.00
  - id: "comedor"
    nombre: "Comedor"
    tipo: "comedor"
    area_m2: 12.00
  - id: "cocina"
    nombre: "Cocina"
    tipo: "cocina"
    area_m2: 9.00
  - id: "bano"
    nombre: "Baño"
    tipo: "bano"
    area_m2: 4.50
  - id: "pasillo"
    nombre: "Hall y Circulaciones"
    tipo: "pasillo"
    area_m2: 10.94
```

#### Valores válidos para el campo `tipo` y su efecto normativo:

| Valor de `tipo` | Iluminancia RETILAP | Protección Requerida NTC 2050 |
|---|---|---|
| `dormitorio_principal` | $100\ \text{lx}$ | **AFCI** obligatorio (Art. 210.12) |
| `dormitorio_secundario` | $100\ \text{lx}$ | **AFCI** obligatorio (Art. 210.12) |
| `sala` | $150\ \text{lx}$ | **AFCI** obligatorio (Art. 210.12) |
| `comedor` | $150\ \text{lx}$ | **AFCI** obligatorio (Art. 210.12) |
| `cocina` | $300\ \text{lx}$ | **GFCI** en mesones (Art. 210.8) |
| `bano` | $150\ \text{lx}$ | **GFCI** obligatorio (Art. 210.8) |
| `zona_ropas` | $200\ \text{lx}$ | **GFCI** obligatorio (Art. 210.8) |
| `pasillo` | $100\ \text{lx}$ | **AFCI** recomendado en circulaciones |
| `exterior` | $50\ \text{lx}$ | **GFCI** obligatorio en tomas a la intemperie |
| `otro` | $150\ \text{lx}$ | Termomagnético estándar o según uso |

> [!TIP]
> El área (`area_m2`) de cada espacio debe corresponder al área libre interior del recinto para que el cálculo de lúmenes de RETILAP sea preciso.

---

## 4. Interpretación del Reporte en Terminal

Al ejecutar el comando `calcular`, el Módulo 1 despliega cuatro tablas de ingeniería:

```text
╭─────── ⚡ MEMORIA DE DISEÑO ELÉCTRICO RESIDENCIAL (NTC 2050 / RETIE) ────────╮
│ PROYECTO: Vivienda Unifamiliar Caso Práctico                                 │
│ Área construida exterior: 86.0 m² | Sistema: MONOFASICO_120 (120 V, 60 Hz)   │
│ Carga alumbrado general: 2,838.0 VA | Total instalada: 5,838.0 VA | Demanda  │
│ calculada: 3,993.3 VA                                                        │
╰──────────────────────────────────────────────────────────────────────────────╯
```
- **Carga alumbrado general:** $86.0\ \text{m}^2 \times 33\ \text{VA/m}^2 = 2838.0\ \text{VA}$.
- **Total instalada:** $2838.0\ \text{VA} + 2 \times 1500.0\ \text{VA} = 5838.0\ \text{VA}$.
- **Demanda calculada:** $3000\ \text{VA} + (5838 - 3000) \times 0.35 = 3993.3\ \text{VA}$.

### Cuadro de Cargas y Circuitos Ramales
- **C1 y C2:** Circuitos de alumbrado y tomas generales ($15\ \text{A}$, $14\ \text{AWG Cu}$, protección AFCI, tomas TR).
- **C3 y C4:** Circuitos de pequeños artefactos ($20\ \text{A}$, $12\ \text{AWG Cu}$, protección GFCI, tomas TR).
- **C5:** Circuito exclusivo de cuarto de baño ($20\ \text{A}$, $12\ \text{AWG Cu}$, protección GFCI, tomas TR).

### Alimentador, Regulación y Puesta a Tierra
- **Corriente de demanda:** $I = \frac{3993.3\ \text{VA}}{120\ \text{V}} = 33.3\ \text{A}$.
- **Disyuntor acometida:** $40\ \text{A}$ (comercial normalizado inmediatamente superior).
- **Calibre acometida:** $8\ \text{AWG Cu}$ (ampacidad de $40\ \text{A}$ a $60\ ^\circ\text{C}$ según NTC 2050 110.14(C)).
- **Caída de tensión:** $\Delta V = 2 \cdot Z \cdot L \cdot I = 2 \cdot 0.0024 \cdot 15 \cdot 33.3 = 2.40\ \text{V}$.
- **% Regulación:** $\frac{2.40\ \text{V}}{120\ \text{V}} \times 100 = 2.00\%$ (Cumple con creces el límite $\le 3.0\%$).
- **Tierra de equipos:** $10\ \text{AWG Cu}$ (Tabla 250.122 para disyuntor de $40\ \text{A}$).
- **Conductor de electrodo:** $8\ \text{AWG Cu}$ (Tabla 250.66 para conductor de entrada 8 AWG).
- **Medidor:** Monofásico $50\ \text{A}$ ($I_{\text{nominal}} \ge I_{\text{demanda}}$).

---

## 5. Plantilla Base para Nuevos Proyectos

Puedes copiar y pegar esta plantilla para iniciar un nuevo diseño residencial:

```yaml
proyecto:
  nombre: "Nombre de Mi Proyecto"
  descripcion: "Vivienda residencial unifamiliar"
  sistema: "MONOFASICO_120"
  tension_nominal_v: 120.0
  frecuencia_hz: 60
  area_construida_exterior_m2: 75.0

acometida:
  longitud_m: 12.0
  tipo_canalizacion: "ducto_pvc"
  impedancia_z_ohm_km: 2.4
  caida_tension_max_admisible_porc: 3.0

circuitos_especiales_normativos:
  pequenos_artefactos:
    cantidad: 2
    potencia_unitaria_va: 1500.0
  bano:
    incluir_circuito_exclusivo_20a: true
  lavanderia:
    incluir_circuito_20a: true

espacios:
  - id: "alcoba_1"
    nombre: "Alcoba Principal"
    tipo: "dormitorio_principal"
    area_m2: 12.50
  - id: "alcoba_2"
    nombre: "Alcoba 2"
    tipo: "dormitorio_secundario"
    area_m2: 9.80
  - id: "sala_comedor"
    nombre: "Sala Comedor"
    tipo: "sala"
    area_m2: 18.00
  - id: "cocina"
    nombre: "Cocina"
    tipo: "cocina"
    area_m2: 6.50
  - id: "bano"
    nombre: "Baño"
    tipo: "bano"
    area_m2: 3.80
  - id: "zona_ropas"
    nombre: "Zona de Ropas"
    tipo: "zona_ropas"
    area_m2: 4.20
  - id: "circulacion"
    nombre: "Circulación"
    tipo: "pasillo"
    area_m2: 5.00
```
