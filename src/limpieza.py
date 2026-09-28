"""Funciones de limpieza y construcción de variables (Parte 2)."""
import numpy as np
import pandas as pd


def limpiar(df: pd.DataFrame, umbral: float = 3.5) -> pd.DataFrame:
    """Quita duplicados, nulos y atípicos extremos de ingreso.

    - Duplicados: filas repetidas por `id_persona` (se conserva la primera).
    - Nulos: filas sin `ingreso` o sin `anios_educ`.
    - Atípicos extremos: z-score robusto (mediana y MAD) sobre log(ingreso),
      eliminando |z| > 3.5 (criterio de Iglewicz y Hoaglin).
      Se usa el log porque el ingreso es asimétrico a la derecha, y mediana/MAD
      porque la media y la desviación estándar se distorsionan con los propios
      atípicos que queremos detectar.
    """
    out = df.drop_duplicates(subset="id_persona", keep="first")
    out = out.dropna(subset=["ingreso", "anios_educ"])
    out = out[out["ingreso"] > 0]

    log_ing = np.log(out["ingreso"])
    mediana = log_ing.median()
    mad = (log_ing - mediana).abs().median() * 1.4826  # escala comparable a la desv. estándar
    z = (log_ing - mediana) / mad
    out = out[z.abs() <= umbral]

    return out.reset_index(drop=True)


def agregar_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Crea `log_ingreso` y `grupo_edad` sin modificar el DataFrame original."""
    out = df.copy()
    out["log_ingreso"] = np.log(out["ingreso"])
    out["grupo_edad"] = pd.cut(out["edad"], bins=[17, 29, 44, 65],
                               labels=["18-29", "30-44", "45-65"])
    return out
