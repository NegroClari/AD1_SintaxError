# Análisis de Datos: Dataset de Farmacia

| | |
|:---|:---|
| **Institución** | Instituto Superior Politécnico Católico (ISPC) |
| **Carrera** | Tecnicatura en Ciencia de Datos e Inteligencia Artificial |
| **Módulo** | Analista de Datos I |
| **Grupo** | SintaxError |
| **Integrantes** | Acosta Otto · Pucheta Matias · Verdú Lucía · Rodriguez Loprete Catriel · Negro Clarisa |

---

## Sección 1: Importación de Datos

La importación de datos es una etapa crítica que condiciona todo el análisis posterior. Antes de cargar cualquier archivo es necesario conocer su origen, cómo fue generado, con qué frecuencia se actualiza, su formato y el método de importación a utilizar.

### 1.1 Descripción del Dataset

| Aspecto | Detalle |
|:---|:---|
| **Nombre del archivo** | `farmacia.csv` |
| **Origen** | Dataset provisto por la cátedra para el proyecto integrador del módulo Analista de Datos I |
| **Dominio** | Consultas en una farmacia argentina |
| **Cómo se generó** | Datos simulados que representan consultas de clientes con información de precios, coberturas de obra social, descuentos bancarios y métodos de pago |
| **Frecuencia de actualización** | Dataset estático — instantánea para uso académico, no se actualiza |
| **Formato** | CSV (Comma-Separated Values), codificación UTF-8 |
| **Dimensiones** | 1.000 registros × 19 variables |
| **Período cubierto** | Mayo 2025 – Abril 2026 |

### 1.2 Método de Importación

Se utilizó la librería **pandas** con la función `read_csv()`. Se especificó `encoding='utf-8'` para garantizar la correcta lectura de caracteres especiales del español (tildes, ñ). El dataset ocupa aproximadamente **774 KB** en memoria.

---

## Sección 2: EDA — Análisis Exploratorio de Datos

El EDA es la etapa inicial de todo proyecto de datos. Su objetivo es **entender el dataset** antes de aplicar modelos o sacar conclusiones. Se estructura en cuatro etapas: conocer los datos, limpiar, describir y visualizar.

---

### 2.1 Conocer los Datos

El dataset contiene **1.000 filas y 19 columnas**. A continuación se describe cada variable:

| # | Variable | Tipo | Descripción | Ejemplo |
|:---:|:---|:---:|:---|:---|
| 1 | `id_consulta` | int64 | Identificador único de la consulta | 1, 2, 3 |
| 2 | `fecha` | object | Fecha de la consulta (M/D/AAAA) | 4/13/2026 |
| 3 | `cliente_id` | int64 | Identificador del cliente (puede repetirse) | 9454545269 |
| 4 | `cliente_nombre` | object | Nombre completo del cliente | Martina García |
| 5 | `cliente_tel` | object | Teléfono de contacto del cliente | 920-347-5536 |
| 6 | `obra_social` | object | Nombre de la obra social o prepaga | OSECAC, PAMI, OSDE |
| 7 | `plan_afiliado` | object | Plan de cobertura dentro de la obra social | PMO, Plan General |
| 8 | `producto_nombre` | object | Nombre comercial del medicamento *(con nulos)* | Vastarel, Optamox |
| 9 | `droga_generica` | object | Denominación genérica del principio activo | Droga Genérica, Amoxicilina |
| 10 | `precio_lista` | int64 | Precio de venta al público sin descuentos, en ARS | 10.468 |
| 11 | `descuento_OS` | float64 | Proporción cubierta por la obra social (0 a 1) | 0.4, 0.9 |
| 12 | `metodo_pago` | object | Medio de pago utilizado *(con nulos)* | Débito, Efectivo |
| 13 | `descuento_banco` | float64 | Descuento adicional por banco (0 a 1) | 0, 0.10, 0.25 |
| 14 | `banco_promocion` | object | Descripción de la promoción bancaria aplicada | Sin Promo, BNA+ |
| 15 | `stock_disponible` | int64 | Unidades en stock al momento de la consulta | 57, 21 |
| 16 | `categoria` | object | Categoría terapéutica del medicamento | Cardiología, Antibióticos |
| 17 | `convertida` | object | Si la consulta resultó en venta — **100% nulo** | NaN |
| 18 | `requiere_receta` | object | Si el medicamento requiere receta médica | true, false |
| 19 | `precio_final` | int64 | Precio final pagado tras aplicar todos los descuentos, en ARS | 6.281 |

**Observaciones sobre la estructura:**

- `id_consulta` es clave primaria: los 1.000 valores son únicos.
- `cliente_id` puede repetirse: hay 1.000 clientes distintos, con un promedio de 1 consulta cada uno en el período registrado.
- La columna `convertida` está **100% vacía** y no aporta valor al análisis en su estado actual.
- El `precio_final` se calcula a partir de una fórmula verificable:

> **precio_final = precio_lista × (1 − descuento_OS) × (1 − descuento_banco)**

Esta fórmula fue validada contra todos los registros, con una diferencia máxima de 1 peso (por redondeo).

---

### 2.2 Limpieza de Datos

El objetivo de esta etapa es garantizar la calidad del dataset antes de analizarlo.

**Paso 1 — Valores nulos iniciales**
En la lectura directa del CSV se detectaron 1.151 valores nulos, concentrados en la columna `convertida` (que representa 1.000 de esos nulos, es decir el 100% de la columna).

**Paso 2 — Strings vacíos**
Pandas no detecta automáticamente las cadenas vacías `""` como nulos. Se revisaron todas las columnas de tipo texto y no se encontraron celdas con strings vacíos; los nulos estaban ya representados como `NaN` desde la lectura.

**Paso 3 — Tratamiento de valores faltantes**

| Columna | Nulos | Decisión |
|:---|:---:|:---|
| `convertida` | 1.000 (100%) | Se mantiene en el dataset pero se excluye del análisis. Requiere recolección adicional de datos. |
| `metodo_pago` | 104 (10,4%) | Se mantienen como `NaN`. Se excluyen automáticamente al calcular estadísticas. |
| `producto_nombre` | 29 (2,9%) | Se mantienen como `NaN`. |

**Paso 4 — Duplicados**
No se encontraron registros completamente duplicados. No se requirió ninguna acción.

**Paso 5 — Corrección de tipos**
Dos columnas tenían tipos incorrectos y fueron convertidas:
- `fecha`: de `object` (texto) a `datetime64`, para poder operar con fechas.
- `requiere_receta`: de `object` (strings `"true"` / `"false"`) a `bool`.

**Paso 6 — Valores atípicos (método IQR)**
Se aplicó el criterio de Rango Intercuartílico con un límite de 1,5×IQR:

| Variable | Atípicos detectados |
|:---|:---:|
| `precio_lista` | 107 |
| `precio_final` | 94 |
| `stock_disponible` | 0 |

Los valores atípicos en precios corresponden principalmente a consultas de afiliados PAMI, cuyo descuento del 90% produce precios finales muy bajos en relación al precio de lista. No representan errores de carga sino diferencias reales de cobertura. Se decidió mantenerlos.

---

### 2.3 Análisis Descriptivo

Se calcularon estadísticas de tendencia central y dispersión para las variables numéricas del dataset limpio.

**Variables numéricas — resumen estadístico:**

| Variable | Media | Mediana | Moda | Desvío Std | Rango |
|:---|---:|---:|---:|---:|---:|
| `precio_lista` | 22.126 | 20.174 | variable | 12.540 | 58.839 |
| `precio_final` | 11.127 | 9.354 | variable | 7.817 | 52.748 |
| `stock_disponible` | 50 | 50 | variable | 29 | 99 |
| `descuento_OS` | 0,43 | 0,40 | 0,40 | 0,09 | 0,50 |
| `descuento_banco` | 0,07 | 0,00 | 0,00 | 0,10 | 0,25 |

**Principales hallazgos:**

- El precio lista promedio es de **$22.126 ARS**, con una mediana de $20.174, lo que indica una distribución levemente asimétrica hacia valores altos.
- El precio final promedio es de **$11.127 ARS**, aproximadamente la mitad del precio lista, lo que refleja el impacto del descuento de obra social.
- El descuento de obra social más frecuente es del **40%** (corresponde a la mayoría de obras sociales, excepto PAMI que cubre el 90%).
- El 57% de las consultas no tiene descuento bancario adicional; el resto se distribuye entre 10%, 15%, 20% y 25%.

**Distribución por categoría de medicamento:**

| Categoría | Consultas |
|:---|---:|
| Otros | 562 |
| Analgésicos | 110 |
| Cardiología | 101 |
| Antibióticos | 92 |
| Gastrointestinal | 74 |
| Vitaminas | 61 |

**Distribución por método de pago:**

Los métodos más utilizados son Débito y Efectivo. Un 10,4% de las consultas no tiene método de pago registrado (`Sin dato`).

**Requiere receta:**
- 823 medicamentos (82,3%) **no requieren receta**.
- 177 medicamentos (17,7%) **sí requieren receta**.

---

### 2.4 Visualización

Se generaron 8 gráficos para representar visualmente los datos e identificar patrones que no son evidentes en tablas numéricas.

**Gráfico 1 — Histogramas de precios**
Muestra la distribución de `precio_lista` y `precio_final`. Ambas distribuciones son asimétricas hacia la derecha (cola larga en valores altos). La media y la mediana de `precio_final` están por debajo de las de `precio_lista`, evidenciando el efecto de los descuentos.

**Gráfico 2 — Top 10 obras sociales**
OSECAC, PAMI y Jerárquicos Salud concentran la mayor cantidad de consultas. La distribución es muy dispersa: hay 60 obras sociales distintas, lo que indica una base de pacientes muy heterogénea.

**Gráfico 3 — Categorías de medicamentos**
La categoría "Otros" agrupa más de la mitad de las consultas (562), lo que sugiere que la clasificación podría mejorarse con subcategorías más específicas. Analgésicos, Cardiología y Antibióticos son las categorías más definidas.

**Gráfico 4 — Métodos de pago**
Débito y Efectivo son los métodos más utilizados. Los pagos con billeteras virtuales (MODO/Mercado Pago) tienen presencia significativa. Se destaca un 10,4% de consultas sin método de pago registrado.

**Gráfico 5 — Boxplot precio final por categoría**
Los medicamentos de Cardiología y Antibióticos presentan precios finales más elevados que los Analgésicos y Vitaminas. En todas las categorías se observan valores atípicos (círculos fuera de los bigotes), que corresponden a casos extremos de descuento bancario alto combinado con obra social de alta cobertura.

**Gráfico 6 — Dispersión precio lista vs. precio final**
La relación entre ambas variables es lineal y positiva, como se espera de la fórmula de descuentos. El color de cada punto indica el descuento de obra social: los puntos verdes (descuento 90%, PAMI) se concentran en la franja inferior del gráfico, mientras que los puntos rojos/amarillos (descuento 40%) forman la franja principal.

**Gráfico 7 — Torta requiere receta**
El 82,3% de los medicamentos no requiere receta, lo que es consistente con el perfil de una farmacia con alto volumen de medicamentos de venta libre (analgésicos, vitaminas, antigripales).

**Gráfico 8 — Mapa de calor de correlaciones**
`precio_lista` y `precio_final` tienen correlación positiva alta (~0,90), lo cual es esperable dado que el precio final se deriva directamente del precio lista. `descuento_OS` y `precio_final` tienen correlación negativa (~−0,60): a mayor cobertura de obra social, menor es el precio que paga el paciente. Las demás variables numéricas no muestran correlaciones relevantes entre sí.

---

## Conclusiones

El análisis exploratorio del dataset de farmacia permitió obtener una comprensión completa de su estructura, calidad y comportamiento.

**Sobre la calidad de los datos:**
- La columna `convertida` está **100% vacía** y no puede ser utilizada en el análisis. Su recolección debería priorizarse para futuras versiones del dataset.
- `metodo_pago` presenta un 10,4% de nulos que pueden afectar análisis relacionados con medios de pago.
- El resto de las variables tiene calidad aceptable para el análisis.

**Sobre el negocio:**
- El **descuento de obra social es el factor más determinante del precio final**. PAMI, con cobertura del 90%, genera precios finales muy bajos que aparecen como atípicos estadísticos pero son completamente válidos.
- La mayoría de los clientes pertenecen a obras sociales con cobertura estándar del 40%.
- Los medicamentos de **Cardiología y Antibióticos** tienen los precios promedio más altos, mientras que **Analgésicos y Vitaminas** son los más accesibles.
- Aproximadamente **1 de cada 5 medicamentos** requiere receta médica.
