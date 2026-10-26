"""Generacion del reporte PDF directamente a partir de los resultados reales."""
import html
import statistics
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    KeepTogether, PageBreak
)
import matplotlib

AZUL = colors.HexColor('#18457e')
SUBTITULO = colors.HexColor('#21364e')
GRIS = colors.HexColor('#5a6878')
CLARO = colors.HexColor('#eff5fc')


def establecer_fuentes():
    fuentes = Path(matplotlib.get_data_path()) / 'fonts' / 'ttf'
    pdfmetrics.registerFont(TTFont('DejaVu',str(fuentes/'DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('DejaVu-Bold',str(fuentes/'DejaVuSans-Bold.ttf')))
    pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',
                                  italic='DejaVu',boldItalic='DejaVu-Bold')


def generar_reporte(datos, metadata, destino, carpeta_graficas):
    establecer_fuentes()
    page_w, page_h = A4
    doc = SimpleDocTemplate(str(destino),pagesize=A4,
                            leftMargin=46,rightMargin=46,topMargin=49,bottomMargin=49,
                            title='Reporte - Ejercicios de algoritmos',
                            author=metadata.get('nombre','Estudiante'))
    sw=page_w-92
    estilos=getSampleStyleSheet()
    estilos.add(ParagraphStyle(name='TituloPropio',fontName='DejaVu-Bold',fontSize=21,leading=28,
                               textColor=AZUL,spaceAfter=15))
    estilos.add(ParagraphStyle(name='SubtituloPropio',fontName='DejaVu-Bold',fontSize=13.2,leading=19,
                               textColor=AZUL,spaceBefore=15,spaceAfter=8))
    estilos.add(ParagraphStyle(name='ParrafoPropio',fontName='DejaVu',fontSize=9.1,
                               leading=15.2,spaceAfter=8,textColor=SUBTITULO))
    estilos.add(ParagraphStyle(name='PequePropio',fontName='DejaVu',fontSize=8,
                               leading=12,spaceAfter=4,textColor=SUBTITULO))
    estilos.add(ParagraphStyle(name='CaptionPropio',fontName='DejaVu',fontSize=8,
                               leading=12,alignment=TA_CENTER,textColor=GRIS,spaceAfter=13))
    estilos.add(ParagraphStyle(name='MetaPropio',fontName='DejaVu',fontSize=9,
                               leading=15,spaceAfter=6,textColor=SUBTITULO,wordWrap='CJK'))
    story=[]
    def p(txt): story.append(Paragraph(txt,estilos['ParrafoPropio']))
    def h(txt): story.append(Paragraph(txt,estilos['SubtituloPropio']))
    def esc(x): return html.escape(str(x))
    def tabla(filas, widths=None):
        contenido = [[Paragraph(esc(x), estilos['PequePropio']) for x in row] for row in filas]
        t=Table(contenido,colWidths=widths or [sw/len(filas[0])]*len(filas[0]),repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),CLARO),
            ('GRID',(0,0),(-1,-1),.35,colors.HexColor('#d5e0ec')),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ]))
        story.append(t)
        story.append(Spacer(1,10))
    def graf(nombre,caption, max_alt=265):
        img=Image(str(carpeta_graficas/nombre))
        factor = min(sw/img.imageWidth,max_alt/img.imageHeight)
        img.drawWidth = img.imageWidth * factor
        img.drawHeight = img.imageHeight * factor
        img.hAlign='CENTER'
        story.append(img)
        story.append(Paragraph(caption, estilos['CaptionPropio']))

    # Portada compacta
    story.append(Spacer(1,23))
    story.append(Paragraph('Experimentos de algoritmos',estilos['TituloPropio']))
    p('<b>Reporte final:</b> aceleración paralela, mochila voraz, búsqueda local 2-opt, '
      'recocido simulado y aproximación MST para el TSP.')
    story.append(Spacer(1,9))
    for clave,label in [('nombre','Alumno'),('materia','Materia'),
                         ('repositorio_url','Repositorio público'),('video_url','Video demostrativo')]:
        story.append(Paragraph('<b>'+label+':</b> '+esc(metadata.get(clave,'PENDIENTE')),
                               estilos['MetaPropio']))
    story.append(Spacer(1,13))
    h('Resumen y metodología')
    p('Se implementaron los cinco experimentos en Python. Se usaron semillas fijas para la '
      'reproducibilidad, mediciones con <b>time.perf_counter()</b> y conjuntos de prueba '
      'compartidos cuando fue necesario comparar métodos. Las tablas y figuras siguientes '
      'se generan automáticamente a partir de ejecuciones reales; no se introdujeron '
      'valores manualmente.')
    p('El problema del agente viajero (TSP) se modeló con distancias euclidianas '
      'bidimensionales. El costo incluye el regreso a la ciudad de inicio. '
      'Cada ruta contiene cada ciudad exactamente una vez. En las pruebas de nueve '
      'ciudades se calculó el óptimo global exacto con programación dinámica Held-Karp.')

    e=datos['ej1']
    h('1. Aceleración paralela: Monte Carlo para π')
    p(f'Se estimó π usando {e["muestras"]:,} puntos uniformes dentro del cuadrado unitario '
      f'y {e["repeticiones"]} repeticiones independientes para cada configuración: '
      '1, 2, 4 y 8 procesos. El número total de puntos se mantuvo fijo. '
      'Se midió el tiempo de pared y se tomó la mediana; la aceleración se calculó '
      'como S(p) = T(1) / T(p).')
    tabla([['Procesos','Tiempo mediano (s)','Speedup real','Speedup ideal']]+[
        [str(q['procesos']),f"{q['mediana_s']:.3f}",f"{q['speedup']:.2f}",str(q['speedup_ideal'])]
        for q in e['resumen']],widths=[sw*.18,sw*.30,sw*.27,sw*.25])
    graf('01_speedup.png','Figura 1. Aceleración medida comparada con el aumento ideal lineal.',235)
    ultimo=e['resumen'][-1]
    p(f'<b>Análisis:</b> con ocho procesos se observó una aceleración de {ultimo["speedup"]:.2f}× '
      f'(ideal: 8×; eficiencia: {100*ultimo["eficiencia"]:.1f}%). '
      'No se espera escalado perfecto porque crear procesos, repartir trabajo y reunir resultados '
      'agrega sobrecostos; la CPU y el ancho de banda de memoria también se comparten. '
      'La ley de Amdahl establece que la fracción no paralelizable limita la aceleración máxima. '
      'Con trabajos relativamente pequeños, los costos fijos pueden incluso provocar desaceleración.')

    e=datos['ej2']
    h('2. Mochila 0/1: menor peso contra valor/peso')
    p('Para una capacidad de 10 kg se evaluaron tres objetos indivisibles. '
      'En el método 1 se ordenan por peso ascendente; en el método 2 por densidad '
      'valor/peso descendente. En ambos casos se incorpora el siguiente objeto solo '
      'si cabe en la capacidad restante.')
    tabla([['Objeto','Peso (kg)','Valor','Valor/peso']]+[
        [o['nombre'],str(o['peso']),str(o['valor']),f"{o['valor']/o['peso']:.2f}"]
        for o in e['objetos']])
    tabla([['Criterio','Objetos elegidos','Peso usado','Valor total']]+[
        ['Menor peso',', '.join(e['metodos']['peso']['nombres']),
         str(e['metodos']['peso']['peso']),str(e['metodos']['peso']['valor'])],
        ['Mayor valor/peso',', '.join(e['metodos']['densidad']['nombres']),
         str(e['metodos']['densidad']['peso']),str(e['metodos']['densidad']['valor'])]])
    graf('02_mochila.png','Figura 2. Selecciones y aprovechamiento de la capacidad.',235)
    p(f'<b>Análisis:</b> seleccionar primero los más ligeros produce valor '
      f'{e["metodos"]["peso"]["valor"]}; priorizar densidad da valor '
      f'{e["metodos"]["densidad"]["valor"]}. '
      'La primera estrategia compromete capacidad con objetos poco valiosos. '
      'Esta instancia demuestra que menor peso puede ser peor que valor/peso. '
      'La heurística valor/peso tampoco garantiza el óptimo general de la mochila 0/1.')

    e=datos['ej3']; r=e['resumen']
    h('3. Búsqueda local: 2-opt para TSP')
    p(f'Se generó un conjunto fijo de {e["ciudades"]} ciudades y se realizaron '
      f'{e["repeticiones"]} ensayos por método inicial. Para cada ensayo se comparó '
      'una permutación aleatoria contra vecino más cercano (ciudad inicial aleatoria). '
      '2-opt evalúa todas las inversiones válidas de segmentos y acepta la mejor '
      'reducción por iteración hasta alcanzar un óptimo local.')
    tabla([['Métrica (media)','Inicio aleatorio','Vecino más cercano'],
           ['Costo inicial',f"{r['costo_inicial_aleatoria']:.2f}",f"{r['costo_inicial_vecino']:.2f}"],
           ['Número de mejoras',f"{r['mejoras_aleatoria']:.2f}",f"{r['mejoras_vecino']:.2f}"],
           ['Costo final',f"{r['costo_aleatoria']:.2f}",f"{r['costo_vecino']:.2f}"]])
    graf('03_dos_opt_mejoras.png','Figura 3. Distribución de mejoras hasta el óptimo local.',225)
    graf('04_dos_opt_calidad.png','Figura 4. Distancias finales tras búsqueda local con 2-opt.',225)
    relacion='menos' if r['mejoras_vecino'] < r['mejoras_aleatoria'] else 'igual o más'
    mejor_metodo='vecino más cercano' if r['costo_vecino']<r['costo_aleatoria'] else 'inicio aleatorio'
    p(f'<b>Análisis:</b> en esta muestra, vecino más cercano requirió {relacion} '
      f'mejoras que el inicio aleatorio ({r["mejoras_vecino"]:.2f} frente a '
      f'{r["mejoras_aleatoria"]:.2f}, en promedio). '
      f'La menor distancia final promedio correspondió a {mejor_metodo}. '
      'El número de mejoras cuenta movimientos aceptados, no tiempo de CPU. '
      'Un óptimo local no implica óptimo global: diferentes rutas iniciales '
      'pueden converger a circuitos distintos.')

    e=datos['ej4']; rl=e['resumen']['lineal']; re=e['resumen']['exponencial']
    h('4. Recocido simulado: ajuste del enfriamiento')
    p(f'En el mismo escenario de {e["ciudades"]} ciudades se compararon '
      f'{e["repeticiones"]} ejecuciones por calendario, de {e["iteraciones"]} '
      'iteraciones cada una. Se usó el mismo punto de partida de cada ensayo '
      'para ambos calendarios, con T inicial = 40 y T final = 0.1. '
      'Los vecinos son movimientos 2-opt; las soluciones peores pueden aceptarse '
      'con probabilidad exp(-Δ/T). Siempre se conserva la mejor ruta encontrada.')
    tabla([['Enfriamiento','Costo final medio','Tiempo medio (s)','Desv. costo'],
           ['Lineal',f"{rl['costo']:.2f}",f"{rl['segundos']:.4f}",f"{rl['desv_costo']:.2f}"],
           ['Exponencial',f"{re['costo']:.2f}",f"{re['segundos']:.4f}",f"{re['desv_costo']:.2f}"]])
    graf('05_recocido_convergencia.png','Figura 5. Evolución del mejor costo y temperatura de un ensayo comparable.',236)
    graf('06_recocido_tiempo_calidad.png','Figura 6. Tiempo real frente a costo final en cada réplica; la X señala la media.',235)
    mejor='lineal' if rl['costo']<re['costo'] else 'exponencial'
    rapida='lineal' if rl['segundos']<re['segundos'] else 'exponencial'
    p(f'<b>Análisis:</b> la menor distancia media correspondió al enfriamiento '
      f'{mejor}, mientras que el menor tiempo medio se observó con el '
      f'enfriamiento {rapida}. El lineal conserva temperaturas relativamente '
      'elevadas durante más iteraciones; el exponencial disminuye más '
      'proporcionalmente al inicio. Ambos ejecutan el mismo número de '
      'iteraciones; las diferencias de tiempo incluyen ruido del sistema '
      'y costos de operaciones específicas. No se garantiza superioridad universal.')

    e=datos['ej5']; r=e['resumen']; mst=r['mst']; post=r['mst_2opt']
    h('5. Razón de aproximación de MST')
    p('Se generaron exactamente 100 instancias aleatorias independientes de '
      '9 ciudades con distancias euclidianas. Para cada instancia se obtuvo el '
      'óptimo global con Held-Karp, luego una ruta MST (Prim + preorden + atajos) '
      'y se aplicó 2-opt a esa ruta. También se ejecutaron los dos inicios '
      'de búsqueda local y los dos esquemas de recocido simulado sobre '
      'las mismas instancias; en recocido se usaron 2,500 iteraciones por ejecución.')
    tabla([['Método','Costo medio','Razón media','Razón máxima']]+[
        [nom,f"{r[clave]['media_costo']:.2f}",f"{r[clave]['media_razon']:.3f}",
         f"{r[clave]['max_razon']:.3f}"]
        for clave, nom in [
            ('mst','MST preorden'),('mst_2opt','MST + 2-opt'),
            ('local_aleatoria','Local aleatorio'),('local_vecino','Local vecino'),
            ('recocido_lineal','Recocido lineal'),('recocido_exponencial','Recocido exp.')
        ]],widths=[sw*.28,sw*.24,sw*.24,sw*.24])
    graf('07_mst_razon_histograma.png','Figura 7. Distribución de C(MST)/C(óptimo) y referencia teórica en 2.',225)
    graf('08_mst_comparacion_costos.png','Figura 8. Costos reales de los seis métodos en las 100 instancias.',225)
    graf('09_mst_comparacion_razones.png','Figura 9. Razones respecto del óptimo exacto, para comparación normalizada.',225)
    reduccion=100*(mst['media_costo']-post['media_costo'])/mst['media_costo']
    p(f'<b>Análisis:</b> la razón media de MST fue {mst["media_razon"]:.3f}, '
      f'y la máxima {mst["max_razon"]:.3f}, '
      'por debajo o igual al límite teórico de 2. '
      f'Agregar 2-opt redujo el costo medio de {mst["media_costo"]:.2f} '
      f'a {post["media_costo"]:.2f}, equivalente a una reducción de '
      f'{reduccion:.1f}%. La cota de 2 es una garantía de peor caso '
      'para el TSP métrico, no una predicción de las razones típicas. '
      'La mejora posterior no puede aumentar el costo debido a que 2-opt '
      'solo acepta cambios estrictamente favorables.')

    h('Conclusiones, limitaciones y reproducibilidad')
    p('Los resultados muestran cómo el paralelismo real depende de los costos de '
      'administración; cómo la regla greedy elegida altera el resultado en mochila '
      '0/1; y cómo la solución inicial y el enfriamiento afectan las heurísticas '
      'para el TSP. El MST preorden proporciona una garantía matemática para '
      'distancias métricas y puede mejorarse con búsqueda local.')
    p('<b>Limitaciones:</b> las mediciones de tiempo varían según el equipo y los '
      'procesos en segundo plano. Las comparaciones empíricas no prueban que un '
      'método sea superior en todas las instancias. Los recocidos son estocásticos '
      'y las conclusiones corresponden a las semillas, tamaños y parámetros usados. '
      'El límite 2 del MST requiere distancias métricas (desigualdad triangular).')
    p('<b>Reproducibilidad:</b> ejecutar <b>python main.py</b> desde la raíz del '
      'repositorio. Las semillas están fijadas en el código. Los datos completos '
      'se guardan en <b>resultados/</b>, las nueve visualizaciones en '
      '<b>graficas/</b> y el reporte en <b>reporte_final.pdf</b>. '
      'Las pruebas automáticas se ejecutan con '
      '<b>python -m unittest discover -s tests -v</b>.')
    p('<b>Referencias conceptuales:</b> Ley de Amdahl (aceleración paralela); '
      'heurística 2-opt (búsqueda local TSP); recocido simulado con criterio '
      'de Metropolis; aproximación doble del árbol mínimo para TSP métrico; '
      'programación dinámica Held-Karp para TSP exacto.')

    def decoracion(canvas, documento):
        canvas.saveState()
        w,h=A4
        canvas.setFillColor(AZUL)
        canvas.rect(0,h-14,w,14,fill=1,stroke=0)
        canvas.setFont('DejaVu',7.4)
        canvas.setFillColor(GRIS)
        canvas.drawString(46,26,'Experimentos de algoritmos | Resultados reproducibles')
        canvas.drawRightString(w-46,26,f'Página {documento.page}')
        canvas.restoreState()
    doc.build(story,onFirstPage=decoracion,onLaterPages=decoracion)
