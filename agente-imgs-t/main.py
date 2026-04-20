from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import logging
import os
import uvicorn
from datetime import datetime


# Importar el agente
from agent.agent import ejecutar_agente, verificar_estado_agente
from agent.tools import TOOLS

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== CONFIGURACIÓN ==========
API_VERSION = "1.0.0"
API_TITLE = "Agente IMGS-T - Consultor de Sostenibilidad Textil"
API_DESCRIPTION = """
## Agente de IA para consultoría en sostenibilidad para PyMEs textiles colombianas

Este agente utiliza Claude de Anthropic para analizar diagnósticos IMGS-T 
y generar recomendaciones personalizadas para mejorar la madurez en sostenibilidad.

### Tools disponibles:
- **obtener_diagnostico_completo**: Obtiene resultados del diagnóstico
- **buscar_recomendaciones**: Busca acciones específicas por dimensión
- **identificar_brechas**: Identifica las 3 brechas más críticas
- **buscar_normativas**: Busca normativas colombianas aplicables
- **calcular_retorno_inversion**: Estima ROI de inversiones
- **comparar_con_sector**: Compara con benchmarks del sector
- **guardar_plan_accion**: Guarda el plan en la base de datos
- **obtener_recursos_apoyo**: Encuentra programas de apoyo

### Endpoints disponibles:
- **GET /** - Información general
- **GET /health** - Verificar estado del servicio
- **GET /api/agente/estado** - Estado detallado del agente
- **POST /api/agente/chat** - Conversación interactiva
- **POST /api/agente/analizar** - Análisis automático post-diagnóstico
"""

# ========== INICIALIZAR FASTAPI ==========
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ========== CONFIGURACIÓN CORS ==========
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== MODELOS DE DATOS ==========

class ChatRequest(BaseModel):
    organizacion_id: int = Field(..., description="ID de la organización en Supabase")
    mensaje: str = Field(..., description="Mensaje del usuario", min_length=1)
    historial: List[Dict[str, Any]] = Field(default=[], description="Historial de conversación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "organizacion_id": 1,
                "mensaje": "¿Cómo puedo mejorar mi gestión ambiental?",
                "historial": []
            }
        }

class TriggerRequest(BaseModel):
    """Solicitud automática después del diagnóstico"""
    organizacion_id: int = Field(..., description="ID de la organización en Supabase")
    indice_global: float = Field(..., ge=0, le=5, description="Índice global IMGS-T (0-5)")
    nivel_nombre: str = Field(..., description="Nivel de madurez")
    puntajes_dimensiones: Optional[Dict[str, float]] = Field(
        default=None, 
        description="Puntajes por dimensión (opcional)"
    )
    class Config:
        json_schema_extra = {
            "example": {
                "organizacion_id": 1,
                "indice_global": 2.3,
                "nivel_nombre": "Estructurado",
                "puntajes_dimensiones": {
                    "D1_gobernanza": 2.5,
                    "D2_economica": 1.8,
                    "D3_social": 2.0,
                    "D4_ambiental": 1.5,
                    "D5_datos_tecnologia": 1.2
                }
            }
        }

class ChatResponse(BaseModel):
    """Respuesta del chat"""
    respuesta: str = Field(..., description="Respuesta del agente")
    historial: List[Dict[str, Any]] = Field(..., description="Historial actualizado")
    timestamp: str = Field(..., description="Marca de tiempo")
    
class AnalisisResponse(BaseModel):
    """Respuesta del análisis automático"""
    diagnostico_inicial: str = Field(..., description="Diagnóstico generado por el agente")
    historial: List[Dict[str, Any]] = Field(..., description="Historial completo")
    timestamp: str = Field(..., description="Marca de tiempo")

class HealthResponse(BaseModel):
    """Respuesta del endpoint health"""
    status: str
    agente: str
    version: str
    timestamp: str
    tools_disponibles: int

# ========== ENDPOINTS ==========

@app.get(
    "/",
    summary="Información general",
    description="Retorna información básica del servicio"
)
async def root():
    """Endpoint raíz con información del servicio"""
    return {
        "servicio": API_TITLE,
        "version": API_VERSION,
        "descripcion": "Agente consultor de sostenibilidad para PyMEs textiles colombianas",
        "documentacion": "/docs",
        "endpoints": {
            "health": "/health",
            "chat": "/api/agente/chat",
            "analizar": "/api/agente/analizar",
            "estado": "/api/agente/estado"
        },
        "tools_disponibles": len(TOOLS),
        "tools_lista": [tool["name"] for tool in TOOLS],
        "timestamp": datetime.now().isoformat()
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Verificar estado del servicio",
    description="Útil para monitoreo y health checks"
)
async def health():
    """Verifica que el servicio esté funcionando correctamente."""
    estado = verificar_estado_agente()
    
    return HealthResponse(
        status="ok",
        agente="IMGS-T v1.0",
        version=API_VERSION,
        timestamp=datetime.now().isoformat(),
        tools_disponibles=estado.get("tools_count", 0)
    )


@app.get(
    "/api/agente/estado",
    summary="Estado detallado del agente",
    description="Endpoint para debugging y monitoreo"
)
async def estado_agente():
    """
    Retorna información detallada sobre la configuración del agente.
    Útil para debugging y verificar que todo funcione correctamente.
    """
    try:
        estado = verificar_estado_agente()
        estado["timestamp"] = datetime.now().isoformat()
        estado["api_key_configured"] = bool(os.getenv("ANTHROPIC_API_KEY"))
        estado["supabase_url_configured"] = bool(os.getenv("SUPABASE_URL"))
        estado["supabase_key_configured"] = bool(os.getenv("SUPABASE_KEY"))
        return estado
    except Exception as e:
        return {"error": str(e), "timestamp": datetime.now().isoformat()}


@app.post(
    "/api/agente/chat",
    response_model=ChatResponse,
    summary="Conversación con el agente",
    description="Envía un mensaje al agente y recibe una respuesta personalizada"
)
async def chat(req: ChatRequest):
    """
    Endpoint para conversación interactiva con el agente.
    """
    logger.info(f"Chat request - Organización: {req.organizacion_id}")
    logger.info(f"Mensaje: {req.mensaje[:100]}...")
    logger.info(f"Historial previo: {len(req.historial)} mensajes")
    
    try:
        if not req.mensaje or req.mensaje.strip() == "":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El mensaje no puede estar vacío"
            )
        
        respuesta, historial_nuevo = ejecutar_agente(
            req.organizacion_id,
            req.mensaje,
            req.historial
        )
        
        logger.info(f"Respuesta generada ({len(respuesta)} caracteres)")
        
        return ChatResponse(
            respuesta=respuesta,
            historial=historial_nuevo,
            timestamp=datetime.now().isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando el mensaje: {str(e)}"
        )


@app.post(
    "/api/agente/analizar",
    response_model=AnalisisResponse,
    summary="Análisis automático del diagnóstico",
    description="Tesis 1 llama a este endpoint cuando se completa el formulario IMGS-T"
)
async def analizar_diagnostico(req: TriggerRequest):
    """
    Endpoint para análisis automático después de completar el diagnóstico.
    """
    logger.info(f"Análisis diagnóstico - Organización: {req.organizacion_id}")
    logger.info(f"Índice global: {req.indice_global} - Nivel: {req.nivel_nombre}")
    
    if req.puntajes_dimensiones:
        logger.info(f"Puntajes: {req.puntajes_dimensiones}")
    
    try:
        mensaje_inicial = f"""La organización acaba de completar su diagnóstico IMGS-T.

RESULTADOS DEL DIAGNÓSTICO:
- Índice global: {req.indice_global:.2f} / 5.0
- Nivel de madurez: {req.nivel_nombre}
"""

        if req.puntajes_dimensiones:
            mensaje_inicial += "\nPUNTAJES POR DIMENSIÓN:\n"
            nombre_dimensiones = {
                'D1_gobernanza': 'Gobernanza',
                'D2_economica': 'Gestión Económica',
                'D3_social': 'Gestión Social',
                'D4_ambiental': 'Gestión Ambiental',
                'D5_datos_tecnologia': 'Datos y Tecnología'
            }
            for dim, puntaje in req.puntajes_dimensiones.items():
                nombre = nombre_dimensiones.get(dim, dim)
                mensaje_inicial += f"- {nombre}: {puntaje:.2f}/5.0\n"
        
        mensaje_inicial += """

Por favor, analiza estos resultados y genera un diagnóstico inicial que incluya:
1. Un análisis general del perfil de madurez
2. Las 3 brechas más críticas identificadas
3. Recomendaciones priorizadas y accionables (máximo 3)
4. Próximos pasos sugeridos

Recuerda que eres un consultor experto en sostenibilidad para PyMEs textiles colombianas.
Utiliza las tools disponibles para obtener información adicional si la necesitas."""
        
        respuesta, historial = ejecutar_agente(
            req.organizacion_id,
            mensaje_inicial,
            []
        )
        
        logger.info(f"Diagnóstico generado ({len(respuesta)} caracteres)")
        
        return AnalisisResponse(
            diagnostico_inicial=respuesta,
            historial=historial,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error en análisis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generando el diagnóstico: {str(e)}"
        )


@app.get(
    "/api/agente/tools",
    summary="Listar todas las tools disponibles",
    description="Retorna la lista completa de tools que el agente puede usar"
)
async def listar_tools():
    tools_info = []
    for tool in TOOLS:
        tools_info.append({
            "name": tool["name"],
            "description": tool["description"][:200] + "..." if len(tool["description"]) > 200 else tool["description"],
            "parameters": list(tool["input_schema"]["properties"].keys()),
            "required": tool["input_schema"].get("required", [])
        })
    
    return {
        "total_tools": len(TOOLS),
        "tools": tools_info,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/chat", response_class=HTMLResponse)
async def chat_ui():
    with open("chat.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get(
    "/api/agente/test-db",
    summary="Probar conexión a Supabase",
    description="Verifica que la conexión a la base de datos funcione correctamente"
)
async def test_database():
    """Prueba la conexión a Supabase."""
    try:
        from db.supabase_client import supabase
        result = supabase.table('empresas').select('*').limit(1).execute()
        return {
            "status": "success",
            "message": "Conexión a Supabase exitosa",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error de conexión: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }


# ========== MANEJADORES DE ERRORES GLOBALES ==========

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detalle": "Error en la solicitud",
            "timestamp": datetime.now().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Error no manejado: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Error interno del servidor",
            "detalle": str(exc) if os.getenv("DEBUG", "False") == "True" else "Contacta al administrador",
            "timestamp": datetime.now().isoformat()
        }
    )


# ========== MIDDLEWARE DE LOGGING ==========

@app.middleware("http")
async def log_requests(request, call_next):
    start_time = datetime.now()
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    duration = (datetime.now() - start_time).total_seconds()
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.2f}s")
    response.headers["X-Response-Time"] = str(duration)
    return response


# ========== INICIO DEL SERVIDOR ==========

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print("\n" + "=" * 60)
    print("🚀 AGENTE IMGS-T - Consultor de Sostenibilidad Textil")
    print("=" * 60)
    print(f"   Versión: {API_VERSION}")
    print(f"   Puerto: {port}")
    print(f"\n   📚 Documentación: http://localhost:{port}/docs")
    print(f"   🔍 Health check: http://localhost:{port}/health")
    print(f"   🔧 Estado agente: http://localhost:{port}/api/agente/estado")
    print(f"   💬 Chat UI: http://localhost:{port}/chat")
    print(f"   🛠️  Tools disponibles: {len(TOOLS)}")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )