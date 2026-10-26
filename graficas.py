"""Graficas originales basadas en los CSV y resultados medidos."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

AZUL = '#2563eb'
NARANJA = '#e8791d'
VERDE = '#159f75'
MORADO = '#8254c5'
ROJO = '#d64045'


def estilo():
    plt.rcParams.update({
        'font.size':10, 'axes.titlesize':13, 'axes.titleweight':'bold',
        'axes.spines.top':False,'axes.spines.right':False,
        'axes.grid':True,'grid.alpha':0.15,'figure.facecolor':'white',
        'savefig.facecolor':'white','axes.labelcolor':'#26384b',
    })


def salvar(fig, destino):
    fig.tight_layout(pad=2)
    fig.savefig(destino, dpi=180, bbox_inches='tight')
    plt.close(fig)


def box(ax, series, etiquetas, titulo, ylabel, colores=None):
    bo = ax.boxplot(series, tick_labels=etiquetas, patch_artist=True,
                    showmeans=True, meanprops={'marker':'D','markersize':5,
                                               'markerfacecolor':'white','markeredgecolor':'#172a43'})
    for i, parche in enumerate(bo['boxes']):
        parche.set_facecolor((colores or [AZUL,VERDE,NARANJA,MORADO])[i%4])
        parche.set_alpha(.55)
    ax.set_title(titulo)
    ax.set_ylabel(ylabel)
    ax.grid(axis='y',alpha=.2)
    ax.grid(axis='x',visible=False)


def crear_graficas(datos, carpeta):
    estilo()
    e1, e2, e3, e4, e5 = (datos[f'ej{x}'] for x in range(1,6))
    # 1. Speedup
    rs=e1['resumen']
    procs=[x['procesos'] for x in rs]
    speedup=[x['speedup'] for x in rs]
    fig,ax=plt.subplots(figsize=(7.5,4.1))
    ax.plot(procs,procs,'--o',color='#64748b',label='Ideal: S(p) = p')
    ax.plot(procs,speedup,'-o',linewidth=2.4,markersize=8,color=AZUL,label='Medido: T(1) / T(p)')
    ax.set(xticks=procs,xlabel='Numero de procesos',ylabel='Aceleracion (speedup)',
           title='Ejercicio 1 | Aceleracion paralela')
    ax.set_ylim(bottom=0)
    ax.legend(frameon=False)
    salvar(fig,carpeta/'01_speedup.png')

    # 2. Comparar objetos, uso capacidad y valor final
    obj=e2['objetos']
    met=e2['metodos']
    fig,axs=plt.subplots(1,2,figsize=(10,3.9))
    for indice,clave in enumerate(('peso','densidad')):
        valores=[o['valor'] if o['nombre'] in met[clave]['nombres'] else 0 for o in obj]
        axs[0].bar([i+(-.19 if indice==0 else .19) for i in range(len(obj))],valores,
                   width=.38, label=('Menor peso' if indice==0 else 'Mayor valor/peso'),
                   color=AZUL if indice==0 else VERDE)
    axs[0].set_xticks(range(len(obj)),[f"{o['nombre']}\n{str(o['peso'])} kg" for o in obj])
    axs[0].set_title('Valor de los objetos seleccionados')
    axs[0].set_ylabel('Valor aportado')
    axs[0].legend(frameon=False,fontsize=8)
    axs[1].bar([0,1],[met['peso']['peso'],met['densidad']['peso']],width=.35,color=[AZUL,VERDE])
    axs[1].set_xticks([0,1],['Menor peso','Valor/peso'])
    axs[1].axhline(e2['capacidad'],color='#64748b',linestyle='--',label='Capacidad maxima')
    axs[1].set_ylabel('Capacidad usada (kg)')
    axs[1].set_title('Capacidad utilizada')
    for i,k in enumerate(('peso','densidad')):
        axs[1].text(i,met[k]['peso']+.16,f"valor = {met[k]['valor']}",ha='center',weight='bold',fontsize=9)
    axs[1].set_ylim(0,e2['capacidad']*1.35)
    axs[1].legend(frameon=False,fontsize=8)
    salvar(fig,carpeta/'02_mochila.png')

    # 3. 2-opt cantidad mejoras
    filas=e3['filas']
    fig,ax=plt.subplots(figsize=(8,4.1))
    box(ax,[[x['aleatoria_mejoras'] for x in filas],[x['vecino_mejoras'] for x in filas]],
        ['Ruta aleatoria','Vecino mas cercano'],
        'Ejercicio 3 | Mejoras hasta el optimo local','Numero de movimientos 2-opt')
    salvar(fig,carpeta/'03_dos_opt_mejoras.png')

    # 4. calidad local
    fig,ax=plt.subplots(figsize=(8,4.1))
    box(ax,[[x['aleatoria_final'] for x in filas],[x['vecino_final'] for x in filas]],
        ['Ruta aleatoria','Vecino mas cercano'],
        'Ejercicio 3 | Costo final del optimo local','Distancia total del circuito')
    salvar(fig,carpeta/'04_dos_opt_calidad.png')

    # 5. Annealing cost vs iteration, temp vs iteration
    fig,axs=plt.subplots(1,2,figsize=(10.4,4))
    for nombre,color in [('lineal',AZUL),('exponencial',NARANJA)]:
        historial=e4['historiales'][nombre]
        axs[0].plot([x[0] for x in historial],[x[1] for x in historial],label=nombre.capitalize(),color=color,lw=1.9)
        axs[1].plot([x[0] for x in historial],[x[2] for x in historial],label=nombre.capitalize(),color=color,lw=1.9)
    axs[0].set(xlabel='Iteracion',ylabel='Mejor distancia observada',title='Convergencia (ensayo 1)')
    axs[1].set(xlabel='Iteracion',ylabel='Temperatura',title='Esquemas de enfriamiento')
    for a in axs: a.legend(frameon=False)
    salvar(fig,carpeta/'05_recocido_convergencia.png')

    # 6. Annealing time vs quality (replicas reales)
    fig,ax=plt.subplots(figsize=(8,4.3))
    for nombre,color in [('lineal',AZUL),('exponencial',NARANJA)]:
        subcon=[x for x in e4['filas'] if x['enfriamiento']==nombre]
        ax.scatter([x['segundos'] for x in subcon],[x['costo_final'] for x in subcon],
                   alpha=.7,label=nombre.capitalize(),s=42,color=color)
        ax.scatter([sum(x['segundos'] for x in subcon)/len(subcon)],
                   [sum(x['costo_final'] for x in subcon)/len(subcon)],
                   marker='X',edgecolors='#182b49',linewidths=1.2,s=190,color=color)
    ax.set(xlabel='Tiempo (s) por ejecucion',ylabel='Mejor costo final',
           title='Ejercicio 4 | Tiempo de ejecucion vs calidad')
    ax.legend(frameon=False)
    salvar(fig,carpeta/'06_recocido_tiempo_calidad.png')

    # 7. MST ratio + theory
    ratios=[x['razon_mst'] for x in e5['filas']]
    fig,ax=plt.subplots(figsize=(8,4.2))
    ax.hist(ratios,bins=16,color=AZUL,alpha=.75,edgecolor='white')
    ax.axvline(2,color=ROJO,ls='--',lw=2,label='Limite teorico: 2')
    ax.axvline(sum(ratios)/len(ratios),color=VERDE,lw=2,label=f'Media observada: {sum(ratios)/len(ratios):.3f}')
    ax.set(xlabel='C(MST preorden) / C(optimo exacto)',
           ylabel='Numero de instancias',title='Ejercicio 5 | Razon de aproximacion (100 TSP)')
    ax.set_xlim(left=1,right=2.05)
    ax.legend(frameon=False)
    salvar(fig,carpeta/'07_mst_razon_histograma.png')

    # 8. Boxplot raw cost for all methods on 100 shared instances
    keys=['mst','mst_2opt','local_aleatoria','local_vecino','recocido_lineal','recocido_exponencial']
    labels=['MST','MST +\n2-opt','Local\naleat.','Local\nvecino','SA\nlineal','SA\nexpo.']
    fig,ax=plt.subplots(figsize=(10,4.5))
    box(ax,[[f[k] for f in e5['filas']] for k in keys],labels,
        'Ejercicio 5 | Costo de los seis metodos sobre las mismas 100 instancias',
        'Distancia total (menor es mejor)',[AZUL,VERDE,NARANJA,MORADO,'#d65a96','#c39940'])
    salvar(fig,carpeta/'08_mst_comparacion_costos.png')

    # 9. ratio comparison to exact optimum across 100
    fig,ax=plt.subplots(figsize=(10,4.5))
    box(ax,[[f['razon_'+k] for f in e5['filas']] for k in keys],labels,
        'Ejercicio 5 | Calidad relativa al optimo exacto (Held-Karp)',
        'Costo / costo optimo (1 = optimo)',[AZUL,VERDE,NARANJA,MORADO,'#d65a96','#c39940'])
    ax.axhline(1,ls=':',lw=1.5,color='#1c9a79',label='Optimo = 1')
    ax.axhline(2,ls='--',lw=1.5,color=ROJO,label='Cota MST = 2')
    ax.legend(frameon=False)
    salvar(fig,carpeta/'09_mst_comparacion_razones.png')
