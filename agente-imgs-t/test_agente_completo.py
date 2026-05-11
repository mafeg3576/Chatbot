from agent.agent import ejecutar_agente

organizacion_id = 'test-pyme-001'
mensaje = """
La organización acaba de completar su diagnóstico IMGS-T.
Índice global: 0.8. Nivel: 1 - Reactivo/Incipiente.
Puntajes: D1=0.9, D2=0.7, D3=0.8, D4=0.6, D5=1.0
Por favor analiza los resultados y genera recomendaciones para la dimensión económica (D2).
"""

respuesta, historial = ejecutar_agente(organizacion_id, mensaje, [])
print("=== RESPUESTA DEL AGENTE ===\n")
print(respuesta)