"""Seudonimización y generalización de datos personales (Parte 5, LOPDP)."""
import hashlib
import os

import pandas as pd

IDENTIFICADORES_DIRECTOS = ["nombre", "fecha_nac"]


def obtener_sal() -> str:
    """Lee la sal secreta de la variable de entorno LOPDP_SAL.
    La sal nunca se escribe en el código ni se sube a Git."""
    sal = os.environ.get("LOPDP_SAL")
    if not sal:
        raise RuntimeError("Define la variable de entorno LOPDP_SAL con una sal secreta.")
    return sal


def seudonimizar(valor: str, sal: str, largo: int = 12) -> str:
    """SHA-256(sal + valor), truncado a los primeros `largo` caracteres hex."""
    return hashlib.sha256((sal + str(valor)).encode("utf-8")).hexdigest()[:largo]


def rango_edad(edad: int, ancho: int = 10) -> str:
    """Generaliza la edad en rangos de `ancho` años: 34 -> '30-39'."""
    ini = (int(edad) // ancho) * ancho
    return f"{ini}-{ini + ancho - 1}"


def anonimizar(df: pd.DataFrame, sal: str) -> pd.DataFrame:
    out = df.copy()
    # 1. Eliminar identificadores directos
    out = out.drop(columns=IDENTIFICADORES_DIRECTOS)
    # 2. Cédula -> seudónimo (se inserta como primera columna)
    out.insert(0, "id_seudonimo", out["cedula"].map(lambda c: seudonimizar(c, sal)))
    out = out.drop(columns="cedula")
    # 3. Generalizar edad y redondear ingreso a la decena
    out["edad"] = out["edad"].map(rango_edad)
    out["ingreso"] = out["ingreso"].round(-1)
    return out


def k_anonimato(df: pd.DataFrame, cuasi_identificadores: list) -> int:
    """Tamaño del grupo más pequeño que comparte la misma combinación de
    cuasi-identificadores. k=1 significa que hay al menos una persona única."""
    return int(df.groupby(cuasi_identificadores, observed=True).size().min())
