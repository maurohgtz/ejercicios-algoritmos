"""Solo regenera el PDF usando resultados existentes (no repite los experimentos)."""
import json
from pathlib import Path
from reporte import generar_reporte

ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'resultados'/'resumen_completo.json').read_text(encoding='utf-8'))
meta=json.loads((ROOT/'datos_entrega.json').read_text(encoding='utf-8'))
generar_reporte(r,meta,ROOT/'reporte_final.pdf',ROOT/'graficas')
print('Reporte regenerado con tus enlaces: reporte_final.pdf')
