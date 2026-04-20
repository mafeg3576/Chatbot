"""
BASE DE CONOCIMIENTO ESPECIALIZADA PARA SOSTENIBILIDAD TEXTIL EN COLOMBIA
IMGS-T - Agente Consultor

Esta base de conocimiento es el corazón del agente. Contiene recomendaciones
específicas, accionables y contextualizadas para PyMEs textiles colombianas.

Estructura: BASE_CONOCIMIENTO[dimensión][nivel_actual] = lista de recomendaciones
Cada recomendación incluye:
- acción: Qué hacer concretamente
- por_que: Beneficio esperado
- como_empezar: Primer paso accionable
- recursos: Inversión estimada
- plazo: Tiempo sugerido
- contexto_colombiano: Relevancia local
"""

BASE_CONOCIMIENTO = {
    # ========== D1: GOBERNANZA, MATERIALIDAD, RIESGOS Y OPORTUNIDADES ==========
    'D1': {
        1: [  # Nivel 1 → Nivel 2: Reactivo a Inicial
            {
                'accion': 'Designar un responsable interno de sostenibilidad',
                'por_que': 'Tener una persona responsable da continuidad a las iniciativas y evita que dependan de voluntarios',
                'como_empezar': 'Asigna esta función a un jefe de producción o administrativo existente, con 4 horas semanales',
                'recursos': '0 COP - Reasignación de tiempo',
                'plazo': '1 mes',
                'contexto_colombiano': 'Muchas PyMEs textiles colombianas empiezan así antes de tener un área dedicada'
            },
            {
                'accion': 'Realizar taller de identificación de impactos ambientales',
                'por_que': 'Conocer los impactos es el primer paso para gestionarlos',
                'como_empezar': 'Convoca a operarios de tintura, corte y confección por 2 horas',
                'recursos': '100.000 COP - Refrigerio',
                'plazo': '2 semanas',
                'contexto_colombiano': 'El sector textil colombiano impacta principalmente agua, energía y químicos'
            },
            {
                'accion': 'Documentar riesgos regulatorios ambientales básicos',
                'por_que': 'Evita multas y sanciones por incumplimiento normativo',
                'como_empezar': 'Crea un archivo con Decreto 1076/2015 y Resolución 1402/2018 del IDEAM',
                'recursos': '0 COP - Investigación documental',
                'plazo': '2 semanas',
                'contexto_colombiano': 'La normativa ambiental colombiana exige registro de residuos peligrosos'
            }
        ],
        2: [  # Nivel 2 → Nivel 3: Inicial a Estructurado
            {
                'accion': 'Implementar matriz de materialidad básica',
                'por_que': 'Prioriza los temas más importantes para la empresa y sus grupos de interés',
                'como_empezar': 'Identifica 3 grupos de interés (trabajadores, clientes, comunidad) y pregunta sus prioridades',
                'recursos': '200.000 COP - Encuestas',
                'plazo': '2 meses',
                'contexto_colombiano': 'GRI 3 recomienda este enfoque para PyMEs'
            },
            {
                'accion': 'Establecer reuniones trimestrales de sostenibilidad con gerencia',
                'por_que': 'La alta dirección debe revisar avances y tomar decisiones',
                'como_empezar': 'Agenda 1 hora cada 3 meses en la reunión de gerencia existente',
                'recursos': '0 COP - Reasignación de tiempo',
                'plazo': 'Inmediato',
                'contexto_colombiano': 'Empresas líderes en Colombia como Fabricato y Enka tienen comités formales'
            },
            {
                'accion': 'Definir 3 indicadores clave de sostenibilidad',
                'por_que': 'Lo que no se mide, no se mejora',
                'como_empezar': 'Selecciona: consumo de agua por kg tela, % residuos reciclados, rotación de personal',
                'recursos': '0 COP - Definición interna',
                'plazo': '1 mes',
                'contexto_colombiano': 'Indicadores alineados con ODS 6 (agua), 12 (producción), 8 (trabajo)'
            }
        ],
        3: [  # Nivel 3 → Nivel 4: Estructurado a Integrado
            {
                'accion': 'Integrar sostenibilidad al plan estratégico',
                'por_que': 'La sostenibilidad deja de ser un proyecto aislado y se vuelve parte del negocio',
                'como_empezar': 'Incluye objetivos de sostenibilidad en el próximo plan anual',
                'recursos': '0 COP - Planificación estratégica',
                'plazo': '3 meses',
                'contexto_colombiano': 'ANDI promueve la integración de sostenibilidad en la estrategia empresarial'
            },
            {
                'accion': 'Implementar proceso de doble materialidad',
                'por_que': 'Evalúa impacto de la empresa en el entorno Y del entorno en la empresa',
                'como_empezar': 'Contrata consultor especializado por 3 meses',
                'recursos': '5-8 millones COP',
                'plazo': '3-4 meses',
                'contexto_colombiano': 'Requisito para reporte GRI y estándares internacionales'
            },
            {
                'accion': 'Crear comité de sostenibilidad interdisciplinario',
                'por_que': 'La sostenibilidad requiere todas las áreas: producción, RH, compras, finanzas',
                'como_empezar': 'Invita a un representante de cada área a reuniones mensuales',
                'recursos': '0 COP - Reasignación de tiempo',
                'plazo': '2 meses',
                'contexto_colombiano': 'Práctica común en empresas con certificación ISO 14001'
            }
        ],
        4: [  # Nivel 4 → Nivel 5: Integrado a Estratégico
            {
                'accion': 'Publicar reporte de sostenibilidad anual',
                'por_que': 'Demuestra transparencia y atrae inversión/mercados',
                'como_empezar': 'Utiliza estándar GRI Core y publica en página web',
                'recursos': '3-5 millones COP',
                'plazo': '4 meses',
                'contexto_colombiano': 'Requerido para empresas que exportan a mercados exigentes'
            },
            {
                'accion': 'Establecer metas alineadas con ODS',
                'por_que': 'Posiciona a la empresa como referente y abre oportunidades de negocio',
                'como_empezar': 'Selecciona 3 ODS donde puedes tener mayor impacto',
                'recursos': '0 COP - Definición estratégica',
                'plazo': '2 meses',
                'contexto_colombiano': 'ODS 6 (agua), 8 (trabajo decente), 12 (producción) son prioritarios'
            },
            {
                'accion': 'Participar en iniciativas sectoriales de sostenibilidad',
                'por_que': 'Aprende de pares y posiciona a la empresa como líder',
                'como_empezar': 'Afíliate a Pacto Global Colombia o Mesa Sectorial Textil de la ANDI',
                'recursos': '1-2 millones COP/año',
                'plazo': '3 meses',
                'contexto_colombiano': 'Pacto Global Colombia tiene +1,500 empresas afiliadas'
            }
        ]
    },

    # ========== D2: GESTIÓN ECONÓMICA SOSTENIBLE ==========
    'D2': {
        1: [  # Nivel 1 → Nivel 2
            {
                'accion': 'Calcular costo real de agua y energía en producción',
                'por_que': 'Identificar costos ocultos que pueden reducirse significativamente',
                'como_empezar': 'Revisa facturas de servicios públicos de últimos 6 meses',
                'recursos': '0 COP - Análisis interno',
                'plazo': '1 mes',
                'contexto_colombiano': 'Empresas textiles pueden ahorrar 15-30% en costos de servicios'
            },
            {
                'accion': 'Identificar proveedores clave y evaluar prácticas sostenibles',
                'por_que': 'La cadena de valor representa hasta 70% del impacto ambiental',
                'como_empezar': 'Crea lista de 5 principales proveedores y solicita sus políticas ambientales',
                'recursos': '0 COP - Gestión comercial',
                'plazo': '2 meses',
                'contexto_colombiano': 'Mercados internacionales exigen trazabilidad en la cadena'
            },
            {
                'accion': 'Registrar ahorros por eficiencia mensualmente',
                'por_que': 'Visibilizar beneficios económicos de la sostenibilidad',
                'como_empezar': 'Crea hoja Excel con: inversión, ahorro mensual, retorno de inversión',
                'recursos': '0 COP',
                'plazo': 'Inmediato',
                'contexto_colombiano': 'Incentivos tributarios Ley 2277/2022 para inversiones ambientales'
            }
        ],
        2: [  # Nivel 2 → Nivel 3
            {
                'accion': 'Implementar compras sostenibles con criterios ambientales',
                'por_que': 'Influye positivamente en la cadena de valor y reduce riesgos',
                'como_empezar': 'Incluye cláusulas ambientales en contratos nuevos',
                'recursos': '0 COP',
                'plazo': '3 meses',
                'contexto_colombiano': 'Colombia tiene política nacional de compras sostenibles'
            },
            {
                'accion': 'Realizar análisis de ciclo de vida básico',
                'por_que': 'Identifica impactos desde materia prima hasta disposición final',
                'como_empezar': 'Contrata consultor especializado para producto principal',
                'recursos': '3-5 millones COP',
                'plazo': '3 meses',
                'contexto_colombiano': 'Base para certificación Sello Ambiental Colombiano'
            },
            {
                'accion': 'Establecer metas de eficiencia energética',
                'por_que': 'Reduce costos operativos y huella de carbono',
                'como_empezar': 'Propón reducir 10% consumo en 12 meses',
                'recursos': '0 COP',
                'plazo': '1 mes',
                'contexto_colombiano': 'Impuesto al carbono motiva reducción de consumo energético'
            }
        ],
        3: [  # Nivel 3 → Nivel 4
            {
                'accion': 'Certificarse en Sello Ambiental Colombiano',
                'por_que': 'Reconocimiento oficial que abre mercados nacionales e internacionales',
                'como_empezar': 'Contacta al IDEAM para conocer requisitos',
                'recursos': '5-10 millones COP',
                'plazo': '6-8 meses',
                'contexto_colombiano': 'El Sello Ambiental Colombiano es el estándar oficial del país'
            },
            {
                'accion': 'Desarrollar portafolio de productos sostenibles',
                'por_que': 'Diferencia en mercado y captura nuevos clientes',
                'como_empezar': 'Identifica 1 línea de producto para certificar',
                'recursos': 'Depende del producto',
                'plazo': '4-6 meses',
                'contexto_colombiano': 'Alta demanda de moda sostenible en mercados europeos'
            },
            {
                'accion': 'Implementar economía circular con clientes',
                'por_que': 'Reduce residuos y crea nuevos ingresos',
                'como_empezar': 'Programa de recolección de prendas usadas',
                'recursos': '1-2 millones COP',
                'plazo': '3 meses',
                'contexto_colombiano': 'Empresas como Patagonia y Decathlon lideran este modelo'
            }
        ]
    },

    # ========== D3: GESTIÓN SOCIAL ==========
    'D3': {
        1: [  # Nivel 1 → Nivel 2
            {
                'accion': 'Realizar encuesta de satisfacción laboral',
                'por_que': 'Identifica áreas de mejora en clima organizacional',
                'como_empezar': 'Encuesta anónima a todo el personal (10 preguntas)',
                'recursos': '0 COP - Google Forms',
                'plazo': '1 mes',
                'contexto_colombiano': 'El sector textil tiene alta rotación; mejorar condiciones reduce costos'
            },
            {
                'accion': 'Capacitar en manejo seguro de químicos',
                'por_que': 'Protege salud de trabajadores y evita accidentes',
                'como_empezar': 'Capacitación de 2 horas con operarios de tintura',
                'recursos': '100.000 COP',
                'plazo': '2 semanas',
                'contexto_colombiano': 'Exigencia de ARL y requisito legal del Ministerio de Trabajo'
            },
            {
                'accion': 'Documentar quejas y reclamos de comunidad',
                'por_que': 'Previene conflictos vecinales y mejora relacionamiento',
                'como_empezar': 'Libro de quejas físico o formulario digital',
                'recursos': '0 COP',
                'plazo': 'Inmediato',
                'contexto_colombiano': 'Empresas textiles urbanas tienen comunidades cercanas'
            }
        ],
        2: [  # Nivel 2 → Nivel 3
            {
                'accion': 'Implementar programa de salud ocupacional',
                'por_que': 'Reduce ausentismo y mejora productividad',
                'como_empezar': 'Apóyate en ARL para diseño de programa',
                'recursos': '0 COP - Apoyo ARL',
                'plazo': '2 meses',
                'contexto_colombiano': 'ARL están obligadas a asesorar empresas afiliadas'
            },
            {
                'accion': 'Programa de formación continua en sostenibilidad',
                'por_que': 'Desarrolla capacidades y compromiso del equipo',
                'como_empezar': 'Cursos SENA virtuales sobre gestión ambiental',
                'recursos': '0 COP - SENA',
                'plazo': '3 meses',
                'contexto_colombiano': 'SENA ofrece cursos gratuitos para el sector textil'
            },
            {
                'accion': 'Jornada de diálogo con comunidad local',
                'por_que': 'Construye confianza y reduce conflictos',
                'como_empezar': 'Invita a líderes comunales a recorrido por planta',
                'recursos': '200.000 COP',
                'plazo': '2 meses',
                'contexto_colombiano': 'Mejora reputación y relacionamiento con el municipio'
            }
        ],
        3: [  # Nivel 3 → Nivel 4
            {
                'accion': 'Implementar programa de bienestar integral',
                'por_que': 'Atrae y retiene talento en sector competitivo',
                'como_empezar': 'Beneficios: horarios flexibles, auxilio educativo, pausas activas',
                'recursos': '500.000 COP/mes por 20 empleados',
                'plazo': '3 meses',
                'contexto_colombiano': 'Empresas con buen clima reducen rotación 30%'
            },
            {
                'accion': 'Establecer alianzas con instituciones educativas',
                'por_que': 'Forma futuros talentos y fortalece comunidad',
                'como_empezar': 'Convenio con SENA o universidad local para pasantías',
                'recursos': '0 COP',
                'plazo': '4 meses',
                'contexto_colombiano': 'Apoyo a formación técnica en confección'
            },
            {
                'accion': 'Desarrollar política de diversidad e inclusión',
                'por_que': 'Amplía talento y mejora reputación',
                'como_empezar': 'Incluye mujeres, población LGBTIQ+, personas con discapacidad',
                'recursos': '0 COP',
                'plazo': '2 meses',
                'contexto_colombiano': 'Mercados internacionales valoran diversidad'
            }
        ]
    },

    # ========== D4: GESTIÓN AMBIENTAL ==========
    'D4': {
        1: [  # Nivel 1 → Nivel 2
            {
                'accion': 'Instalar medidores de agua en procesos de tintura',
                'por_que': 'El consumo excesivo es el mayor impacto ambiental del sector textil',
                'como_empezar': 'Instala medidores en 3 máquinas de mayor consumo',
                'recursos': '500.000-1.000.000 COP',
                'plazo': '1 mes',
                'contexto_colombiano': 'El sector textil consume hasta 200 litros de agua por kg de tela'
            },
            {
                'accion': 'Crear registro mensual de consumos',
                'por_que': 'Medir es el primer paso para reducir',
                'como_empezar': 'Hoja Excel con: agua (m3), energía (kWh), residuos (kg)',
                'recursos': '0 COP',
                'plazo': 'Inmediato',
                'contexto_colombiano': 'Base para reportes regulatorios al IDEAM'
            },
            {
                'accion': 'Revisar manejo de residuos peligrosos',
                'por_que': 'Evita multas y daños ambientales',
                'como_empezar': 'Contrata gestor autorizado para colorantes y químicos',
                'recursos': '300.000-500.000 COP/mes',
                'plazo': '2 meses',
                'contexto_colombiano': 'Resolución 1402/2018 exige reporte semestral al IDEAM'
            }
        ],
        2: [  # Nivel 2 → Nivel 3
            {
                'accion': 'Implementar recirculación de agua en tintura',
                'por_que': 'Reduce consumo 30-50% y ahorra costos',
                'como_empezar': 'Sistema de filtrado básico para reutilizar agua de enjuagues',
                'recursos': '2-5 millones COP',
                'plazo': '3 meses',
                'contexto_colombiano': 'FONAGUA financia proyectos de eficiencia hídrica'
            },
            {
                'accion': 'Calcular huella de carbono básica',
                'por_que': 'Identifica principales fuentes de emisiones',
                'como_empezar': 'Calculadora IDEAM o apoyo consultor básico',
                'recursos': '1-2 millones COP',
                'plazo': '2 meses',
                'contexto_colombiano': 'Metodología GHG Protocol Scope 1 y 2'
            },
            {
                'accion': 'Establecer metas de reducción de consumo',
                'por_que': 'Concentra esfuerzos y mide avances',
                'como_empezar': 'Meta: reducir 15% agua y 10% energía en 12 meses',
                'recursos': '0 COP',
                'plazo': '1 mes',
                'contexto_colombiano': 'Beneficios tributarios por cumplimiento de metas'
            }
        ],
        3: [  # Nivel 3 → Nivel 4
            {
                'accion': 'Certificación ISO 14001',
                'por_que': 'Estándar internacional que demuestra gestión ambiental seria',
                'como_empezar': 'Contrata consultor especializado (6 meses)',
                'recursos': '10-15 millones COP',
                'plazo': '6-8 meses',
                'contexto_colombiano': 'Requerido por grandes compradores internacionales'
            },
            {
                'accion': 'Implementar sistema de tratamiento de aguas residuales',
                'por_que': 'Cumple normativa y reduce impacto hídrico',
                'como_empezar': 'Planta de tratamiento físico-químico básica',
                'recursos': '20-50 millones COP',
                'plazo': '6-12 meses',
                'contexto_colombiano': 'Requisito para vertimientos según Resolución 631/2015'
            },
            {
                'accion': 'Programa de economía circular con proveedores',
                'por_que': 'Reduce residuos y genera nuevos ingresos',
                'como_empezar': 'Recolección de retazos para reciclaje o reutilización',
                'recursos': '1-2 millones COP',
                'plazo': '3 meses',
                'contexto_colombiano': 'Crecimiento de mercado de textiles reciclados en Colombia'
            }
        ],
        4: [  # Nivel 4 → Nivel 5
            {
                'accion': 'Implementar ISO 50001 - Gestión de Energía',
                'por_que': 'Reduce costos energéticos 10-20% y huella de carbono',
                'como_empezar': 'Sistema de gestión energética con metas de eficiencia',
                'recursos': '8-12 millones COP',
                'plazo': '6 meses',
                'contexto_colombiano': 'Beneficios tributarios por inversiones en eficiencia energética'
            },
            {
                'accion': 'Alcanzar carbono neutralidad',
                'por_que': 'Posiciona como líder en sostenibilidad',
                'como_empezar': 'Medir, reducir y compensar emisiones',
                'recursos': '5-10 millones COP/año',
                'plazo': '12 meses',
                'contexto_colombiano': 'Mercados internacionales valoran productos carbono neutral'
            },
            {
                'accion': 'Certificación AWS Standard (Agua)',
                'por_que': 'Demuestra gestión responsable del recurso hídrico',
                'como_empezar': 'Implementar buenas prácticas de gestión del agua',
                'recursos': '5-8 millones COP',
                'plazo': '8 meses',
                'contexto_colombiano': 'Estándar internacional reconocido por GRI'
            }
        ]
    },

    # ========== D5: DATOS Y TECNOLOGÍA (DIMENSIÓN HABILITADORA) ==========
    'D5': {
        1: [  # Nivel 1 → Nivel 2
            {
                'accion': 'Centralizar datos en hoja de cálculo',
                'por_que': 'Sin datos básicos no hay base para mejorar ninguna dimensión',
                'como_empezar': 'Excel con: consumos (agua, energía), residuos, producción',
                'recursos': '0 COP',
                'plazo': '2 semanas',
                'contexto_colombiano': '80% de PyMEs textiles colombianas empiezan así'
            },
            {
                'accion': 'Registro fotográfico de medidores',
                'por_que': 'Evita pérdida de datos y verifica lecturas',
                'como_empezar': 'Carpeta compartida en Drive con fotos mensuales',
                'recursos': '0 COP',
                'plazo': 'Inmediato',
                'contexto_colombiano': 'Útil para auditorías y reportes al IDEAM'
            },
            {
                'accion': 'Definir qué datos recolectar antes de invertir',
                'por_que': 'Evita comprar herramientas que no se usan',
                'como_empezar': 'Lista: 5 indicadores más relevantes para su negocio',
                'recursos': '0 COP',
                'plazo': '1 mes',
                'contexto_colombiano': 'Muchas PyMEs invierten en software sin definir necesidades'
            }
        ],
        2: [  # Nivel 2 → Nivel 3
            {
                'accion': 'Implementar Google Sheets con fórmulas automáticas',
                'por_que': 'Reduce errores y tiempo de cálculo',
                'como_empezar': 'Configurar fórmulas: consumo unitario, % variación, metas',
                'recursos': '0 COP',
                'plazo': '1 mes',
                'contexto_colombiano': 'Herramienta gratuita y accesible para PyMEs'
            },
            {
                'accion': 'Dashboard en Google Looker Studio',
                'por_que': 'Visualiza datos y facilita toma de decisiones',
                'como_empezar': 'Gráficos: tendencias mensuales, comparación metas, alertas',
                'recursos': '0 COP',
                'plazo': '2 meses',
                'contexto_colombiano': 'Plataforma gratuita de Google'
            },
            {
                'accion': 'Automatizar cálculo del IMGS-T',
                'por_que': 'Facilita seguimiento continuo de avances',
                'como_empezar': 'Hoja Excel que calcula puntajes automáticamente',
                'recursos': '0 COP',
                'plazo': '1 mes',
                'contexto_colombiano': 'Permite evaluar mejora cada 6 meses'
            }
        ],
        3: [  # Nivel 3 → Nivel 4
            {
                'accion': 'Implementar software especializado en gestión ambiental',
                'por_que': 'Gestiona grandes volúmenes de datos y genera reportes automáticos',
                'como_empezar': 'Evaluar opciones: SGS, Enablon, soluciones locales',
                'recursos': '5-15 millones COP/año',
                'plazo': '3-4 meses',
                'contexto_colombiano': 'Facilita reportes regulatorios al IDEAM'
            },
            {
                'accion': 'Sistema integrado de gestión con indicadores en tiempo real',
                'por_que': 'Permite reacción inmediata ante desviaciones',
                'como_empezar': 'Dashboards en tiempo real con datos de medidores',
                'recursos': '10-20 millones COP',
                'plazo': '6 meses',
                'contexto_colombiano': 'Tecnología 4.0 en el sector textil colombiano'
            },
            {
                'accion': 'Capacitar personal en análisis de datos',
                'por_que': 'Los datos son útiles si se interpretan correctamente',
                'como_empezar': 'Cursos en Excel avanzado, Power BI, análisis de datos',
                'recursos': '500.000-1.000.000 COP por persona',
                'plazo': '3 meses',
                'contexto_colombiano': 'SENA ofrece formación gratuita en datos'
            }
        ],
        4: [  # Nivel 4 → Nivel 5
            {
                'accion': 'Implementar Power BI o Tableau',
                'por_que': 'Análisis avanzado de datos para decisiones estratégicas',
                'como_empezar': 'Conectar datos de producción, sostenibilidad, costos',
                'recursos': '3-5 millones COP/año',
                'plazo': '3 meses',
                'contexto_colombiano': 'Empresas líderes del sector usan estas herramientas'
            },
            {
                'accion': 'Sistema de alertas tempranas',
                'por_que': 'Identifica desviaciones antes de que sean críticas',
                'como_empezar': 'Alertas automáticas cuando consumo supera meta',
                'recursos': '5-10 millones COP',
                'plazo': '4 meses',
                'contexto_colombiano': 'Prevención de multas por incumplimiento normativo'
            },
            {
                'accion': 'Integrar datos con sistemas ERP',
                'por_que': 'Sostenibilidad integrada al negocio principal',
                'como_empezar': 'Conectar indicadores ambientales a SAP, Odoo o similar',
                'recursos': '10-20 millones COP',
                'plazo': '6-8 meses',
                'contexto_colombiano': 'Nivel de madurez tecnológica para exportación'
            }
        ]
    }
}


# ========== FUNCIONES AUXILIARES PARA CONSULTAR ==========

def obtener_recomendaciones(dimension: str, nivel_actual: int) -> list:
    """
    Obtiene recomendaciones para una dimensión y nivel específico.
    
    Args:
        dimension: D1, D2, D3, D4, D5
        nivel_actual: Nivel actual (1-5)
    
    Returns:
        Lista de recomendaciones con estructura detallada
    """
    if nivel_actual >= 5:
        return []  # Ya está en nivel máximo
    
    recomendaciones = BASE_CONOCIMIENTO.get(dimension, {}).get(nivel_actual, [])
    return recomendaciones


def obtener_contexto_colombiano(tema: str) -> str:
    """
    Obtiene contexto colombiano específico para un tema.
    
    Args:
        tema: agua, energia, quimicos, normativa, incentivos, programas
    
    Returns:
        Texto con contexto colombiano
    """
    contextos = {
        'agua': "En Colombia, el sector textil consume aproximadamente 200 litros de agua por kg de tela. La gestión eficiente del agua puede generar ahorros del 15-30% y hay apoyo de FONAGUA para proyectos de eficiencia hídrica.",
        
        'energia': "El impuesto al carbono (Ley 2277 de 2022) grava el consumo de energía. Reducir consumo energético tiene beneficios económicos directos y hay exclusión de IVA para equipos de eficiencia energética.",
        
        'quimicos': "La Resolución 1402 de 2018 del IDEAM regula el manejo de residuos peligrosos. La correcta gestión de colorantes y químicos evita multas de hasta 5,000 salarios mínimos.",
        
        'normativa': "Decreto 1076 de 2015 (Decreto Único Ambiental) compila toda la normativa ambiental colombiana. Las PyMEs deben cumplir requisitos básicos de licenciamiento ambiental y reporte de residuos.",
        
        'incentivos': "Ley 2277 de 2022 ofrece deducción del 25% en inversiones ambientales. Exclusión de IVA para equipos de control ambiental (medidores, filtros, sistemas de tratamiento).",
        
        'programas': "Colombia Productiva, iNNpulsa Colombia, SENA, Cámaras de Comercio ofrecen asistencia técnica y financiamiento para sostenibilidad en PyMEs textiles. FONAGUA apoya proyectos de eficiencia hídrica."
    }
    
    return contextos.get(tema.lower(), "Consulta normativas específicas en el Ministerio de Ambiente y Desarrollo Sostenible o el IDEAM.")


# ========== PARA PRUEBAS ==========
if __name__ == "__main__":
    print("="*60)
    print("BASE DE CONOCIMIENTO IMGS-T - VERIFICACIÓN")
    print("="*60)
    
    total_recomendaciones = 0
    for dim, niveles in BASE_CONOCIMIENTO.items():
        for nivel, recs in niveles.items():
            total_recomendaciones += len(recs)
            print(f"{dim} Nivel {nivel}: {len(recs)} recomendaciones")
    
    print(f"\n✅ Total de recomendaciones: {total_recomendaciones}")
    
    # Prueba de una recomendación
    print("\n" + "="*60)
    print("EJEMPLO DE RECOMENDACIÓN (D4 Nivel 1):")
    print("="*60)
    ejemplo = obtener_recomendaciones('D4', 1)[0]
    print(f"Acción: {ejemplo['accion']}")
    print(f"Por qué: {ejemplo['por_que']}")
    print(f"Cómo empezar: {ejemplo['como_empezar']}")
    print(f"Recursos: {ejemplo['recursos']}")
    print(f"Plazo: {ejemplo['plazo']}")