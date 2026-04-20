# agent/agent.py

import anthropic
import os
import logging
from typing import Tuple, List, Dict, Any
from datetime import datetime

from .tools import TOOLS
from .tool_executor import ejecutar_tool
from .prompts import SYSTEM_PROMPT

# Configurar logging para debug y monitoreo (sin emojis)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa el cliente de Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Constantes
MAX_TURNOS = 10
MAX_TOKENS = 4096
MODELO = "claude-sonnet-4-6"
MAX_HISTORIAL_MENSAJES = 20  # Limitar historial para no exceder tokens


def ejecutar_agente(
    organizacion_id: str,
    mensaje_usuario: str,
    historial: List[Dict[str, Any]]
) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Ejecuta el agente de sostenibilidad con manejo robusto de errores.
    
    Args:
        organizacion_id: ID de la organización en Supabase
        mensaje_usuario: Mensaje del usuario
        historial: Historial de conversación anterior
    
    Returns:
        Tuple con (respuesta_final, historial_actualizado)
    """
    
    logger.info(f"=== INICIO AGENTE ===")
    logger.info(f"Organizacion: {organizacion_id}")
    logger.info(f"Mensaje usuario: {mensaje_usuario[:100]}...")
    logger.info(f"Longitud historial: {len(historial)} mensajes")
    
    # Limpiar historial si es muy largo (para no exceder tokens)
    if len(historial) > MAX_HISTORIAL_MENSAJES:
        logger.info(f"Historial largo ({len(historial)} mensajes), limpiando...")
        historial = limpiar_historial(historial, MAX_HISTORIAL_MENSAJES)
    
    try:
        # Validar que el mensaje no esté vacío
        if not mensaje_usuario or mensaje_usuario.strip() == "":
            return "Por favor, escribe un mensaje para poder ayudarte.", historial
        
        # Agrega el mensaje del usuario al historial
        historial = historial + [{'role': 'user', 'content': mensaje_usuario}]
        
        # Bucle principal del agente
        for turno in range(MAX_TURNOS):
            logger.info(f"Turno {turno + 1}/{MAX_TURNOS}")
            
            try:
                # Llamar a Claude con el contexto actual
                response = client.messages.create(
                    model=MODELO,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=historial
                )
                
                logger.info(f"Stop reason: {response.stop_reason}")
                logger.info(f"Contenido respuesta: {len(response.content)} bloques")
                
                # CASO 1: Claude terminó la respuesta
                if response.stop_reason == "end_turn":
                    texto_final = _extraer_texto_respuesta(response.content)
                    
                    if not texto_final:
                        texto_final = "He completado mi analisis. Hay algo mas en lo que pueda ayudarte?"
                    
                    # Agregar respuesta al historial
                    historial = historial + [{'role': 'assistant', 'content': texto_final}]
                    
                    logger.info(f"Respuesta final generada ({len(texto_final)} caracteres)")
                    logger.info("=== FIN AGENTE (respuesta completa) ===")
                    
                    return texto_final, historial
                
                # CASO 2: Claude quiere usar herramientas
                elif response.stop_reason == "tool_use":
                    logger.info("Claude solicita usar herramientas")
                    
                    # Agregar la respuesta de Claude al historial
                    historial = historial + [{'role': 'assistant', 'content': response.content}]
                    
                    # Ejecutar las herramientas solicitadas
                    resultados = []
                    for bloque in response.content:
                        if bloque.type == "tool_use":
                            logger.info(f"Ejecutando tool: {bloque.name}")
                            logger.info(f"   Input: {bloque.input}")
                            
                            try:
                                resultado = ejecutar_tool(bloque.name, bloque.input)
                                logger.info(f"   Resultado: {str(resultado)[:100]}...")
                                
                                resultados.append({
                                    "type": "tool_result",
                                    "tool_use_id": bloque.id,
                                    "content": resultado
                                })
                            except Exception as e:
                                error_msg = f"Error ejecutando {bloque.name}: {str(e)}"
                                logger.error(error_msg)
                                resultados.append({
                                    "type": "tool_result",
                                    "tool_use_id": bloque.id,
                                    "content": f"Error: {error_msg}. Por favor, intenta nuevamente."
                                })
                    
                    # Agregar los resultados al historial
                    if resultados:
                        historial = historial + [{'role': 'user', 'content': resultados}]
                        logger.info(f"{len(resultados)} herramientas ejecutadas, continuando...")
                    
                    # Continuar el bucle para que Claude procese los resultados
                    continue
                
                # CASO 3: Otros tipos de stop (max_tokens, etc.)
                else:
                    logger.warning(f"Stop reason inesperado: {response.stop_reason}")
                    texto_final = _extraer_texto_respuesta(response.content)
                    if texto_final:
                        historial = historial + [{'role': 'assistant', 'content': texto_final}]
                        return texto_final, historial
                    else:
                        return "He procesado tu solicitud pero necesito mas informacion. Podrias detallar mas tu pregunta?", historial
                        
            except anthropic.APIError as e:
                logger.error(f"Error de API de Anthropic: {e}")
                return f"Hubo un problema de conexion con el servicio de IA. Por favor, intenta de nuevo en unos momentos. Error: {str(e)}", historial
                
            except anthropic.RateLimitError as e:
                logger.error(f"Limite de tasa excedido: {e}")
                return "El servicio esta recibiendo muchas solicitudes. Por favor, espera unos segundos y vuelve a intentarlo.", historial
                
            except anthropic.APIConnectionError as e:
                logger.error(f"Error de conexion: {e}")
                return "No se pudo conectar con el servicio de IA. Verifica tu conexion a internet e intenta nuevamente.", historial
                
            except Exception as e:
                logger.error(f"Error inesperado en turno {turno}: {e}")
                if turno == MAX_TURNOS - 1:
                    return f"Ocurrio un error inesperado: {str(e)}. Por favor, intenta nuevamente.", historial
                continue
        
        # Si llegamos aqui, se excedio el limite de turnos
        logger.warning(f"Limite de {MAX_TURNOS} turnos alcanzado")
        return "He realizado varias iteraciones para procesar tu solicitud. Para no extender demasiado la conversacion, podrias reformular tu pregunta o dividirla en partes mas pequenas?", historial
        
    except Exception as e:
        logger.error(f"Error critico en ejecutar_agente: {e}")
        return f"Error inesperado en el agente: {str(e)}. Por favor, intenta nuevamente.", historial


def _extraer_texto_respuesta(content: List[Any]) -> str:
    """
    Extrae el texto de la respuesta de Claude.
    
    Args:
        content: Lista de bloques de contenido de Claude
    
    Returns:
        Texto extraido o string vacio
    """
    texto = ""
    for bloque in content:
        if hasattr(bloque, 'text') and bloque.text:
            texto += bloque.text
        elif hasattr(bloque, 'type') and bloque.type == "text" and hasattr(bloque, 'text'):
            texto += bloque.text
    
    return texto.strip()


def formatear_respuesta_para_usuario(texto: str) -> str:
    """
    Funcion auxiliar para formatear respuestas antes de enviarlas al usuario.
    Util para limpiar o mejorar el formato.
    
    Args:
        texto: Texto de respuesta del agente
    
    Returns:
        Texto formateado
    """
    # Eliminar espacios extras
    texto = texto.strip()
    
    # Asegurar que no haya lineas vacias al inicio
    if texto.startswith('\n'):
        texto = texto[1:]
    
    # Asegurar que termine con punto o signo de pregunta
    if texto and texto[-1] not in ['.', '?', '!', ':', ';']:
        texto += '.'
    
    return texto


def verificar_estado_agente() -> Dict[str, Any]:
    """
    Verifica que el agente este configurado correctamente.
    Util para debugging.
    
    Returns:
        Diccionario con estado del agente
    """
    estado = {
        "modelo": MODELO,
        "max_turnos": MAX_TURNOS,
        "max_tokens": MAX_TOKENS,
        "max_historial": MAX_HISTORIAL_MENSAJES,
        "anthropic_key_configured": bool(os.getenv("ANTHROPIC_API_KEY")),
        "tools_count": len(TOOLS),
        "tools_names": [tool["name"] for tool in TOOLS],
        "system_prompt_length": len(SYSTEM_PROMPT)
    }
    
    # Verificar que el system prompt no este vacio
    if not SYSTEM_PROMPT:
        estado["warning"] = "SYSTEM_PROMPT esta vacio"
    else:
        estado["system_prompt_preview"] = SYSTEM_PROMPT[:200] + "..."
    
    return estado


def limpiar_historial(historial: List[Dict[str, Any]], max_mensajes: int = 20) -> List[Dict[str, Any]]:
    """
    Limita el historial para no exceder tokens.
    Mantiene los primeros mensajes (contexto) y los ultimos.
    
    Args:
        historial: Historial completo
        max_mensajes: Maximo numero de mensajes a mantener
    
    Returns:
        Historial recortado
    """
    if len(historial) <= max_mensajes:
        return historial
    
    # Mantener primeros 4 mensajes (contexto inicial)
    # y ultimos (max_mensajes - 4) mensajes
    primeros = historial[:4]
    ultimos = historial[-(max_mensajes - 4):]
    
    return primeros + ultimos


if __name__ == "__main__":
    print("=== VERIFICACION DEL AGENTE ===")
    estado = verificar_estado_agente()
    for key, value in estado.items():
        print(f"{key}: {value}")
    
    print("\n" + "="*50)
    
    if estado["anthropic_key_configured"]:
        print("\nEjecutando prueba simple...")
        prueba_historial = []
        respuesta, nuevo_historial = ejecutar_agente(
            "test-id-123",
            "Hola, soy una prueba. Que informacion necesitas para ayudarme?",
            []
        )
        print(f"\nRespuesta:\n{respuesta}")
        print(f"\nHistorial actualizado: {len(nuevo_historial)} mensajes")
    else:
        print("\nNo hay API key configurada. No se puede probar.")