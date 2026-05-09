# =============================================================================
# ANALISTA DE DATOS I — ISPC | Grupo: SintaxError
# SECCIÓN 2.1: CONOCER LOS DATOS
# =============================================================================

import os
import pandas as pd

HERE    = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(HERE, "..", "01_importacion", "farmacia_importado.csv")
SALIDA  = os.path.join(HERE, "resumen_columnas.csv")

DICCIONARIO = {
    "id_consulta"     : "Identificador único de la consulta",
    "fecha"           : "Fecha de la consulta (M/D/AAAA)",
    "cliente_id"      : "Identificador del cliente (puede repetirse)",
    "cliente_nombre"  : "Nombre completo del cliente",
    "cliente_tel"     : "Teléfono de contacto del cliente",
    "obra_social"     : "Nombre de la obra social o prepaga",
    "plan_afiliado"   : "Plan de cobertura dentro de la obra social",
    "producto_nombre" : "Nombre comercial del medicamento (con nulos)",
    "droga_generica"  : "Denominación genérica del principio activo",
    "precio_lista"    : "Precio sin descuentos en ARS",
    "descuento_OS"    : "Proporción cubierta por la obra social (0 a 1)",
    "metodo_pago"     : "Medio de pago utilizado (con nulos)",
    "descuento_banco" : "Descuento adicional por banco (0 a 1)",
    "banco_promocion" : "Descripción de la promoción bancaria",
    "stock_disponible": "Unidades en stock al momento de la consulta",
    "categoria"       : "Categoría terapéutica del medicamento",
    "convertida"      : "Si la consulta resultó en venta — 100% NULO",
    "requiere_receta" : "Si el medicamento requiere receta médica",
    "precio_final"    : "Precio final tras aplicar todos los descuentos (ARS)",
}


def generar_resumen(df: pd.DataFrame) -> pd.DataFrame:
    """Genera un DataFrame con una fila por columna: tipo, únicos, nulos y muestra."""
    filas = []
    for col in df.columns:
        serie = df[col]
        filas.append({
            "columna"          : col,
            "descripcion"      : DICCIONARIO.get(col, ""),
            "tipo_dato"        : str(serie.dtype),
            "total_registros"  : len(serie),
            "valores_unicos"   : serie.nunique(dropna=False),
            "nulos"            : serie.isna().sum(),
            "porcentaje_nulos" : round(serie.isna().mean() * 100, 1),
            "muestra_valores"  : ", ".join(str(v) for v in serie.dropna().unique()[:3]),
        })
    return pd.DataFrame(filas)


if __name__ == "__main__":
    df = pd.read_csv(ENTRADA, encoding="utf-8")

    n_id       = df["id_consulta"].nunique()
    n_conv     = df["convertida"].isna().sum()
    precio_calc = (df["precio_lista"] * (1 - df["descuento_OS"]) * (1 - df["descuento_banco"])).round(0).astype("Int64")
    dif_max    = (df["precio_final"] - precio_calc).abs().max()
    print(f"Estructura: {df.shape[0]:,} filas x {df.shape[1]} columnas | id único: {'Sí' if n_id == len(df) else 'No'} | 'convertida' {n_conv/len(df)*100:.0f}% nula | fórmula precio dif. máx: {dif_max}")

    resumen = generar_resumen(df)
    print(resumen[["columna", "tipo_dato", "valores_unicos", "nulos", "porcentaje_nulos"]].to_string(index=False))

    resumen.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"-> {SALIDA}")
