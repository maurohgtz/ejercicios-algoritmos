# Ejercicios - Experimentos de algoritmos

Proyecto en Python que implementa los **5 ejercicios** solicitados, genera **9 gráficas**, tablas CSV y un **reporte final PDF** con resultados medidos.

## Requisitos

- Windows, macOS o Linux.
- Python 3.10 o superior; para Windows se recomienda Python 3.11 o 3.12.
- Conexión a internet *solo para instalar las dependencias* por primera vez.

## Ejecutar en Windows (VS Code)

1. Extraer el ZIP completo y abrir **la carpeta `Proyecto_Algoritmos`** con `Archivo > Abrir carpeta` en VS Code.
2. Abrir `Terminal > Nuevo terminal`.
3. Ejecutar los siguientes comandos (uno a la vez):

```powershell
py -m pip install -r requirements.txt
py -m unittest discover -s tests -v
py main.py
```

Si el comando `py` no existe, reemplazarlo por `python` en los tres comandos.

Si Windows solicita permisos para procesos, permitir la ejecución de Python. `main.py` está protegido por `if __name__ == '__main__'`, necesario en Windows para procesamiento paralelo.

Al terminar, se crean/sobrescriben:

- `reporte_final.pdf`: reporte escrito automáticamente con datos medidos.
- `graficas/`: nueve gráficas PNG.
- `resultados/`: ocho archivos CSV y `resumen_completo.json`.

La ejecución puede tardar algunos segundos o minutos según la computadora; no cerrar la terminal hasta ver `LISTO`.

### Poner tus datos antes de entregar

Abrir `datos_entrega.json` y modificar únicamente los textos entre comillas:

```json
{
  "nombre": "TU NOMBRE COMPLETO",
  "materia": "NOMBRE DE LA MATERIA",
  "repositorio_url": "https://github.com/TU_USUARIO/TU_REPOSITORIO",
  "video_url": "https://youtu.be/ENLACE_DE_TU_VIDEO"
}
```

Guardar y repetir `py main.py` para que los enlaces aparezcan en `reporte_final.pdf`. **Los tiempos se vuelven a medir cada vez que se ejecuta.** Puedes evitar repetir experimentos utilizando el script `actualizar_reporte.py` que solo regenera el PDF:

```powershell
py actualizar_reporte.py
```

También puede abrirse el archivo `reporte_final.pdf` generado previamente para verificar que todo esté correctamente escrito.

## Estructura del repositorio

```text
Proyecto_Algoritmos/
├── README.md
├── requirements.txt
├── datos_entrega.json
├── main.py
├── algoritmos.py
├── graficas.py
├── reporte.py
├── actualizar_reporte.py
├── guion_video.md
├── reporte_final.pdf
├── tests/
│   └── test_algoritmos.py
├── graficas/
│   ├── 01_speedup.png
│   ├── ...
│   └── 09_mst_comparacion_razones.png
└── resultados/
    ├── ej1_tiempos.csv
    ├── ...
    └── resumen_completo.json
```

> En la captura de la tarea se menciona una "estructura exacta", pero no aparece el árbol de directorios que se debe seguir. Esta es una estructura completa y organizada de reemplazo. Si tu profesor publicó otra estructura en otro lugar, ajusta los directorios antes de subir.

## Resumen de los algoritmos

1. **Estimación de π (Monte Carlo)**: mismo número total de puntos, 1/2/4/8 procesos con `ProcessPoolExecutor`, tres repeticiones y tiempos medianos para speedup medido e ideal. La misma carga total permite una comparación fuerte.
2. **Mochila voraz 0/1**: compara menor peso con mayor valor/peso; el caso de capacidad 10 da valor 10 vs 26 respectivamente.
3. **TSP 2-opt**: 40 ensayos sobre 25 ciudades, comparando rutas iniciales aleatorias y construidas por vecino más cercano, siempre hasta el óptimo local por mejor mejora.
4. **Recocido simulado**: 25 repeticiones por calendario lineal/exponencial sobre 25 ciudades; operadores 2-opt, temperaturas 40 a 0.1, 4500 iteraciones, calidad final y tiempos reales.
5. **Aproximación MST**: 100 instancias independientes de 9 ciudades, algoritmo Prim + preorden; óptimo global exacto Held-Karp; ratio y límite de 2, comparación con MST + 2-opt, búsquedas locales y recocido.

## Detalles importantes de rigor

- Todas las ciudades usan distancias **euclidianas**, por lo que rige la desigualdad triangular y la cota teórica de 2.
- Los resultados de los dos últimos ejercicios incluyen un circuito **cerrado** (se vuelve al punto de partida).
- Todas las heurísticas devuelven un recorrido que contiene cada ciudad una sola vez.
- Un **óptimo local 2-opt no implica óptimo global**.
- Los tiempos varían con la computadora. El reporte se genera con los resultados que realmente obtiene esa ejecución.
- Las pruebas incluidas verifican la propiedad de aproximación MST, una instancia de cuadrado de TSP exacto, mochila y las garantías de no empeorar para 2-opt y SA.

## Entrega

Publicar el repositorio de GitHub/GitLab y pegar su URL en el reporte. Grabar un video de hasta ocho minutos ejecutando `py main.py`, demostrando las gráficas y explicando los resultados. **No basta con subir un archivo ZIP como único contenido del repositorio**: los archivos deben verse individualmente. Seguir `guion_video.md` para la grabación.

## Subir a GitHub paso a paso

1. Crear un repositorio **Public** llamado, por ejemplo, `ejercicios-algoritmos` desde `https://github.com/new`. No activar `Add a README file`, `.gitignore` ni licencia al crearlo (el proyecto ya los tiene).
2. En la terminal abierta en la carpeta del proyecto, ejecutar estos comandos uno por uno (necesitas Git instalado):

```powershell
git --version
git init
git branch -M main
git add .
git commit -m "Proyecto de algoritmos"
git remote add origin https://github.com/TU_USUARIO/ejercicios-algoritmos.git
git push -u origin main
```

**Modificar** `TU_USUARIO` por tu usuario real de GitHub y usar la URL que copiaste del repositorio recién creado. Si Git solicita inicio de sesión, completar la autenticación oficial en el navegador.

3. Verificar que el repositorio muestra `main.py`, `README.md`, carpetas `graficas` y `resultados` y `reporte_final.pdf`. Copiar la URL pública.
4. Grabar y subir el video (por ejemplo, YouTube "Oculto" o Google Drive con acceso por enlace). Probar la URL desde una ventana de incógnito.
5. Actualizar `datos_entrega.json` con el nombre, GitHub y video; guardar y ejecutar:

```powershell
py actualizar_reporte.py
git add datos_entrega.json reporte_final.pdf
git commit -m "Agregar enlaces de entrega"
git push
```

De esta forma el reporte público contiene ambos enlaces definitivos.

> Si `git` no está instalado, instalar **Git for Windows** desde https://git-scm.com/downloads/win o usar GitHub Desktop; también es posible subir archivos desde la interfaz web, pero el flujo anterior preserva mejor las carpetas.
