"""Generación del dataset sintético ENEMDU."""
import numpy as np
import pandas as pd


def generar_enemdu(n=4000, semilla=2026):
    """ENEMDU simplificada y SINTÉTICA (inspirada en la estructura del INEC).
    Los valores son simulados con relaciones realistas; no son datos oficiales."""
    rng = np.random.default_rng(semilla)
    prov = {"Pichincha": ("Sierra", .20), "Guayas": ("Costa", .24), "Azuay": ("Sierra", .06),
            "Manabí": ("Costa", .09), "El Oro": ("Costa", .05), "Tungurahua": ("Sierra", .04),
            "Imbabura": ("Sierra", .04), "Loja": ("Sierra", .04), "Los Ríos": ("Costa", .06),
            "Esmeraldas": ("Costa", .04), "Chimborazo": ("Sierra", .04), "Sucumbíos": ("Amazonía", .03),
            "Orellana": ("Amazonía", .03), "Morona Santiago": ("Amazonía", .03), "Galápagos": ("Insular", .01)}
    nombres = list(prov)
    p = np.array([prov[k][1] for k in nombres]); p = p / p.sum()
    provincia = rng.choice(nombres, n, p=p)
    region = np.array([prov[k][0] for k in provincia])
    area = np.where(rng.random(n) < np.where(region == "Amazonía", .45, .70), "Urbana", "Rural")
    sexo = rng.choice(["Hombre", "Mujer"], n, p=[.53, .47])
    edad = rng.integers(18, 66, n)
    anios_educ = np.clip(rng.normal(10 + 2.5 * (area == "Urbana"), 3.6, n), 0, 22).round()
    horas = np.clip(rng.normal(41, 10, n), 5, 80).round()
    ef_reg = pd.Series(region).map({"Sierra": .06, "Costa": 0, "Amazonía": -.10, "Insular": .35}).values
    log_ing = (5.05 + .075 * anios_educ + .011 * (edad - 18) - .00012 * (edad - 18) ** 2
               + .17 * (sexo == "Hombre") + .20 * (area == "Urbana") + ef_reg
               + .007 * (horas - 40) + rng.normal(0, .5, n))
    ingreso = np.exp(log_ing).round(2)
    adecuado = ((ingreso >= 470) & (horas >= 40)).astype(int)
    ruido = rng.random(n) < .05
    adecuado[ruido] = 1 - adecuado[ruido]
    df = pd.DataFrame({
        "id_persona": [f"P{i:05d}" for i in range(1, n + 1)],
        "provincia": provincia, "region": region, "area": area, "sexo": sexo,
        "edad": edad, "anios_educ": anios_educ, "horas_trabajo": horas,
        "ingreso": ingreso, "empleo_adecuado": adecuado})
    df["nivel_instruccion"] = pd.cut(df["anios_educ"], [-1, 6, 12, 16, 23],
                                     labels=["Primaria", "Secundaria", "Superior", "Posgrado"])
    # Problemas típicos de datos reales
    df.loc[rng.choice(n, int(n * .03), replace=False), "ingreso"] = np.nan
    df.loc[rng.choice(n, int(n * .02), replace=False), "anios_educ"] = np.nan
    atip = rng.choice(n, 12, replace=False)
    df.loc[atip, "ingreso"] = df.loc[atip, "ingreso"] * 15
    df = pd.concat([df, df.sample(25, random_state=semilla)], ignore_index=True)  # duplicados
    return df
