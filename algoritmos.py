"""Algoritmos de los cinco ejercicios. Python 3.10+; no hay datos inventados.

TSP euclidiano simetrico, ciclos Hamiltonianos cerrados (se incluye regreso a origen).
"""
import math
import random
from functools import lru_cache


def pi_worker(argumentos):
    muestras, semilla = argumentos
    rng = random.Random(semilla)
    dentro = 0
    for _ in range(muestras):
        x, y = rng.random(), rng.random()
        if x*x + y*y <= 1.0:
            dentro += 1
    return dentro


def mochila_voraz(objetos, capacidad, criterio):
    """Mochila 0/1: los objetos NO se fraccionan.

    objetos: listas de dicts con 'nombre','peso','valor'
    criterio: 'peso' o 'densidad'
    """
    if criterio == 'peso':
        ordenados = sorted(objetos, key=lambda a: (a['peso'], -a['valor'], a['nombre']))
    elif criterio == 'densidad':
        ordenados = sorted(objetos, key=lambda a: (-a['valor']/a['peso'], a['peso'], a['nombre']))
    else:
        raise ValueError('Criterio desconocido')
    seleccion = []
    disponible = capacidad
    for obj in ordenados:
        if obj['peso'] <= disponible:
            seleccion.append(obj)
            disponible -= obj['peso']
    return {
        'nombres': [x['nombre'] for x in seleccion],
        'peso': sum(x['peso'] for x in seleccion),
        'valor': sum(x['valor'] for x in seleccion),
    }


def puntos_aleatorios(n, rng, limite=100):
    return [(rng.uniform(0, limite), rng.uniform(0, limite)) for _ in range(n)]


def matriz_distancias(puntos):
    return [[math.hypot(x1-x2, y1-y2) for x2, y2 in puntos] for x1, y1 in puntos]


def costo_ruta(ruta, dist):
    return sum(dist[ruta[k]][ruta[(k+1) % len(ruta)]] for k in range(len(ruta)))


def vecino_mas_cercano(dist, inicio):
    n = len(dist)
    ruta = [inicio]
    disponibles = set(range(n)) - {inicio}
    while disponibles:
        sig = min(disponibles, key=lambda ciudad: (dist[ruta[-1]][ciudad], ciudad))
        ruta.append(sig)
        disponibles.remove(sig)
    return ruta


def delta_2opt(ruta, dist, i, j):
    """Cambia aristas (i,i+1), (j,j+1). Revierte ruta[i+1:j+1]."""
    a, b = ruta[i], ruta[i+1]
    c, d = ruta[j], ruta[(j+1) % len(ruta)]
    return dist[a][c] + dist[b][d] - dist[a][b] - dist[c][d]


def dos_opt(ruta_inicial, dist, registrar=False):
    """Descenso local de mejor mejora. Devuelve ruta, costo, cantidad de mejoras, historial."""
    ruta = list(ruta_inicial)
    n = len(ruta)
    costo = costo_ruta(ruta, dist)
    historial = [costo]
    mejoras = 0
    while True:
        mejor_delta, mejor_par = -1e-10, None
        for i in range(n-2):
            for j in range(i+2, n):
                if i == 0 and j == n-1:
                    continue  # enlaces adyacentes en el ciclo
                delta = delta_2opt(ruta, dist, i, j)
                if delta < mejor_delta:
                    mejor_delta, mejor_par = delta, (i, j)
        if mejor_par is None:
            break
        i, j = mejor_par
        ruta[i+1:j+1] = reversed(ruta[i+1:j+1])
        costo += mejor_delta
        mejoras += 1
        if registrar:
            historial.append(costo)
    costo = costo_ruta(ruta, dist)  # evita errores acumulados de redondeo
    if registrar:
        historial[-1] = costo
    else:
        historial = []
    return {'ruta': ruta, 'costo': costo, 'mejoras': mejoras, 'historial': historial}


def recocido_simulado(ruta_inicial, dist, esquema='exponencial', iteraciones=4000,
                      temp_inicial=40.0, temp_final=0.1, semilla=0, registrar=False):
    """Annealing con vecinos 2-opt. Se entrega la MEJOR solución visitada."""
    if esquema not in ('lineal', 'exponencial'):
        raise ValueError('Esquema desconocido')
    if iteraciones < 2 or temp_inicial <= temp_final or temp_final <= 0:
        raise ValueError('Parametros de temperatura/iteraciones incorrectos')
    rng = random.Random(semilla)
    ruta = list(ruta_inicial)
    n = len(ruta)
    costo = costo_ruta(ruta, dist)
    mejor_costo = costo
    mejor_ruta = list(ruta)
    trace = [(0, mejor_costo, temp_inicial)] if registrar else []
    for t in range(iteraciones):
        fraccion = t/(iteraciones-1)
        if esquema == 'lineal':
            temperatura = temp_inicial + (temp_final - temp_inicial)*fraccion
        else:
            temperatura = temp_inicial*(temp_final/temp_inicial)**fraccion
        i = rng.randrange(0, n-2)
        j = rng.randrange(i+2, n)
        if i == 0 and j == n-1:
            # Esta pareja cortaria aristas adyacentes en el ciclo.
            continue
        delta = delta_2opt(ruta, dist, i, j)
        if delta < 0 or rng.random() < math.exp(-delta/temperatura):
            ruta[i+1:j+1] = reversed(ruta[i+1:j+1])
            costo += delta
            if costo < mejor_costo - 1e-10:
                mejor_costo = costo
                mejor_ruta = list(ruta)
        if registrar and (t+1) % 25 == 0:
            trace.append((t+1, mejor_costo, temperatura))
    return {'ruta': mejor_ruta, 'costo': costo_ruta(mejor_ruta, dist),
            'historial': trace, 'inicial': costo_ruta(ruta_inicial, dist)}


def mst_preorden(dist):
    """Prim + recorrido preorden + atajos: aproximacion 2 para TSP metrico."""
    n = len(dist)
    en_arbol = [False]*n
    padre = [-1]*n
    menor = [float('inf')]*n
    menor[0] = 0.0
    for _ in range(n):
        u = min((x for x in range(n) if not en_arbol[x]), key=lambda x: menor[x])
        en_arbol[u] = True
        for v in range(n):
            if not en_arbol[v] and dist[u][v] < menor[v]:
                menor[v] = dist[u][v]
                padre[v] = u
    hijos = [[] for _ in range(n)]
    for v in range(1, n):
        hijos[padre[v]].append(v)
    for h in hijos:
        h.sort()
    ruta, pila = [], [0]
    while pila:
        u = pila.pop()
        ruta.append(u)
        pila.extend(reversed(hijos[u]))
    return ruta


def tsp_exacto_held_karp(dist):
    """Programacion dinamica Held-Karp O(n^2*2^n), inicio 0 y regreso 0."""
    n = len(dist)
    if n < 2:
        return 0.0
    @lru_cache(None)
    def visita(actual, restantes):
        if restantes == 0:
            return dist[actual][0]
        mejor = float('inf')
        for sig in range(1, n):
            bit = 1 << (sig-1)
            if restantes & bit:
                mejor = min(mejor, dist[actual][sig] + visita(sig, restantes ^ bit))
        return mejor
    return visita(0, (1 << (n-1))-1)
