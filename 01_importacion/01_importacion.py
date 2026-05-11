# =============================================================================
# ESPACIOS CURRICULARES
# - CIENCIA DE DATOS I | Grupo: Syntax Error
# - ANALISTA DE DATOS I | Grupo: 19
# Instituto Superior Politécnico Córdoba - ISPC
# SECCIÓN 1: IMPORTACIÓN DE DATOS
# =============================================================================

import os
import pandas as pd

ENTRADA = "https://raw.githubusercontent.com/NegroClari/AD1_SintaxError/main/Datos/farmacia.csv"
SALIDA_LIMPIO = "farmacia_importado.csv"

def importar_datos(ruta: str) -> pd.DataFrame:
    """Carga el CSV directamente desde la URL de GitHub y devuelve el DataFrame."""
    return pd.read_csv(ruta, encoding="utf-8")

if __name__ == "__main__":
    try:
        df  = importar_datos(ENTRADA)
        mem = df.memory_usage(deep=True).sum() / 1024
        print(f"Importado: {df.shape[0]:,} filas x {df.shape[1]} columnas | {mem:.0f} KB")
        print(df.head().to_string())

        # En Colab, este archivo quedará en el entorno virtual temporal de la sesión
        df.to_csv(SALIDA_LIMPIO, index=False, encoding="utf-8")
        print(f"\nArchivo procesado y guardado con éxito como: {SALIDA_LIMPIO}")

    except Exception as e:
        print(f"Ocurrió un error al importar los datos: {e}")
