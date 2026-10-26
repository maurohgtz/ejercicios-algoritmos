# Guion breve para el video (máximo 8 minutos)

**00:00-00:35 | Introducción.** "Este proyecto implementa cinco experimentos sobre análisis de algoritmos. Se ejecuta en Python y produce un reporte PDF, nueve gráficas y datos CSV."

**00:35-01:20 | Ejecución real.** Mostrar VS Code con la carpeta abierta. Ejecutar `py -m unittest discover -s tests -v` y luego `py main.py`. Se pueden comentar los archivos mientras termina. No afirmar que se ejecutó si no se mostró corriendo.

**01:20-02:10 | Ejercicio 1.** Abrir `graficas/01_speedup.png` y `resultados/ej1_speedup.csv`. "Uso 1, 2, 4 y 8 procesos, manteniendo el trabajo total. El speedup real es T1/Tp. La línea diagonal es el ideal. Los costos de gestión y Amdahl explican las diferencias."

**02:10-02:55 | Ejercicio 2.** Abrir `graficas/02_mochila.png`. "Con capacidad diez, elegir por menor peso deja valor diez; por valor/peso obtiene veintiséis. El ejemplo demuestra que elegir primero objetos ligeros puede ser peor."

**02:55-04:00 | Ejercicio 3.** Abrir `graficas/03_dos_opt_mejoras.png` y `04_dos_opt_calidad.png`. Leer en el reporte cuántas mejoras promedio se obtuvieron y qué método alcanzó el menor costo. "2-opt invierte segmentos mientras mejoran la distancia; compara inicio aleatorio con vecino más cercano. Óptimo local no significa global."

**04:00-05:15 | Ejercicio 4.** Abrir `graficas/05_recocido_convergencia.png` y `06_recocido_tiempo_calidad.png`. "Comparé enfriamiento lineal y exponencial. El recocido acepta ocasionalmente movimientos peores para explorar rutas. Muestro costos, temperaturas y tiempo por ejecución."

**05:15-06:40 | Ejercicio 5.** Abrir `graficas/07_mst_razon_histograma.png`, `08_mst_comparacion_costos.png` y `09_mst_comparacion_razones.png`. "Se probaron cien instancias de nueve ciudades y el óptimo exacto con Held-Karp. MST preorden tiene razón menor o igual a dos para TSP métrico. 2-opt mejora o mantiene esa ruta y se compara con búsqueda local y recocido."

**06:40-07:20 | Entrega y cierre.** Abrir `reporte_final.pdf` y el repositorio público en navegador. Explicar que los CSV y gráficos son reproducibles y mostrar el enlace del video en el PDF si ya está disponible. Terminar antes de 8 minutos.

**IMPORTANTE:** Las medidas numéricas cambian según el equipo; leer las de tu `reporte_final.pdf`. No recitar una cifra del guion sin verificarla.
