"""Pipeline completo: crudo -> procesado. Uso: python ejecutar.py"""
from pathlib import Path

import pandas as pd

from src.datos import generar_enemdu
from src.limpieza import limpiar, agregar_variables

RAIZ = Path(__file__).resolve().parent
CRUDO = RAIZ / "data" / "crudos" / "enemdu.csv"
PROCESADO = RAIZ / "data" / "procesados" / "enemdu_limpio.csv"


def main():
    # Ejercicio 1.1: guardar el crudo (solo si no existe)
    if not CRUDO.exists():
        CRUDO.parent.mkdir(parents=True, exist_ok=True)
        generar_enemdu().to_csv(CRUDO, index=False)
        print(f"Crudo guardado en {CRUDO.relative_to(RAIZ)}")

    # Ejercicio 2.2: cargar, limpiar, agregar variables y guardar
    crudo = pd.read_csv(CRUDO)
    limpio = agregar_variables(limpiar(crudo))
    PROCESADO.parent.mkdir(parents=True, exist_ok=True)
    limpio.to_csv(PROCESADO, index=False)
    print(f"Filas: {len(crudo)} crudas -> {len(limpio)} limpias")
    print(f"Procesado guardado en {PROCESADO.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
