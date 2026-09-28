# Brechas de ingreso laboral en Ecuador · ENEMDU sintética

## Pregunta de análisis
¿Cómo se relaciona el ingreso laboral con los años de educación, y cuánto cambia
esa relación según sexo, área (urbana/rural) y región, una vez controladas la edad
y las horas trabajadas?

## Fuente de datos
Dataset **sintético** que imita la estructura de la Encuesta Nacional de Empleo,
Desempleo y Subempleo (ENEMDU) del INEC. Se genera con `src/datos.py`
(`generar_enemdu(n=4000, semilla=2026)`). **No son datos oficiales.**
Incluye a propósito nulos, 12 ingresos atípicos (×15) y 25 filas duplicadas.

## Requisitos
- Python 3.11 o superior (`numpy 2.4.4` y `pandas 3.0.2` no se instalan en versiones anteriores)
- Git
- Opcional: VS Code con las extensiones de Python y Jupyter

## Cómo ejecutar

### Windows (PowerShell / terminal de VS Code)
Abre la carpeta `mi_proyecto` en VS Code (**Archivo → Abrir carpeta**) y luego
abre la terminal (**Terminal → Nuevo terminal**). Si `python` no responde o abre
la Microsoft Store, usa `py` en su lugar.

```powershell
# 1. Entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1
# Si aparece "la ejecución de scripts está deshabilitada", ejecuta una vez:
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 2. Dependencias
python -m pip install -r requirements.txt
python -m pip install ipykernel      # para ejecutar el notebook en VS Code

# 3. Pipeline: crudo -> procesado
python ejecutar.py                   # -> data\procesados\enemdu_limpio.csv

# 4. Anonimización (la sal solo vale para esta terminal)
$env:LOPDP_SAL = "tu-sal-secreta"
python anonimizar_personal.py        # -> data\procesados\enemdu_anonimizada.csv
```

### macOS / Linux (bash)
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install ipykernel
python ejecutar.py
export LOPDP_SAL="tu-sal-secreta"
python anonimizar_personal.py
```

### Notebook
Abre `notebooks/01_analisis.ipynb`, selecciona el kernel de `.venv` (arriba a la
derecha, **Select Kernel**) y ejecuta **Run All**. El kernel no hereda la variable
`LOPDP_SAL` de la terminal, así que el notebook pedirá la sal en un cuadro de texto.

### Resultado esperado
```
Filas: 4025 crudas -> 3790 limpias
```

Todo es reproducible: las semillas están fijadas (`semilla=2026` para los datos,
`SEMILLA = 42` para muestreos) y las versiones de las librerías, en `requirements.txt`.

## Estructura
```
mi_proyecto/
├── data/
│   ├── crudos/          # datos originales · NO versionados (.gitignore)
│   └── procesados/      # salidas limpias y anonimizadas
├── notebooks/
│   └── 01_analisis.ipynb
├── src/
│   ├── __init__.py
│   ├── datos.py         # generación del dataset sintético
│   ├── limpieza.py      # limpiar(), agregar_variables()
│   └── anonimizar.py    # seudonimización y generalización (LOPDP)
├── reportes/            # gráficos y tablas finales
├── ejecutar.py          # pipeline crudo → procesado
├── anonimizar_personal.py
├── requirements.txt
├── .env.example         # plantilla de la sal (el .env real no se sube)
├── .gitignore
└── README.md
```

## Control de versiones
Quedan fuera del repositorio (ver `.gitignore`): `data/crudos/`, `.env`,
`.venv/`, `.ipynb_checkpoints/` y `__pycache__/`. Para comprobarlo:

```powershell
git status --ignored
```

En Windows pueden aparecer avisos `LF will be replaced by CRLF`; son normales
y no afectan al proyecto.

## Protección de datos (LOPDP)
Los datos con identificadores personales solo existen en `data/crudos/`, que no
se sube al repositorio. La versión compartible:

1. elimina `nombre` y `fecha_nac` (identificadores directos);
2. sustituye la `cedula` por un seudónimo SHA-256 con sal secreta (12 caracteres);
3. generaliza la `edad` en rangos de 10 años y redondea el `ingreso` a la decena.

**Limitaciones.** Los datos seudonimizados siguen siendo datos personales mientras
exista la sal, por eso esta se guarda fuera del código y del repositorio. Además,
la combinación provincia + rango de edad + sexo deja personas únicas (k-anonimato
= 1), y `id_persona` permite volver a unir la tabla con la original. Antes de
publicar convendría agrupar provincias poco pobladas, suprimir celdas pequeñas
(k ≥ 5) y eliminar `id_persona`.
