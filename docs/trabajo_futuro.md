# Trabajo Futuro (Versiones Posteriores a V1)

Este documento registra las funcionalidades, ampliaciones normativas y capacidades técnicas que quedan fuera del alcance de la V1 y se incorporarán en versiones futuras.

## 1. Cargas Especiales e Individuales
- **Circuitos individuales dedicados:**
  - Estufa eléctrica / cocina (NTC 2050 220.55).
  - Horno eléctrico independiente.
  - Ducha eléctrica / calentador de paso (NTC 2050 422).
  - Calentador de agua de acumulación (NTC 2050 422.13: dimensionamiento al 125% continuo).
  - Aire acondicionado (NTC 2050 440).
  - Motobomba / equipo hidroneumático (NTC 2050 430: protección y conductor al 125%).
  - Secadora de ropa (NTC 2050 220.54: mínimo 5000 VA o potencia de placa).
- **Factores de demanda combinados:**
  - Aplicación de factor de demanda para 4 o más artefactos fijos según NTC 2050 220.53 (75% de demanda).

## 2. Sistemas Eléctricos Bifásicos y Trifásicos
- **Monofásico trifilar (120/240 V o 208/120 V):**
  - Asignación de circuitos a Fase A y Fase B.
  - Algoritmo de optimización para balanceo de fases ($Desbalance\% \le 5\%$).
  - Cálculo de corriente en el conductor neutro desbalanceado (NTC 2050 220.61).
  - Dimensionamiento de acometida bifilar / trifilar y medidor bifásico.
- **Trifásico tetrafilar (208/120 V o 480/277 V):**
  - Reparto y balanceo en tres fases (A, B, C).
  - Corriente de línea $I = \frac{S}{\sqrt{3} \cdot V_{LL}}$.
  - Medidor trifásico y alimentadores de 4 hilos más tierra.

## 3. Catálogos Dinámicos de Fabricantes de Conductores
- Integración de catálogos técnicos de fabricantes comerciales (Centelsa by Nexans, Procables, Cables de Energía, etc.).
- Desglose de parámetros:
  - Resistencia en corriente continua $R_{DC}$ a 20 °C.
  - Resistencia en corriente alterna $R_{AC}$ a 75 °C y 90 °C.
  - Reactancia inductiva $X_L$ según tipo de ducto (conduit PVC, EMT, IMC, aluminio).
  - Cálculo dinámico de impedancia eficaz:
    $$Z_{EF} = R \cdot \cos\theta + X_L \cdot \operatorname{sen}\theta$$
    para diferentes factores de potencia de carga ($\cos\theta = 0,85$, $0,90$, $0,95$, $1,0$).

## 4. Opciones de Canalizaciones y Tuberías
- Dimensionamiento automático de ductos conduit según porcentaje de ocupación (NTC 2050 Capítulo 9 Tabla 1: 40% para 3 o más conductores, 31% para 2 conductores, 53% para 1 conductor).
- Verificación de tablas de dimensiones de tubos PVC, EMT e IMC.

## 5. Plantillas de Rótulo y Operadores de Red
- Plantillas específicas para empresas distribuidoras (OR):
  - Electrohuila, Enel Colombia, EPM, Celsia, Air-e, Afinia, etc.
- Adaptación a normas de presentación de proyectos de cada operador.

## 6. Módulo 2 Avanzado (CAD / Geometría)
- Detección automática de polígonos de recintos a partir de líneas de muro arquitectónico sin requerir la polilínea manual `ESPACIOS`.
- Enrutamiento óptimo de tuberías evitando cruce de muros estructurales o columnas (mediante algoritmos $A^*$ o Voronoi).
- Compatibilidad nativa con modelos IFC / BIM (Revit, Archicad).
