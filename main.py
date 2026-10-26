"""Ejecuta los 5 ejercicios, crea datos CSV, graficas PNG y reporte PDF.

Uso (desde la carpeta del proyecto): python main.py
Los resultados de tiempos se miden en el equipo donde se ejecuta.
"""
import csv
import json
import os
import random
import statistics
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from algoritmos import (
    pi_worker, mochila_voraz, puntos_aleatorios, matriz_distancias,
    vecino_mas_cercano, dos_opt, costo_ruta, recocido_simulado,
    mst_preorden, tsp_exacto_held_karp
)
from graficas import crear_graficas
from reporte import generar_reporte

BASE = Path(__file__).resolve().parent
DATOS = BASE / 'resultados'
FIGURAS = BASE / 'graficas'


def guardar_csv(nombre, filas):
    if not filas:
        return
    with (DATOS / nombre).open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=list(filas[0]))
        writer.writeheader()
        writer.writerows(filas)


def promedio(valores):
    return statistics.mean(valores)


def ejecutar_pi():
    """Numero total fijo de muestras en todos los escenarios (comparacion fuerte)."""
    muestras_total = int(os.getenv('PI_MUESTRAS', '3000000'))
    repeticiones = int(os.getenv('PI_REPETICIONES', '3'))
    filas = []
    print('  E1: estimacion pi con 1, 2, 4, 8 procesos...')
    for procesos in (1, 2, 4, 8):
        for repeticion in range(repeticiones):
            partes = [muestras_total // procesos] * procesos
            for k in range(muestras_total % procesos):
                partes[k] += 1
            argumentos = [(cantidad, 1000 + 100*repeticion + k)
                          for k, cantidad in enumerate(partes)]
            inicio = time.perf_counter()
            if procesos == 1:
                dentro = pi_worker(argumentos[0])
            else:
                with ProcessPoolExecutor(max_workers=procesos) as ejecutor:
                    dentro = sum(ejecutor.map(pi_worker, argumentos))
            tiempo = time.perf_counter() - inicio
            filas.append({'procesos': procesos, 'repeticion': repeticion+1,
                          'segundos': round(tiempo, 6),
                          'pi_estimado': round(4*dentro/muestras_total, 8),
                          'muestras': muestras_total})
        print(f'       {procesos} procesos listos')
    resumen = []
    t1 = statistics.median(x['segundos'] for x in filas if x['procesos'] == 1)
    for procesos in (1,2,4,8):
        mediana = statistics.median(x['segundos'] for x in filas if x['procesos'] == procesos)
        resumen.append({'procesos': procesos, 'mediana_s': round(mediana, 6),
                        'speedup': round(t1/mediana, 4), 'speedup_ideal': procesos,
                        'eficiencia': round(t1/mediana/procesos, 4)})
    guardar_csv('ej1_tiempos.csv', filas)
    guardar_csv('ej1_speedup.csv', resumen)
    return {'muestras': muestras_total, 'repeticiones': repeticiones,
            'ensayos': filas, 'resumen': resumen}


def ejecutar_mochila():
    print('  E2: mochila voraz...')
    objetos = [{'nombre':'A', 'peso':2, 'valor':2},
               {'nombre':'B', 'peso':4, 'valor':8},
               {'nombre':'C', 'peso':6, 'valor':18}]
    capacidad = 10
    resultados = {
        'peso': mochila_voraz(objetos, capacidad, 'peso'),
        'densidad': mochila_voraz(objetos, capacidad, 'densidad'),
    }
    guardar_csv('ej2_objetos.csv', [dict(obj, densidad=round(obj['valor']/obj['peso'], 3))
                                     for obj in objetos])
    guardar_csv('ej2_comparacion.csv', [
        {'metodo': etiqueta, 'objetos': ', '.join(r['nombres']),
         'capacidad_usada': r['peso'], 'valor_total': r['valor']}
        for etiqueta, r in resultados.items()
    ])
    return {'objetos': objetos, 'capacidad': capacidad, 'metodos': resultados}


def ejecutar_busqueda_local():
    print('  E3: 2-opt: aleatorio vs vecino mas cercano...')
    n, repeticiones = 25, 40
    puntos = puntos_aleatorios(n, random.Random(20261025))
    dist = matriz_distancias(puntos)
    filas, ejemplo = [], {}
    for r in range(repeticiones):
        rng = random.Random(3700+r)
        ruta_random = rng.sample(range(n), n)
        inicio_nn = rng.randrange(n)
        ruta_nn = vecino_mas_cercano(dist, inicio_nn)
        ran = dos_opt(ruta_random, dist, registrar=(r==0))
        nn = dos_opt(ruta_nn, dist, registrar=(r==0))
        filas.append({'ensayo': r+1, 'aleatoria_mejoras':ran['mejoras'],
                      'vecino_mejoras':nn['mejoras'],
                      'aleatoria_inicial':round(costo_ruta(ruta_random,dist), 6),
                      'vecino_inicial':round(costo_ruta(ruta_nn,dist), 6),
                      'aleatoria_final':round(ran['costo'], 6),
                      'vecino_final':round(nn['costo'], 6)})
        if r == 0:
            ejemplo = {'aleatoria': ran['historial'], 'vecino': nn['historial']}
    guardar_csv('ej3_comparacion.csv', filas)
    return {'ciudades': n, 'repeticiones': repeticiones, 'filas':filas,
            'historial_ejemplo':ejemplo,
            'resumen':{
                'mejoras_aleatoria':promedio(x['aleatoria_mejoras'] for x in filas),
                'mejoras_vecino':promedio(x['vecino_mejoras'] for x in filas),
                'costo_aleatoria':promedio(x['aleatoria_final'] for x in filas),
                'costo_vecino':promedio(x['vecino_final'] for x in filas),
                'costo_inicial_aleatoria':promedio(x['aleatoria_inicial'] for x in filas),
                'costo_inicial_vecino':promedio(x['vecino_inicial'] for x in filas),
            }}


def ejecutar_recocido():
    print('  E4: recocido simulado: enfriamiento lineal y exponencial...')
    n, repeticiones, iteraciones = 25, 25, 4500
    dist = matriz_distancias(puntos_aleatorios(n, random.Random(20261025)))
    filas, historiales = [], {}
    for r in range(repeticiones):
        ruta = random.Random(6000+r).sample(range(n), n)
        for esquema in ('lineal', 'exponencial'):
            inicio = time.perf_counter()
            result = recocido_simulado(ruta, dist, esquema=esquema,
                                       iteraciones=iteraciones,
                                       temp_inicial=40, temp_final=0.1,
                                       semilla=10000+r, registrar=(r==0))
            duracion = time.perf_counter()-inicio
            filas.append({'ensayo':r+1, 'enfriamiento':esquema,
                          'costo_inicial':round(result['inicial'],6),
                          'costo_final':round(result['costo'],6),
                          'segundos':round(duracion,6)})
            if r==0:
                historiales[esquema] = result['historial']
    guardar_csv('ej4_recocido.csv', filas)
    guardar_csv('ej4_convergencia.csv', [
        {'esquema': esq, 'iteracion':fila[0],
         'mejor_costo':round(fila[1],6), 'temperatura':round(fila[2],6)}
        for esq, hist in historiales.items() for fila in hist
    ])
    return {'ciudades':n, 'repeticiones':repeticiones, 'iteraciones':iteraciones,
            'filas':filas, 'historiales':historiales,
            'resumen':{
                esq: {'costo':promedio(x['costo_final'] for x in filas if x['enfriamiento']==esq),
                      'segundos':promedio(x['segundos'] for x in filas if x['enfriamiento']==esq),
                      'desv_costo':statistics.stdev(x['costo_final'] for x in filas if x['enfriamiento']==esq)}
                for esq in ('lineal','exponencial')
            }}


def ejecutar_mst():
    print('  E5: 100 instancias, TSP exacto, MST y comparaciones...')
    n, repeticiones = 9, 100
    filas = []
    for r in range(repeticiones):
        dist = matriz_distancias(puntos_aleatorios(n, random.Random(900000+r)))
        opt = tsp_exacto_held_karp(dist)
        inicial_mst = mst_preorden(dist)
        mst = costo_ruta(inicial_mst,dist)
        post = dos_opt(inicial_mst,dist)['costo']
        ruta_ran = random.Random(30000+r).sample(range(n), n)
        ruta_nn = vecino_mas_cercano(dist, random.Random(40000+r).randrange(n))
        local_ran = dos_opt(ruta_ran,dist)['costo']
        local_nn = dos_opt(ruta_nn,dist)['costo']
        sa_lin = recocido_simulado(ruta_ran, dist, 'lineal', 2500, 40, 0.1, 50000+r)['costo']
        sa_exp = recocido_simulado(ruta_ran, dist, 'exponencial', 2500, 40, 0.1, 50000+r)['costo']
        costos = {'optimo_exacto':opt, 'mst':mst, 'mst_2opt':post,
                  'local_aleatoria':local_ran, 'local_vecino':local_nn,
                  'recocido_lineal':sa_lin, 'recocido_exponencial':sa_exp}
        fila = {'instancia':r+1, **{k:round(v,6) for k,v in costos.items()},
                **{'razon_'+k:round(v/opt,6) for k,v in costos.items() if k!='optimo_exacto'}}
        filas.append(fila)
        assert opt <= min(costos.values()) + 1e-7, 'Optimo exacto incongruente'
        assert mst <= 2*opt+1e-8, 'Violacion del limite teorico MST'
        assert post <= mst+1e-8, '2-opt empeoro MST'
    guardar_csv('ej5_100_instancias.csv', filas)
    claves = ['mst','mst_2opt','local_aleatoria','local_vecino','recocido_lineal','recocido_exponencial']
    resumen = {k:{'media_costo':promedio(x[k] for x in filas),
                  'media_razon':promedio(x['razon_'+k] for x in filas),
                  'max_razon':max(x['razon_'+k] for x in filas)} for k in claves}
    return {'ciudades':n,'instancias':repeticiones,'filas':filas,'resumen':resumen}


def main():
    print('\n=== PROYECTO: EXPERIMENTOS DE ALGORITMOS ===')
    DATOS.mkdir(exist_ok=True)
    FIGURAS.mkdir(exist_ok=True)
    inicio = time.perf_counter()
    resultados = {
        'ej1': ejecutar_pi(),
        'ej2': ejecutar_mochila(),
        'ej3': ejecutar_busqueda_local(),
        'ej4': ejecutar_recocido(),
        'ej5': ejecutar_mst(),
    }
    (DATOS/'resumen_completo.json').write_text(json.dumps(resultados,ensure_ascii=False,indent=2),encoding='utf-8')
    print('  Creando graficas...')
    crear_graficas(resultados, FIGURAS)
    print('  Redactando reporte_final.pdf con los datos calculados...')
    metadata = json.loads((BASE/'datos_entrega.json').read_text(encoding='utf-8'))
    generar_reporte(resultados, metadata, BASE/'reporte_final.pdf', FIGURAS)
    print(f'\nLISTO. Tiempo total: {time.perf_counter()-inicio:.1f} segundos')
    print('Reporte: reporte_final.pdf')
    print('Graficas: graficas/ (9 archivos PNG)')
    print('Datos: resultados/ (archivos CSV y JSON)')
    print('Revisa datos_entrega.json para agregar nombre, GitHub y video.\n')


if __name__ == '__main__':
    # Imprescindible para multiprocessing en Windows.
    main()
