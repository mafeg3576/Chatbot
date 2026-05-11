# agent/agent.py
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple

import anthropic

from .prompts import SYSTEM_PROMPT
from .tool_executor import ejecutar_tool
from .tools import TOOLS

# ==========================
# Configuración y constantes
# ==========================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cliente de Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Constantes de comportamiento
MAX_TURNOS = 10
MAX_TOKENS = 4096
MODELO = "claude-sonnet-4-6"
MAX_HISTORIAL_MENSAJES = 20

# Caché del diagnóstico
diagnostico_cache = {}

# ==========================
# Funciones auxiliares
# ==========================

def _extraer_texto_respuesta(content: List[Any]) -> str:
    """Extrae el texto plano de la respuesta de Claude."""
    texto = ""
    for bloque in content:
        if hasattr(bloque, 'text') and bloque.text:
            texto += bloque.text
        elif hasattr(bloque, 'type') and bloque.type == "text" and hasattr(bloque, 'text'):
            texto += bloque.text
    return texto.strip()


def limpiar_historial(historial: List[Dict[str, Any]], max_mensajes: int = 20) -> List[Dict[str, Any]]:
    """Mantiene solo los primeros y últimos mensajes para no exceder el límite."""
    if len(historial) <= max_mensajes:
        return historial
    primeros = historial[:4]
    ultimos = historial[-(max_mensajes - 4):]
    return primeros + ultimos


def obtener_diagnostico_cache(org_id: str) -> str:
    """Obtiene el diagnóstico desde caché o consultando Supabase."""
    org_id_str = str(org_id)
    if org_id_str not in diagnostico_cache:
        logger.info(f"Consultando diagnóstico para {org_id_str}...")
        resultado = ejecutar_tool("obtener_diagnostico_completo", {"organizacion_id": org_id_str})
        if resultado and "No se encontró" not in resultado and "Error" not in resultado:
            diagnostico_cache[org_id_str] = resultado
        else:
            return None
    return diagnostico_cache[org_id_str]


def extraer_nivel_dimension(diagnostico_texto: str, dimension: str) -> int:
    """Extrae el nivel de madurez de una dimensión (ej: D4) desde el texto del diagnóstico."""
    if not diagnostico_texto:
        return None
    patron = rf'- {dimension}.*?:\s*([\d\.]+)'
    match = re.search(patron, diagnostico_texto)
    if match:
        puntaje = float(match.group(1).replace(',', '.'))
        if puntaje <= 1.0:
            return 1
        elif puntaje <= 2.0:
            return 2
        elif puntaje <= 3.0:
            return 3
        elif puntaje <= 4.0:
            return 4
        else:
            return 5
    return None


def generar_respuesta_ia(tipo_respuesta: str, diagnostico_texto: str) -> str:
    """
    Genera respuestas usando IA real (Claude) según el diagnóstico.
    Tipos soportados: "resumen", "analisis", "recomendaciones".
    """
    prompts = {
        "resumen": f"""
Eres un consultor senior en sostenibilidad textil. Analiza este diagnóstico y genera un RESUMEN EJECUTIVO.
OBJETIVO:
- Explicar el nivel de madurez
- Explicar qué significa operativamente
- Interpretar competitividad, eficiencia y riesgos
- Dar una lectura estratégica real

REGLAS:
- Máximo 180 palabras
- Profesional, claro, analítico
- No repetir datos literalmente
- NO usar emojis
- NO usar tablas

DIAGNÓSTICO:
{diagnostico_texto}
""",
        "analisis": f"""
Eres un consultor senior especializado en sostenibilidad para PyMEs textiles. Analiza el diagnóstico.

CLASIFICA OBLIGATORIAMENTE:
1. Fortalezas (>=4.0)
2. Áreas de mejora (3.0-3.9)
3. Brechas críticas (<3.0)

IMPORTANTE:
- Nunca pongas algo menor a 4.0 como fortaleza
- Explica impacto real: costos, eficiencia, cumplimiento, competitividad
- Explica qué pasa si no mejoran

FORMATO:
ANALISIS DE DIAGNOSTICO
Fortalezas: ...
Áreas de mejora: ...
Brechas críticas: ...
Conclusión: ...

NO usar emojis. NO usar tablas.

DIAGNÓSTICO:
{diagnostico_texto}
""",
        "recomendaciones": f"""
Eres un consultor senior en sostenibilidad textil colombiana. Genera máximo 4 recomendaciones ESTRATÉGICAS y PERSONALIZADAS según el diagnóstico.

Cada recomendación debe incluir:
- Qué hacer
- Por qué es importante
- Cómo empezar
- Impacto esperado
- Costo estimado en COP
- Plazo

REGLAS:
- Nada genérico
- Debe sentirse consultoría real
- Priorizar quick wins
- Priorizar sostenibilidad real
- Relacionar recomendaciones con las dimensiones débiles

FORMATO:
RECOMENDACIONES PRIORITARIAS
1. ...
   Por qué:
   Cómo empezar:
   Impacto:
   Costo:
   Plazo:

NO usar emojis. NO usar tablas.

DIAGNÓSTICO:
{diagnostico_texto}
"""
    }

    try:
        response = client.messages.create(
            model=MODELO,
            max_tokens=1200,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompts[tipo_respuesta]}]
        )
        return _extraer_texto_respuesta(response.content)
    except Exception as e:
        logger.error(f"Error generando respuesta IA: {e}")
        return "Error generando análisis inteligente."


def verificar_estado_agente() -> Dict[str, Any]:
    """Función auxiliar para debugging: muestra el estado del agente."""
    return {
        "modelo": MODELO,
        "tools_count": len(TOOLS),
        "anthropic_key_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "system_prompt_length": len(SYSTEM_PROMPT)
    }


# ==========================
# Funciones principales del agente
# ==========================

def manejar_opcion_numerica(org_id: str, opcion: str, historial: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    """Maneja las opciones 1 a 5 del menú principal."""
    diagnostico = obtener_diagnostico_cache(org_id)
    if not diagnostico:
        return "No se pudo obtener el diagnóstico. Verifica el ID.", historial

    if opcion == '1':
        respuesta = generar_respuesta_ia("resumen", diagnostico)
    elif opcion == '2':
        respuesta = generar_respuesta_ia("analisis", diagnostico)
    elif opcion == '3':
        respuesta = generar_respuesta_ia("recomendaciones", diagnostico)
    elif opcion == '4':
        respuesta = (
            "Elige la dimensión para ver indicadores y recomendaciones específicas:\n"
            "2. D2 - Dimensión Económica\n"
            "3. D3 - Dimensión Social\n"
            "4. D4 - Dimensión Ambiental"
        )
        historial = historial + [{'role': 'assistant', 'content': respuesta}]
        return respuesta, historial
    elif opcion == '5' or opcion.lower() == 'salir':
        respuesta = "Sesión finalizada. Gracias por usar IMGS-T Advisor. Para comenzar de nuevo, establece un ID de empresa."
        return respuesta, []
    else:
        respuesta = "Opción no válida. Elige 1,2,3,4 o 5."

    # Añadir menú principal al final (excepto si es la opción 4 que ya tiene su propio submenú)
    if opcion in ('1', '2', '3', '5'):
        respuesta += "\n\n¿Qué deseas hacer ahora?\n1. Resumen\n2. Análisis\n3. Recomendaciones generales\n4. Indicadores y recomendaciones específicas\n5. Salir"

    historial = historial + [{'role': 'assistant', 'content': respuesta}]
    return respuesta, historial


def manejar_indicadores_por_dimension(org_id: str, dimension: str, historial: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    """Opción 4: entrega recomendaciones específicas + indicadores para D2, D3 o D4."""
    diagnostico = obtener_diagnostico_cache(org_id)
    if not diagnostico:
        return "No se pudo obtener el diagnóstico.", historial

    nivel = extraer_nivel_dimension(diagnostico, dimension)
    if nivel is None:
        respuesta = f"No tengo el nivel actual para {dimension}. ¿Cuál es tu nivel (1 a 5)?"
        historial = historial + [{'role': 'assistant', 'content': respuesta, 'esperando_nivel': True, 'dim_indicador': dimension}]
        return respuesta, historial

    # Obtener recomendaciones e indicadores
    resultado_recomendaciones = ejecutar_tool('buscar_recomendaciones', {'dimension': dimension, 'nivel_actual': nivel})
    resultado_indicadores = ejecutar_tool('sugerir_indicadores', {'dimension': dimension, 'nivel_actual': nivel, 'solo_gestion': True})

    respuesta = f"RECOMENDACIONES ESPECÍFICAS E INDICADORES PARA {dimension} (nivel {nivel})\n\n"
    respuesta += resultado_recomendaciones
    respuesta += "\n\nINDICADORES SUGERIDOS:\n" + resultado_indicadores
    respuesta += "\n\n¿Qué deseas hacer ahora?\n1. Resumen\n2. Análisis\n3. Recomendaciones generales\n4. Indicadores y recomendaciones específicas\n5. Salir"

    historial = historial + [{'role': 'assistant', 'content': respuesta}]
    return respuesta, historial


def ejecutar_flujo_normal(
    organizacion_id: str,
    mensaje_usuario: str,
    historial: List[Dict[str, Any]]
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Flujo original con Claude (para preguntas libres, análisis complejos, etc.)
    """
    historial = historial + [{'role': 'user', 'content': mensaje_usuario}]

    for turno in range(MAX_TURNOS):
        try:
            response = client.messages.create(
                model=MODELO,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=historial
            )

            if response.stop_reason == "end_turn":
                texto = _extraer_texto_respuesta(response.content)
                if not texto:
                    texto = "He completado mi análisis. ¿Hay algo más en lo que pueda ayudarte?"
                historial = historial + [{'role': 'assistant', 'content': texto}]
                return texto, historial

            elif response.stop_reason == "tool_use":
                historial = historial + [{'role': 'assistant', 'content': response.content}]
                resultados = []
                for bloque in response.content:
                    if bloque.type == "tool_use":
                        try:
                            resultado = ejecutar_tool(bloque.name, bloque.input)
                            resultados.append({
                                "type": "tool_result",
                                "tool_use_id": bloque.id,
                                "content": resultado
                            })
                        except Exception as e:
                            resultados.append({
                                "type": "tool_result",
                                "tool_use_id": bloque.id,
                                "content": f"Error: {str(e)}"
                            })
                if resultados:
                    historial = historial + [{'role': 'user', 'content': resultados}]
                    continue
                else:
                    texto = _extraer_texto_respuesta(response.content)
                    if texto:
                        historial = historial + [{'role': 'assistant', 'content': texto}]
                        return texto, historial
                    else:
                        return "Necesito más información. ¿Puedes detallar tu pregunta?", historial

        except Exception as e:
            logger.error(f"Error en turno {turno}: {e}")
            if turno == MAX_TURNOS - 1:
                return f"Error: {str(e)}", historial
            continue

    return "Límite de iteraciones alcanzado. Reformula tu pregunta.", historial


def ejecutar_agente(
    organizacion_id: str,
    mensaje_usuario: str,
    historial: List[Dict[str, Any]]
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Punto de entrada del agente.
    Soporta menú interactivo (1-5), respuestas a submenús y preguntas libres.
    """
    logger.info(f"=== INICIO AGENTE ===")
    logger.info(f"Organizacion: {organizacion_id}")
    logger.info(f"Mensaje: {mensaje_usuario[:100]}...")
    logger.info(f"Historial: {len(historial)} mensajes")

    # Limpiar historial si es muy largo
    if len(historial) > MAX_HISTORIAL_MENSAJES:
        historial = limpiar_historial(historial, MAX_HISTORIAL_MENSAJES)

    try:
        if not mensaje_usuario or mensaje_usuario.strip() == "":
            return "Por favor, escribe un mensaje.", historial

        mensaje_limpio = mensaje_usuario.strip()

        # Verificar si es respuesta a un submenú (esperando dimensión para opción 4)
        ultimo_msg_bot = None
        for msg in reversed(historial):
            if msg.get('role') == 'assistant':
                ultimo_msg_bot = msg.get('content', '')
                break

        # Caso: estábamos esperando una dimensión para la opción 4
        if ultimo_msg_bot and "Elige la dimensión para ver indicadores" in ultimo_msg_bot:
            if mensaje_limpio.isdigit() and int(mensaje_limpio) in [2, 3, 4]:
                dimension = f"D{int(mensaje_limpio)}"
                return manejar_indicadores_por_dimension(organizacion_id, dimension, historial)

        # Opción numérica del menú principal (1-5)
        if re.match(r'^[1-5]$', mensaje_limpio) or mensaje_limpio.lower() in ['salir', 'exit']:
            return manejar_opcion_numerica(organizacion_id, mensaje_limpio, historial)

        # Si escribe directamente una dimensión (ej: "D4") como atajo
        if re.match(r'^[Dd][1-5]$', mensaje_limpio):
            return manejar_indicadores_por_dimension(organizacion_id, mensaje_limpio.upper(), historial)

        # Flujo normal con Claude (preguntas libres)
        return ejecutar_flujo_normal(organizacion_id, mensaje_usuario, historial)

    except Exception as e:
        logger.error(f"Error crítico: {e}")
        return f"Error inesperado: {str(e)}", historial


# ==========================
# Punto de entrada para pruebas
# ==========================

if __name__ == "__main__":
    print("=== AGENTE IMGS-T ===")
    estado = verificar_estado_agente()
    for k, v in estado.items():
        print(f"{k}: {v}")