# =============================================================================
# ESPACIOS CURRICULARES
# - CIENCIA DE DATOS I | Grupo: Syntax Error
# - ANALISTA DE DATOS I | Grupo: 19
# Instituto Superior Politécnico Córdoba - ISPC
# SECCIÓN 1: IMPORTACIÓN DE DATOS
# =============================================================================

import os
import pandas as pd

HERE    = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(HERE, "..", "Datos", "farmacia.csv")
SALIDA  = os.path.join(HERE, "farmacia_importado.csv")


def importar_datos(ruta: str) -> pd.DataFrame:
    """Carga el CSV y devuelve el DataFrame sin modificaciones."""
    return pd.read_csv(ruta, encoding="utf-8")


if __name__ == "__main__":
    df  = importar_datos(ENTRADA)
    mem = df.memory_usage(deep=True).sum() / 1024

    print(f"Importado: {df.shape[0]:,} filas x {df.shape[1]} columnas | {mem:.0f} KB")
    print(df.head().to_string())

    df.to_csv(SALIDA, index=False, encoding="utf-8")
    print(f"-> {SALIDA}")
