TOOLS = [
    {
        "name": "obtener_diagnostico_completo",
        "description": "OBLIGATORIO: Úsala SIEMPRE que el usuario pregunte por el nombre de su empresa, su diagnóstico o cualquier información de su organización. Consulta la base de datos y retorna el nombre de la empresa y sus puntajes. No respondas sin llamar a esta herramienta. El parámetro organizacion_id es el número que el usuario te proporciona (ej: '2').",
        "input_schema": {
            "type": "object",
            "properties": {
                "organizacion_id": {
                    "type": "string",
                    "description": "ID numérico de la organización (ej: '2')"
                }
            },
            "required": ["organizacion_id"]
        }
    },
    {
        "name": "buscar_recomendaciones",
        "description": "Busca recomendaciones específicas en la base de conocimiento por dimensión y nivel de madurez.",
        "input_schema": {
            "type": "object",
            "properties": {
                "dimension": {
                    "type": "string",
                    "enum": ["D1", "D2", "D3", "D4", "D5"]
                },
                "nivel_actual": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5
                }
            },
            "required": ["dimension", "nivel_actual"]
        }
    },
    {
        "name": "identificar_brechas",
        "description": "Identifica las 3 brechas más críticas a partir de los puntajes por dimensión.",
        "input_schema": {
            "type": "object",
            "properties": {
                "puntajes": {
                    "type": "object",
                    "properties": {
                        "D1_gobernanza": {"type": "number"},
                        "D2_economica": {"type": "number"},
                        "D3_social": {"type": "number"},
                        "D4_ambiental": {"type": "number"},
                        "D5_datos_tecnologia": {"type": "number"}
                    }
                }
            },
            "required": ["puntajes"]
        }
    },
    {
        "name": "guardar_plan_accion",
        "description": "Guarda un plan de acción en la base de datos para seguimiento futuro.",
        "input_schema": {
            "type": "object",
            "properties": {
                "organizacion_id": {"type": "string"},
                "plan": {"type": "string"}
            },
            "required": ["organizacion_id", "plan"]
        }
    }
]