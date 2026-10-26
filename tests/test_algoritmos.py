import unittest
import random
from algoritmos import (
    mochila_voraz, matriz_distancias, costo_ruta, dos_opt,
    recocido_simulado, mst_preorden, tsp_exacto_held_karp,
    vecino_mas_cercano, puntos_aleatorios
)

class TestAlgoritmos(unittest.TestCase):
    def test_mochila_ejemplo(self):
        objetos = [{'nombre':'A','peso':2,'valor':2}, {'nombre':'B','peso':4,'valor':8},
                   {'nombre':'C','peso':6,'valor':18}]
        self.assertEqual(mochila_voraz(objetos, 10, 'peso')['valor'], 10)
        self.assertEqual(mochila_voraz(objetos, 10, 'densidad')['valor'], 26)

    def test_tsp_cuadrado(self):
        d = matriz_distancias([(0,0),(1,0),(1,1),(0,1)])
        self.assertAlmostEqual(tsp_exacto_held_karp(d), 4)
        self.assertAlmostEqual(costo_ruta([0,1,2,3], d), 4)

    def test_busqueda_local(self):
        d = matriz_distancias(puntos_aleatorios(15, random.Random(7)))
        ruta = random.Random(8).sample(range(15), 15)
        resultado = dos_opt(ruta, d)
        self.assertLessEqual(resultado['costo'], costo_ruta(ruta, d) + 1e-8)
        self.assertEqual(set(resultado['ruta']), set(ruta))

    def test_recocido(self):
        d = matriz_distancias(puntos_aleatorios(12, random.Random(2)))
        ruta = list(range(12))
        for esquema in ('lineal','exponencial'):
            resultado = recocido_simulado(ruta, d, esquema=esquema, iteraciones=300)
            self.assertLessEqual(resultado['costo'], costo_ruta(ruta, d)+1e-8)
            self.assertEqual(set(resultado['ruta']), set(ruta))

    def test_mst_aproximacion(self):
        for semilla in range(12):
            d = matriz_distancias(puntos_aleatorios(9, random.Random(semilla)))
            opt = tsp_exacto_held_karp(d)
            mst = costo_ruta(mst_preorden(d), d)
            self.assertLessEqual(mst, 2*opt + 1e-8)
            self.assertGreaterEqual(mst+1e-8, opt)

if __name__ == '__main__':
    unittest.main()
