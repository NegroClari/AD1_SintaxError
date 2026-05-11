# =============================================================================
# ANALISTA DE DATOS I — ISPC | Grupo: SintaxError
# SECCIÓN 2.2: LIMPIEZA DE DATOS
# =============================================================================

import os
import pandas as pd
import numpy as np

HERE    = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(HERE, "..", "01_importacion", "farmacia_importado.csv")
SALIDA  = os.path.join(HERE, "farmacia_limpio.csv")


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pasos de la limpieza:
      1. Reemplaza strings vacíos por NaN
      2. Convierte 'fecha' a datetime
      3. Convierte 'requiere_receta' a bool
      4. Elimina filas completamente duplicadas
    """
    df = df.copy()
     # --- MEJORA 1: ELIMINACIÓN DE COLUMNA CONVERTIDA
    if 'convertida' in df.columns:
        df.drop(columns=['convertida'], inplace=True)

    # --- MEJORA 2: ESTANDARIZACIÓN DE CATEGORÍAS 
    cols_estandarizar = ["obra_social", "metodo_pago", "banco_promocion", "categoria"]
    for col in cols_estandarizar:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title().replace("Nan", np.nan)
    
    df.replace("", np.nan, inplace=True)
    df["fecha"] = pd.to_datetime(df["fecha"])
    df["requiere_receta"] = (
        df["requiere_receta"].astype(str).str.lower().str.strip()
        .map({"true": True, "false": False})
    )
    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


if __name__ == "__main__":
    df_raw = pd.read_csv(ENTRADA, encoding="utf-8")

    print(f"PASO 1 — NaN iniciales: {df_raw.isnull().sum().sum()}")

    obj_cols = df_raw.select_dtypes(include="object").columns
    vacios   = {c: int((df_raw[c].str.strip() == "").sum()) for c in obj_cols}
    vacios   = {c: n for c, n in vacios.items() if n > 0}
    print(f"PASO 2 — Strings vacíos: {', '.join(f'{c}={n}' for c, n in vacios.items()) or 'ninguno'}")

    n_conv = int(df_raw["convertida"].isna().sum() + (df_raw["convertida"].astype(str).str.strip() == "").sum())
    n_mp   = int(df_raw["metodo_pago"].isna().sum() + (df_raw["metodo_pago"].astype(str).str.strip() == "").sum())
    n_pn   = int(df_raw["producto_nombre"].isna().sum() + (df_raw["producto_nombre"].astype(str).str.strip() == "").sum())
    print(f"PASO 3 — Nulos: convertida={n_conv} (excluida), metodo_pago={n_mp}, producto_nombre={n_pn} (mantenidos como NaN)")

    n_dup = int(df_raw.duplicated().sum())
    print(f"PASO 4 — Duplicados: {n_dup} {'eliminados' if n_dup > 0 else '(ninguno)'}")

    print("PASO 5 — Tipos corregidos: fecha -> datetime64 | requiere_receta -> bool")

    df_temp = df_raw.replace("", np.nan)
    outliers = {}
    for col in ["precio_lista", "precio_final", "stock_disponible"]:
        Q1, Q3 = df_temp[col].quantile(0.25), df_temp[col].quantile(0.75)
        IQR    = Q3 - Q1
        outliers[col] = int(df_temp[(df_temp[col] < Q1 - 1.5 * IQR) | (df_temp[col] > Q3 + 1.5 * IQR)].shape[0])
    print(f"PASO 6 — Outliers (IQR): {', '.join(f'{c}={n}' for c, n in outliers.items())}")

    df_limpio = limpiar_datos(df_raw)
    df_limpio.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"Resultado: {df_limpio.shape[0]:,} filas | {df_limpio.isnull().sum().sum()} nulos totales | -> {SALIDA}")
