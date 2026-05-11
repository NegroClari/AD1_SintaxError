# =============================================================================
# ESPACIOS CURRICULARES
# - CIENCIA DE DATOS I | Grupo: Syntax Error
# - ANALISTA DE DATOS I | Grupo: 19
# Instituto Superior Politécnico Córdoba - ISPC
# SECCIÓN 2.3: ANÁLISIS DESCRIPTIVO
# =============================================================================

import os
import pandas as pd
import numpy as np

HERE    = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(HERE, "..", "03_limpieza", "farmacia_limpio.csv")
SALIDA  = os.path.join(HERE, "estadisticas_descriptivas.csv")

COLS_NUM = ["precio_lista", "descuento_OS", "descuento_banco", "stock_disponible", "precio_final"]


def calcular_estadisticas(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve media, mediana, moda, desvío, mín, máx, rango, Q1 y Q3 por variable numérica."""
    filas = []
    for col in COLS_NUM:
        s = df[col].dropna()
        filas.append({
            "variable"  : col,
            "media"     : round(s.mean(), 2),
            "mediana"   : round(s.median(), 2),
            "moda"      : round(s.mode()[0], 2),
            "desvio_std": round(s.std(), 2),
            "minimo"    : round(s.min(), 2),
            "maximo"    : round(s.max(), 2),
            "rango"     : round(s.max() - s.min(), 2),
            "q25"       : round(s.quantile(0.25), 2),
            "q75"       : round(s.quantile(0.75), 2),
        })
    return pd.DataFrame(filas)


if __name__ == "__main__":
    df = pd.read_csv(ENTRADA, encoding="utf-8", parse_dates=["fecha"])

    print(df[COLS_NUM].describe().round(2).to_string())

    enc  = f"\n  {'Variable':<22} {'Media':>12} {'Mediana':>12} {'Moda':>12} {'Desvío Std':>12} {'Rango':>12}"
    sep  = "  " + "-" * 84
    rows = [enc, sep]
    for col in ["precio_lista", "precio_final", "stock_disponible"]:
        s = df[col]
        rows.append(f"  {col:<22} {s.mean():>12,.0f} {s.median():>12,.0f} {s.mode()[0]:>12,.0f} {s.std():>12,.0f} {(s.max()-s.min()):>12,.0f}")
    print("\n".join(rows))

    for col, titulo in [("obra_social", "Obras Sociales"), ("categoria", "Categorías"), ("metodo_pago", "Métodos de Pago"), ("droga_generica", "Drogas Genéricas"), ("plan_afiliado", "Planes")]:
        print(f"\n{titulo}:\n{df[col].value_counts(dropna=False).head(10).to_string()}")

    grupo = df.groupby("categoria")[["precio_lista", "precio_final"]].mean().round(0).sort_values("precio_final", ascending=False)
    print(f"\nPrecio promedio por categoría:\n{grupo.to_string()}")

    receta = df["requiere_receta"].value_counts()
    print(f"\nRequiere receta: {receta.get(True, 0)} sí | {receta.get(False, 0)} no")

    stats = calcular_estadisticas(df)
    stats.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"\n-> {SALIDA}")
