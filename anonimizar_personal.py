"""Ejercicio 5.1: anonimiza la tabla con datos personales antes de compartirla.
Uso:  export LOPDP_SAL="una-sal-larga-y-secreta"  &&  python anonimizar_personal.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

from src.anonimizar import anonimizar, k_anonimato, obtener_sal

SEMILLA = 42
RAIZ = Path(__file__).resolve().parent
CRUDO = RAIZ / "data" / "crudos" / "enemdu.csv"
PERSONAL = RAIZ / "data" / "crudos" / "enemdu_personal.csv"           # NO se sube a Git
SALIDA = RAIZ / "data" / "procesados" / "enemdu_anonimizada.csv"


def simular_datos_personales(df: pd.DataFrame) -> pd.DataFrame:
    """Reproduce la tabla con datos personales FICTICIOS del enunciado."""
    rng = np.random.default_rng(SEMILLA)
    personal = df.drop_duplicates("id_persona").head(1500).copy()
    personal["cedula"] = [f"{rng.integers(1, 25):02d}{rng.integers(0, 10**8):08d}" for _ in range(len(personal))]
    personal["nombre"] = rng.choice(["Ana", "Luis", "María", "Jorge", "Carla", "Diego", "Sofía", "Pablo"], len(personal)) + " " + \
                         rng.choice(["Pérez", "Guerrero", "Andrade", "Zambrano", "Vera", "Mora", "Salazar"], len(personal))
    personal["fecha_nac"] = pd.to_datetime("2026-01-01") - pd.to_timedelta(
        personal["edad"] * 365 + rng.integers(0, 365, len(personal)), unit="D")
    return personal


def main():
    sal = obtener_sal()
    personal = simular_datos_personales(pd.read_csv(CRUDO))
    personal.to_csv(PERSONAL, index=False)

    anon = anonimizar(personal, sal)
    anon.to_csv(SALIDA, index=False)

    print(anon[["id_seudonimo", "provincia", "edad", "ingreso"]].head())
    print(f"\nColumnas finales: {list(anon.columns)}")
    print(f"k-anonimato (provincia, edad, sexo): {k_anonimato(anon, ['provincia', 'edad', 'sexo'])}")
    print(f"Guardado en {SALIDA.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
