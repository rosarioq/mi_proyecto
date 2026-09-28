# Brechas de ingreso laboral en Ecuador · ENEMDU sintética

## Pregunta de análisis
¿Cómo se relaciona el ingreso laboral con los años de educación, y cuánto cambia
esa relación según sexo, área (urbana/rural) y región, una vez controlada la edad
y las horas trabajadas?

## Fuente de datos
Dataset **sintético** que imita la estructura de la Encuesta Nacional de Empleo,
Desempleo y Subempleo (ENEMDU) del INEC. Se genera con `src/datos.py`
(`generar_enemdu(n=4000, semilla=2026)`). **No son datos oficiales.**
Incluye a propósito nulos, 12 ingresos atípicos (×15) y 25 filas duplicadas.

## Cómo ejecutar
```bash
git clone <url-del-repo> && cd mi_proyecto
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python ejecutar.py            # genera data/crudos/enemdu.csv y data/procesados/enemdu_limpio.csv

cp .env.example .env          # edita la sal secreta
export $(cat .env | xargs)    # Windows PowerShell: $env:LOPDP_SAL="..."
python anonimizar_personal.py # genera data/procesados/enemdu_anonimizada.csv
```
Luego abre `notebooks/01_analisis.ipynb` (requiere `pip install jupyterlab`).

Todo es reproducible: las semillas están fijadas (`semilla=2026` para los datos,
`SEMILLA = 42` para muestreos) y las versiones de librerías, en `requirements.txt`.

## Estructura
```
mi_proyecto/
├── data/
│   ├── crudos/          # datos originales · NO versionados (.gitignore)
│   └── procesados/      # salidas limpias y anonimizadas
├── notebooks/
│   └── 01_analisis.ipynb
├── src/
│   ├── datos.py         # generación del dataset sintético
│   ├── limpieza.py      # limpiar(), agregar_variables()
│   └── anonimizar.py    # seudonimización y generalización (LOPDP)
├── reportes/            # gráficos y tablas finales
├── ejecutar.py          # pipeline crudo → procesado
├── anonimizar_personal.py
├── requirements.txt
├── .env.example         # plantilla de la sal (el .env real no se sube)
└── .gitignore
```

## Protección de datos (LOPDP)
Los datos con identificadores personales solo existen en `data/crudos/`, que no
se sube al repositorio. La versión compartible elimina nombre y fecha de
nacimiento, sustituye la cédula por un seudónimo SHA-256 con sal secreta,
generaliza la edad en rangos de 10 años y redondea el ingreso a la decena.
Ojo: los datos seudonimizados siguen siendo datos personales mientras exista la
sal; ver la sección de limitaciones en el notebook.
