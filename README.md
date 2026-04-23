# 🤖 Agente IMGS-T  
### Consultor de Sostenibilidad Textil basado en IA

---

## 📌 Descripción

Este proyecto consiste en el desarrollo de un **chatbot inteligente basado en inteligencia artificial**, capaz de generar respuestas en tiempo real a partir de las consultas de los usuarios.

El sistema implementa una **arquitectura cliente-servidor**, donde:

- El backend procesa las solicitudes
- Consulta la base de datos
- Se comunica con un modelo de IA para generar respuestas dinámicas

El objetivo es proveer un **agente de consultoría en sostenibilidad** dirigido a **PyMEs textiles colombianas**, permitiendo evaluar su nivel de madurez y generar planes de acción personalizados.

---

## 🧠 Tecnologías utilizadas

- **FastAPI** → Backend y endpoints REST  
- **Anthropic (Claude)** → Motor de inteligencia artificial  
- **Supabase (PostgreSQL)** → Base de datos  
- **Python** → Lógica del sistema  

---

## 🏗️ Arquitectura (C4 Model)

A continuación se presenta el diagrama general de la arquitectura utilizando el estándar **C4 (Nivel de Contenedores)**:

```mermaid
C4Context
    title Nivel de Contenedores - Agente IMGS-T

    Person(user, "Usuario / Frontend", "Interactúa mediante la interfaz de chat")

    System_Boundary(c1, "Sistema Agente IMGS-T") {
        Container(api, "API Server", "Python / FastAPI", "Endpoints REST")
        Container(agent, "Core del Agente", "Python", "Lógica de IA")
        Container(tools, "Tool Executor", "Python", "Ejecución de herramientas")
    }

    SystemDb_Ext(supabase, "Base de Datos", "Supabase / PostgreSQL")
    System_Ext(claude, "Motor LLM", "Anthropic Claude API")

    Rel(user, api, "HTTP/JSON")
    Rel(api, agent, "Procesa solicitudes")
    Rel(agent, claude, "Envía prompts")
    Rel(claude, agent, "Respuestas")
    Rel(agent, tools, "Tool calls")
    Rel(tools, supabase, "Consultas DB")

