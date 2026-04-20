import sys
import os
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.supabase_client import supabase
from knowledge.recomendaciones import BASE_CONOCIMIENTO

def ejecutar_tool(nombre: str, inputs: Dict[str, Any]) -> str:
    if nombre == "obtener_diagnostico_completo":
        return _obtener_diagnostico_completo(inputs)
    elif nombre == "buscar_recomendaciones":
        return _buscar_recomendaciones(inputs)
    elif nombre == "identificar_brechas":
        return _identificar_brechas(inputs)
    elif nombre == "guardar_plan_accion":
        return _guardar_plan_accion(inputs)
    else:
        return f"Herramienta '{nombre}' no reconocida."

# ========== TOOL 1: OBTENER DIAGNÓSTICO (desde respuestas) ==========
def _obtener_diagnostico_completo(inputs: Dict[str, Any]) -> str:
    org_id = inputs.get('organizacion_id')
    if not org_id:
        return "No se proporcionó ID de organización."

    try:
        org_id_int = int(org_id)
    except:
        org_id_int = org_id

    # 1. Obtener nombre de la empresa
    empresa = supabase.table('empresas').select('nombre_empresa').eq('id', org_id_int).execute()
    if not empresa.data:
        return f"No se encontró empresa con ID {org_id_int}"
    nombre_empresa = empresa.data[0]['nombre_empresa']

    # 2. Obtener respuestas de la empresa
    respuestas = supabase.table('respuestas').select('pregunta_id, valor_puntos').eq('empresa_id', org_id_int).execute()
    if not respuestas.data:
        return f"La empresa {nombre_empresa} no ha completado el diagnóstico. No hay respuestas."

    # 3. Obtener relación pregunta -> dimensión
    preguntas = supabase.table('preguntas').select('id, dimension_id').execute()
    dim_por_pregunta = {p['id']: p['dimension_id'] for p in preguntas.data}

    # 4. Acumular puntajes por dimensión (valor_puntos está en escala 0-4)
    puntajes_dim = {1: [], 2: [], 3: [], 4: [], 5: []}
    for r in respuestas.data:
        p_id = r['pregunta_id']
        valor = r.get('valor_puntos')
        if valor is not None and p_id in dim_por_pregunta:
            dim_id = dim_por_pregunta[p_id]
            try:
                puntajes_dim[dim_id].append(float(valor))
            except:
                pass

    # 5. Calcular promedios y convertir a escala 0-5
    resultados = {}
    for dim_id, valores in puntajes_dim.items():
        if valores:
            prom_0_4 = sum(valores) / len(valores)
            prom_0_5 = (prom_0_4 / 4) * 5
            resultados[f"D{dim_id}"] = round(prom_0_5, 2)
        else:
            resultados[f"D{dim_id}"] = 0.0

    # Asegurar las 5 dimensiones
    for d in ['D1', 'D2', 'D3', 'D4', 'D5']:
        if d not in resultados:
            resultados[d] = 0.0

    indice_global = sum(resultados.values()) / 5

    # 6. Determinar nivel de madurez (desde tu tabla niveles_madurez)
    niveles = supabase.table('niveles_madurez').select('*').execute()
    nivel_global = 1
    nivel_nombre = "Reactivo/Incipiente"
    for n in niveles.data:
        if n['rango_min'] <= indice_global <= n['rango_max']:
            nivel_global = n['id']
            nivel_nombre = n['nombre_nivel']
            break

    # Construir respuesta formateada
    respuesta = f"""
EMPRESA: {nombre_empresa} (ID {org_id_int})
INDICE GLOBAL: {indice_global:.2f} / 5.0
NIVEL: {nivel_global} - {nivel_nombre}

PUNTAJES POR DIMENSION:
- D1 Gobernanza: {resultados.get('D1', 0):.2f}
- D2 Economica: {resultados.get('D2', 0):.2f}
- D3 Social: {resultados.get('D3', 0):.2f}
- D4 Ambiental: {resultados.get('D4', 0):.2f}
- D5 Datos/Tecnologia: {resultados.get('D5', 0):.2f}
"""
    return respuesta

# ========== TOOL 2: BUSCAR RECOMENDACIONES ==========
def _buscar_recomendaciones(inputs: Dict[str, Any]) -> str:
    dimension = inputs.get('dimension')
    nivel_actual = inputs.get('nivel_actual')
    if not dimension or not nivel_actual:
        return "Faltan parámetros: dimension y nivel_actual"
    recs = BASE_CONOCIMIENTO.get(dimension, {}).get(nivel_actual, [])
    if not recs:
        return f"No hay recomendaciones para {dimension} nivel {nivel_actual}"
    resultado = f"Recomendaciones para {dimension} (nivel {nivel_actual}):\n\n"
    for i, rec in enumerate(recs, 1):
        if isinstance(rec, dict):
            resultado += f"{i}. {rec.get('accion', rec)}\n"
            resultado += f"   Por que: {rec.get('por_que', '')}\n"
            resultado += f"   Como empezar: {rec.get('como_empezar', '')}\n"
            resultado += f"   Recursos: {rec.get('recursos', '')}\n"
            resultado += f"   Plazo: {rec.get('plazo', '')}\n\n"
        else:
            resultado += f"{i}. {rec}\n\n"
    return resultado

# ========== TOOL 3: IDENTIFICAR BRECHAS ==========
def _identificar_brechas(inputs: Dict[str, Any]) -> str:
    puntajes = inputs.get('puntajes', {})
    if not puntajes:
        return "No se proporcionaron puntajes"
    ordenados = sorted(puntajes.items(), key=lambda x: x[1])
    top3 = ordenados[:3]
    res = "Brechas mas criticas (menor a mayor puntaje):\n"
    for i, (dim, val) in enumerate(top3, 1):
        res += f"{i}. {dim}: {val}/5.0\n"
    return res

# ========== TOOL 4: GUARDAR PLAN DE ACCION ==========
def _guardar_plan_accion(inputs: Dict[str, Any]) -> str:
    org_id = inputs.get('organizacion_id')
    plan = inputs.get('plan')
    if not org_id or not plan:
        return "Faltan organizacion_id o plan"
    try:
        supabase.table('planes_accion').insert({
            'organizacion_id': int(org_id),
            'plan': plan,
            'fecha_creacion': 'now()'
        }).execute()
        return "Plan de accion guardado correctamente."
    except Exception as e:
        return f"Error al guardar: {e}"