# =============================================================================
# ANALISTA DE DATOS I — ISPC | Grupo: SintaxError
# SECCIÓN 2.4: VISUALIZACIÓN
# =============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams["font.size"] = 11

HERE        = os.path.dirname(os.path.abspath(__file__))
ENTRADA     = os.path.join(HERE, "..", "03_limpieza", "farmacia_limpio.csv")
SALIDA_CORR = os.path.join(HERE, "correlaciones.csv")

fmt_ars = mticker.FuncFormatter(lambda x, _: f"${x:,.0f}")


def _guardar(nombre: str) -> None:
    plt.savefig(os.path.join(HERE, nombre), dpi=150, bbox_inches="tight")
    plt.close()


def generar_graficos(df: pd.DataFrame) -> pd.DataFrame:
    """Genera y guarda 8 gráficos PNG. Devuelve la matriz de correlaciones."""

    # 1. Histogramas de precios
    media_pf, mediana_pf, media_pl = df["precio_final"].mean(), df["precio_final"].median(), df["precio_lista"].mean()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].hist(df["precio_final"].dropna(), bins=30, color="#3498db", edgecolor="white", alpha=0.85)
    axes[0].axvline(media_pf,   color="red",    linestyle="--", lw=1.5, label=f"Media: ${media_pf:,.0f}")
    axes[0].axvline(mediana_pf, color="orange", linestyle="--", lw=1.5, label=f"Mediana: ${mediana_pf:,.0f}")
    axes[0].set_title("Distribución del Precio Final"); axes[0].set_xlabel("Precio Final (ARS)"); axes[0].set_ylabel("Frecuencia")
    axes[0].legend(); axes[0].xaxis.set_major_formatter(fmt_ars)
    axes[1].hist(df["precio_lista"].dropna(), bins=30, color="#2ecc71", edgecolor="white", alpha=0.85)
    axes[1].axvline(media_pl, color="red", linestyle="--", lw=1.5, label=f"Media: ${media_pl:,.0f}")
    axes[1].set_title("Distribución del Precio Lista"); axes[1].set_xlabel("Precio Lista (ARS)"); axes[1].set_ylabel("Frecuencia")
    axes[1].legend(); axes[1].xaxis.set_major_formatter(fmt_ars)
    plt.suptitle("Histogramas de Precios", fontsize=14, fontweight="bold"); plt.tight_layout()
    _guardar("grafico_01_histogramas_precios.png")

    # 2. Barras — Top 10 obras sociales
    top_os = df["obra_social"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(11, 5))
    bars = ax.bar(top_os.index, top_os.values, color=["#e74c3c" if v == top_os.max() else "#3498db" for v in top_os.values], edgecolor="white", alpha=0.85)
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=10)
    ax.set_title("Top 10 Obras Sociales por Cantidad de Consultas", fontsize=13, fontweight="bold")
    ax.set_xlabel("Obra Social"); ax.set_ylabel("Cantidad de Consultas"); ax.tick_params(axis="x", rotation=40)
    plt.tight_layout(); _guardar("grafico_02_obras_sociales.png")

    # 3. Barras — Categorías
    cat_counts = df["categoria"].value_counts()
    fig, ax = plt.subplots(figsize=(11, 5))
    bars = ax.bar(cat_counts.index, cat_counts.values, color=sns.color_palette("Set2", len(cat_counts)), edgecolor="white", alpha=0.9)
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=10)
    ax.set_title("Consultas por Categoría de Medicamento", fontsize=13, fontweight="bold")
    ax.set_xlabel("Categoría"); ax.set_ylabel("Cantidad de Consultas"); ax.tick_params(axis="x", rotation=30)
    plt.tight_layout(); _guardar("grafico_03_categorias.png")

    # 4. Barras — Métodos de pago
    mp_counts = df["metodo_pago"].value_counts(dropna=False)
    labels_mp = [str(i) if pd.notna(i) else "Sin dato" for i in mp_counts.index]
    fig, ax = plt.subplots(figsize=(11, 5))
    bars = ax.bar(labels_mp, mp_counts.values, color=["#e74c3c" if pd.isna(i) else "#9b59b6" for i in mp_counts.index], edgecolor="white", alpha=0.85)
    ax.bar_label(bars, fmt="%d", padding=3, fontsize=10)
    ax.set_title("Distribución de Métodos de Pago", fontsize=13, fontweight="bold")
    ax.set_xlabel("Método de Pago"); ax.set_ylabel("Cantidad de Consultas"); ax.tick_params(axis="x", rotation=40)
    plt.tight_layout(); _guardar("grafico_04_metodos_pago.png")

    # 5. Boxplot — precio_final por categoría
    df_cat    = df[df["categoria"].notna()].copy()
    orden_cat = df_cat.groupby("categoria")["precio_final"].median().sort_values(ascending=False).index
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(data=df_cat, x="categoria", y="precio_final", order=orden_cat, palette="Set2", linewidth=1.2, ax=ax)
    ax.set_title("Distribución del Precio Final por Categoría (Boxplot)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Categoría"); ax.set_ylabel("Precio Final (ARS)"); ax.yaxis.set_major_formatter(fmt_ars); ax.tick_params(axis="x", rotation=25)
    plt.tight_layout(); _guardar("grafico_05_boxplot_categorias.png")

    # 6. Dispersión — precio_lista vs precio_final
    fig, ax = plt.subplots(figsize=(10, 7))
    sc = ax.scatter(df["precio_lista"], df["precio_final"], c=df["descuento_OS"], cmap="RdYlGn", alpha=0.55, s=25, edgecolors="none")
    cb = plt.colorbar(sc, ax=ax, label="Descuento Obra Social")
    cb.set_ticks([0.4, 0.6, 0.8, 0.9]); cb.set_ticklabels(["40%", "60%", "80%", "90%"])
    ax.set_title("Precio Lista vs. Precio Final\n(color = descuento obra social)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Precio Lista (ARS)"); ax.set_ylabel("Precio Final (ARS)")
    ax.xaxis.set_major_formatter(fmt_ars); ax.yaxis.set_major_formatter(fmt_ars)
    plt.tight_layout(); _guardar("grafico_06_dispersion_precios.png")

    # 7. Torta — requiere receta
    receta_str = df["requiere_receta"].astype(str).str.strip().str.lower()
    sizes = [int((receta_str == "false").sum()), int((receta_str == "true").sum())]
    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(sizes, labels=["No requiere receta", "Requiere receta"], colors=["#2ecc71", "#e74c3c"],
                                      autopct="%1.1f%%", startangle=90, explode=(0, 0.05), textprops={"fontsize": 12})
    for at in autotexts: at.set_fontsize(12); at.set_fontweight("bold")
    ax.set_title("Proporción de Medicamentos\nque Requieren Receta", fontsize=13, fontweight="bold")
    plt.tight_layout(); _guardar("grafico_07_receta_pie.png")

    # 8. Mapa de calor — correlaciones
    num_cols = ["precio_lista", "descuento_OS", "descuento_banco", "stock_disponible", "precio_final"]
    corr = df[num_cols].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True,
                linewidths=0.5, linecolor="white", annot_kws={"size": 11}, ax=ax)
    ax.set_title("Mapa de Calor — Correlación entre Variables Numéricas", fontsize=13, fontweight="bold")
    ax.tick_params(axis="x", rotation=30); ax.tick_params(axis="y", rotation=0)
    plt.tight_layout(); _guardar("grafico_08_heatmap_correlacion.png")

    return corr


if __name__ == "__main__":
    df   = pd.read_csv(ENTRADA, encoding="utf-8", parse_dates=["fecha"])
    corr = generar_graficos(df)
    print("8 gráficos generados en: " + HERE)

    corr.to_csv(SALIDA_CORR, encoding="utf-8")
    print(f"-> {SALIDA_CORR}")
