# Alcance de la Versión 1 (V1)

## Objetivo
Implementar el motor de diseño eléctrico (cálculo según NTC 2050 2ª ed., RETIE 2026 y RETILAP) para viviendas unifamiliares residenciales, limitado estrictamente a la tipología y alcance del caso práctico de referencia (86 m²).

## Alcance Incluido
1. **Sistema Eléctrico:**
   - Exclusivamente monofásico 120 V (1 Fase + 1 Neutro + 1 Tierra de protección).
   - Tensión nominal: 120 V AC, 60 Hz.

2. **Cargas Consideradas:**
   - **Alumbrado general:** cálculo por área construida a razón de $33\ \text{VA/m}^2$ (NTC 2050 Tabla 220.12).
   - **Tomacorrientes de uso general:** cubiertos bajo la carga de alumbrado general.
   - **Pequeños artefactos:** mínimo 2 circuitos de 20 A (120 V, 1500 VA cada uno) para cocina/comedor (NTC 2050 210.11(C)(1) y 220.52(A)).
   - **Lavandería:** 1 circuito de 20 A (120 V, 1500 VA) exclusivo para lavandería/planchado (NTC 2050 210.11(C)(2) y 220.52(B)).
   - **Cuarto de baño:** 1 circuito de 20 A para tomacorrientes de baño (NTC 2050 210.11(C)(3)). Conforme a 220.52 no adiciona carga de demanda en el cálculo de alimentador.

3. **Cálculo de Iluminación:**
   - Método de lúmenes / cavidad zonal ($N = \frac{E \cdot A}{F \cdot CU \cdot MF}$).
   - Niveles de iluminancia mínima ($E$) por tipo de espacio según RETILAP.

4. **Dimensionamiento de Circuitos Ramales:**
   - Circuitos de 15 A con conductor mínimo 14 AWG Cu THHN/THWN.
   - Circuitos de 20 A con conductor mínimo 12 AWG Cu THHN/THWN.
   - Protección termomagnética calibrada según NTC 2050 240.4(D).

5. **Protecciones Especiales:**
   - **AFCI:** obligatorio en dormitorios, sala y áreas habitables según NTC 2050 210.12.
   - **GFCI:** obligatorio en baño, mesón de cocina, zona de lavandería y tomas exteriores según NTC 2050 210.8.
   - **TR (Tamper Resistant):** tomacorrientes con protección infantil en todas las áreas según NTC 2050 406.12.

6. **Acometida y Alimentador:**
   - Demanda calculada con factores de demanda de NTC 2050 Tabla 220.42 (primeros 3000 VA al 100%, excedente al 35%).
   - Corriente de acometida: $I = \frac{S_{\text{demanda}}}{120\ \text{V}}$.
   - Selección de conductor de fase y neutro (ampacidad Tabla 310.15(B)(16) a 75 °C o 60 °C, ajustada).
   - Regulación / caída de tensión: $\Delta V = 2 \cdot Z \cdot L \cdot I$, con $\%Reg \le 3\%$ en alimentador. Se usa el valor de referencia de la presentación ($Z = 2,4\ \Omega/\text{km}$ para 8 AWG en ducto PVC).

7. **Sistema de Puesta a Tierra (SPT):**
   - Conductor de tierra de equipos por circuito y alimentador según NTC 2050 Tabla 250.122.
   - Conductor del electrodo de puesta a tierra según NTC 2050 Tabla 250.66.
   - Especificación del electrodo (varilla copperweld de $2,4\ \text{m} \times 12,7\ \text{mm}$, resistencia $\le 25\ \Omega$).

8. **Medidor:**
   - Selección de medidor monofásico con corriente nominal superior a la corriente de demanda.

## Exclusiones en V1
- Cargas individuales específicas (estufa eléctrica, ducha eléctrica, calentador de agua, aire acondicionado, motobomba).
- Sistemas bifásicos (120/240 V o 208/120 V) y trifásicos.
- Desbalance de fases.
- Catálogos dinámicos de fabricantes para reactancia inductiva variable.
