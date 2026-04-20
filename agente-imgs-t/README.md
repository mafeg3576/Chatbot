# Agente IMGS-T - Consultor de Sostenibilidad Textil

Este proyecto provee un agente de IA para consultoría en sostenibilidad dirigido a PyMEs textiles colombianas. Utiliza FastAPI para los endpoints de la API, integra a Anthropic (Claude) como motor LLM central, y utiliza Supabase como base de datos para almacenar el contexto y los resultados de los diagnósticos.

## Arquitectura (C4 Model)

A continuación se presenta el diagrama general de la arquitectura utilizando el estándar C4 (Nivel de Contenedores).

```mermaid
C4Context
    title Nivel de Contenedores - Agente IMGS-T

    Person(user, "Usuario / Frontend", "Interactúa mediante la interfaz de chat (HTML) o la aplicación principal (Tesis 1).")

    System_Boundary(c1, "Sistema Agente IMGS-T") {
        Container(api, "API Server", "Python / FastAPI", "Provee endpoints REST (/chat, /analizar, /estado). Gestiona las peticiones HTTP y Middlewares.")
        Container(agent, "Core del Agente", "Python", "Controla el bucle de razonamiento de la IA, historial y parseo de peticiones.")
        Container(tools, "Tool Executor", "Python", "Ejecuta las acciones o 'herramientas' que la IA decide usar.")
    }

    SystemDb_Ext(supabase, "Base de Datos", "Supabase / PostgreSQL", "Guarda empresas, respuestas del diagnóstico, niveles de madurez y planes de acción.")
    System_Ext(claude, "Motor LLM", "Anthropic Claude API", "Infiere respuestas y decide cuándo consultar herramientas locales.")

    Rel(user, api, "Llama a los endpoints", "HTTPS/JSON")
    Rel(api, agent, "Delega la conversación o análisis de diagnóstico", "Llamada Python")
    Rel(agent, claude, "Envía contexto, prompts y herramientas disponibles", "API HTTP")
    Rel(claude, agent, "Devuelve texto o peticiones de uso de herramientas (Tool calls)", "JSON")
    Rel(agent, tools, "Enruta la ejecución si el modelo pide una herramienta", "Llamada Python")
    Rel(tools, supabase, "Consulta DB: obtener_diagnostico, guardar_plan_accion...", "PostgREST API")
```

### Componentes Principales

1. **API Server (FastAPI)**: El punto de entrada (`main.py`). Se encarga de procesar las URLs web, validar esquemas con Pydantic, servir la UI basica `chat.html` y manejar excepciones.
2. **Core del Agente (agent.py)**: Orquesta la interacción con Anthropic. Implementa un bucle donde le envía el historial a Claude. Si Claude emite intenciones de invocar herramientas ("tool_use"), se procesan internamente.
3. **Tool Executor (tool_executor.py)**: Cuando Claude decide que necesita datos adicionales (como las preguntas respondidas y resultados del usuario), delega a este módulo para obtenerlos o guardarlos.
4. **Supabase Client**: Se usa para comunicarse a la capa de persistencia remota (Postgres), consultar el estado de la empresa y poder generar los planes de acción a la medida.
5. **Base de Conocimiento (knowledge/)**: Una base documental interna estandarizada (`recomendaciones.py`) que las herramientas consultan (ej. `_buscar_recomendaciones`).

## Uso Local

1. Instalar requerimientos: `pip install -r requirements.txt`
2. Configurar variables en un `.env` (como las claves de SUPABASE y ANTHROPIC_API_KEY).
3. Iniciar servidor: `python main.py` o mediante uvicorn estándar.
