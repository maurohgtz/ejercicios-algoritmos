Experimentos de análisis de algoritmos
Implementación en Python de cinco experimentos sobre paralelismo, algoritmos voraces y heurísticas para el problema del agente viajero (TSP). El proyecto incluye código fuente, pruebas, datos en formato CSV, visualizaciones y un reporte de resultados en PDF.
Requisitos
- Python 3.10 o superior.
- Dependencias indicadas en requirements.txt.
Ejecución
Desde la carpeta raíz del proyecto, instalar las dependencias:
py -m pip install -r requirements.txt
Ejecutar las pruebas y los experimentos:
py -m unittest discover -s tests -v
py main.py
En sistemas donde no esté disponible el comando py, utilizar python.

Al finalizar se actualizan el reporte reporte_final.pdf, las gráficas de graficas/ y los resultados numéricos de resultados/. Para regenerar únicamente el PDF a partir de los resultados existentes:
py actualizar_reporte.py
Experimentos
Ejercicio	Algoritmo	Evaluación
1	Estimación de π mediante Monte Carlo	Aceleración con 1, 2, 4 y 8 procesos frente al speedup ideal.
2	Mochila 0/1 con selección voraz	Comparación de menor peso y mayor relación valor/peso.
3	Búsqueda local 2-opt para TSP	Número de mejoras y costo final usando inicios aleatorios y por vecino más cercano.
4	Recocido simulado para TSP	Enfriamiento lineal y exponencial: convergencia, costo final y tiempo.
5	Aproximación para TSP basada en MST	Razón de aproximación en 100 instancias de 9 ciudades y efecto del postprocesamiento con 2-opt.


En el ejercicio 5 se obtiene el costo óptimo con el algoritmo exacto Held-Karp, para utilizarlo como referencia en la razón de aproximación. Las distancias del TSP son euclidianas y las rutas incluyen el regreso a la ciudad inicial.
Organización
Proyecto_Algoritmos/
├── README.md
├── requirements.txt
├── datos_entrega.json
├── main.py
├── algoritmos.py
├── graficas.py
├── reporte.py
├── actualizar_reporte.py
├── reporte_final.pdf
├── tests/
│   └── test_algoritmos.py
├── graficas/
│   ├── 01_speedup.png
│   ├── 02_mochila.png
│   ├── 03_dos_opt_mejoras.png
│   ├── 04_dos_opt_calidad.png
│   ├── 05_recocido_convergencia.png
│   ├── 06_recocido_tiempo_calidad.png
│   ├── 07_mst_razon_histograma.png
│   ├── 08_mst_comparacion_costos.png
│   └── 09_mst_comparacion_razones.png
└── resultados/
    ├── ej1_tiempos.csv
    ├── ej1_speedup.csv
    ├── ej2_objetos.csv
    ├── ej2_comparacion.csv
    ├── ej3_comparacion.csv
    ├── ej4_recocido.csv
    ├── ej4_convergencia.csv
    ├── ej5_100_instancias.csv
    └── resumen_completo.json
Notas metodológicas
- Las semillas pseudoaleatorias son fijas para facilitar la reproducción de los experimentos.
- Los tiempos se obtienen con time.perf_counter() y dependen del equipo y de la carga del sistema.
- En la comparación de paralelismo se mantiene constante la cantidad total de muestras.
- La búsqueda 2-opt se detiene en un óptimo local, que no necesariamente coincide con el óptimo global.
- La garantía teórica de aproximación 2 para el recorrido derivado del MST depende de que las distancias satisfagan la desigualdad triangular.
Las tablas completas están en resultados/ y la interpretación de cada experimento se encuentra en reporte_final.pdf.