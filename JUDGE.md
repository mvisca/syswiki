# ═══════════════════════════════════════════════════════════════
# EL JUEZ — Framework de Evaluación Sistémico-Causal
# ═══════════════════════════════════════════════════════════════
#
# Aplica a: SPEC.md (especificación del sistema) y UX-UI-BRIEF.md
#            (brief de diseño de experiencia)
#
# Cada dimensión evalúa un aspecto del documento usando los
# propios criterios del modelo sistémico-causal.
#
# Escala de puntuación:
#   0 = Ausente — el criterio no está contemplado en absoluto
#   1 = Mínimo — se menciona pero sin desarrollo
#   2 = Parcial — cubierto parcialmente, con carencias importantes
#   3 = Aceptable — cubierto, funcional, pero mejorable
#   4 = Bueno — bien cubierto, con profundidad
#   5 = Excelente — ejemplar, el criterio está completamente integrado
#
# Ponderación: todas las dimensiones pesan igual (20% cada una).
# Nivel "alto" = puntuación ≥ 4.0 en cada dimensión.
# ═══════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────
# DIMENSIÓN MATERIAL
# ─────────────────────────────────────────────────────────────
# Evalúa si el documento identifica y describe correctamente
# los COMPONENTES del sistema: entidades, datos, interfaces,
# elementos tangibles que lo constituyen.
# ─────────────────────────────────────────────────────────────

## M1 — Identidad de los componentes
El documento identifica explícitamente los componentes del sistema
(entidades, objetos, interfaces, módulos) con nombres y propósito claro.
- ¿Nombra las entidades fundamentales? (Concepto, Causa, Relación...)
- ¿Describe sus atributos esenciales?
- ¿Son distinguibles unos de otros?

## M2 — Precisión del modelo de datos
Si el documento incluye estructuras de datos, estas deben ser
coherentes con el modelo conceptual y sin ambigüedades.
- ¿Las estructuras reflejan fielmente las 4 causas?
- ¿Los estados epistémicos están representados?
- ¿Las relaciones incluyen intercambio (sustancia, fases, nivel)?

## M3 — Abstracción y extensibilidad
Los componentes están diseñados como abstracciones extensibles,
no como implementaciones rígidas.
- ¿Hay interfaces/contratos claros? (SearchSource, Storage...)
- ¿Son reemplazables/extensibles?
- ¿El documento distingue abstracción de implementación?

## M4 — Completitud de cobertura material
El documento cubre todos los componentes necesarios para
entender "de qué está hecho" el sistema sin lagunas graves.
- ¿Falta algún componente esencial?
- ¿Hay referencias circulares sin resolver?
- ¿Los ejemplos son suficientes?

Puntuación Material (0-5): ___
Evidencia: ...
Gaps identificados: ...

# ─────────────────────────────────────────────────────────────
# DIMENSIÓN FORMAL
# ─────────────────────────────────────────────────────────────
# Evalúa si el documento establece la ESTRUCTURA, las REGLAS,
# la ORGANIZACIÓN del sistema. No solo qué hay, sino cómo se
# ordena y qué principios lo rigen.
# ─────────────────────────────────────────────────────────────

## F1 — Principios y reglas estructurales
El documento explicita las reglas que gobiernan el sistema.
- ¿Define reglas claras (R1, R2...)?
- ¿Las reglas son consistentes entre sí?
- ¿Cubren todos los casos de uso previstos?

## F2 — Arquitectura y relaciones entre componentes
El documento muestra cómo se conectan e interactúan los
componentes en una estructura coherente.
- ¿Hay diagrama o descripción arquitectónica?
- ¿Los flujos entre componentes están claros?
- ¿La arquitectura es escalable?

## F3 — Coherencia interna (auto-apicación del modelo)
El documento debe aplicar su propio modelo. Si describe un
sistema causal-sistémico, el documento mismo debería reflejar
esa organización.
- ¿El documento está estructurado por las 4 causas + vista sistémica?
- ¿El meta-modelo se aplica consistentemente?
- ¿Hay contradicciones entre la forma del documento y su contenido?

## F4 — Mapeo TGS ↔ Causas
Si el documento menciona Teoría General de Sistemas, el mapeo
debe ser preciso y justificado.
- ¿Cada causa se asocia correctamente con su concepto TGS?
- ¿La emergencia se explica como interacción de causas?
- ¿Hay isomorfismos identificados?

Puntuación Formal (0-5): ___
Evidencia: ...
Gaps identificados: ...

# ─────────────────────────────────────────────────────────────
# DIMENSIÓN EFICIENTE
# ─────────────────────────────────────────────────────────────
# Evalúa si el documento describe los PROCESOS, FLUJOS,
# PIPELINES y MECANISMOS que generan y mantienen el sistema.
# No importa solo qué es el sistema, sino cómo opera.
# ─────────────────────────────────────────────────────────────

## E1 — Pipeline o proceso de generación
El documento describe cómo se produce el valor del sistema
(pipeline, flujo de trabajo, cadena de procesamiento).
- ¿Está claro el flujo: entrada → proceso → salida?
- ¿Las etapas son distinguibles y justificadas?
- ¿Se muestra qué produce cada etapa?

## E2 — Mecanismo de aprendizaje y adaptación
Si el sistema aprende (por curación, feedback), el documento
describe el mecanismo concreto.
- ¿Cómo recibe feedback el sistema?
- ¿Cómo transforma feedback en mejora?
- ¿Hay protección contra sobre-aprendizaje o malaprendizaje?

## E3 — Roles de proceso (agentes, actores)
El documento identifica quién/procesa, con qué responsabilidad
y en qué orden.
- ¿Los agentes/roles están claramente definidos?
- ¿Cada uno tiene un prompt/misión específica?
- ¿Hay un orquestador/sintetizador?

## E4 — Visibilidad del proceso
Si el documento es un brief de UX/UI, debe considerar cómo el
usuario percibe y entiende el proceso del sistema.
- ¿El usuario ve el progreso del procesamiento?
- ¿Hay transparencia sobre las fuentes y su confianza?
- ¿El usuario entiende por qué el sistema sugiere lo que sugiere?

Puntuación Eficiente (0-5): ___
Evidencia: ...
Gaps identificados: ...

# ─────────────────────────────────────────────────────────────
# DIMENSIÓN FINAL
# ─────────────────────────────────────────────────────────────
# Evalúa si el documento explicita el PROPÓSITO, TELOS,
# y CRITERIOS DE ÉXITO del sistema. Para qué existe, a quién
# sirve, cómo se mide si funciona.
# ─────────────────────────────────────────────────────────────

## T1 — Propósito y visión
El documento tiene una declaración clara y precisa del propósito.
- ¿Hay una frase que captura el "para qué" del sistema?
- ¿El propósito es distintivo (no es "otra Wikipedia")?
- ¿Es ambicioso pero realista?

## T2 — Usuarios y sus fines
El documento identifica los tipos de usuario y lo que cada uno
busca lograr con el sistema.
- ¿Hay perfiles de usuario?
- ¿Cada perfil tiene una finalidad específica?
- ¿Los fines de los usuarios son consistentes con el propósito del sistema?

## T3 — Criterios de éxito medibles
El documento define cómo se sabe si el sistema funciona.
- ¿Hay métricas o criterios concretos?
- ¿Cubren usabilidad, calidad epistémica, rendimiento?
- ¿Son verificables?

## T4 — Visión evolutiva (MVP → maduro)
El documento distingue entre lo mínimo viable y la visión a largo plazo.
- ¿Hay fases o etapas definidas?
- ¿Cada fase tiene capacidades concretas?
- ¿La visión futura es coherente con la arquitectura actual?

Puntuación Final (0-5): ___
Evidencia: ...
Gaps identificados: ...

# ─────────────────────────────────────────────────────────────
# DIMENSIÓN SISTÉMICA (Vista como totalidad)
# ─────────────────────────────────────────────────────────────
# Evalúa si el documento trata el sistema como un TODO
# integrado, no como una suma de partes. Emergencia,
# límites, relaciones entre causas, isomorfismos.
# ─────────────────────────────────────────────────────────────

## S1 — Emergencia y propiedades del todo
El documento identifica qué propiedades emergen de la interacción
de los componentes, que no existen en las partes por separado.
- ¿Menciona propiedades emergentes del sistema?
- ¿Explica cómo surgen de la interacción de las causas?
- ¿Diferencia entre propiedad de componente vs emergente?

## S2 — Límites y entorno
El documento define los límites del sistema (lo que está dentro
vs fuera) y su relación con el entorno.
- ¿Hay una declaración explícita de lo que el sistema NO es?
- ¿Identifica el entorno (fuentes externas, otros sistemas)?
- ¿Los límites son coherentes con el propósito?

## S3 — Recursividad y cambio de nivel
El documento captura la capacidad del sistema de cambiar de
nivel de análisis (arista↔nodo, sistema↔subsistema, zoom↔reframe).
- ¿La recursividad ontológica está presente?
- ¿Hay ejemplos concretos de cambio de nivel?
- ¿La interfaz/navegación permite estos cambios?

## S4 — Coherencia sistémica global
El documento es internamente coherente: no hay contradicciones
entre dimensiones, y las partes forman un todo integrado.
- ¿Hay contradicciones entre secciones?
- ¿Los ejemplos son consistentes con el modelo?
- ¿Se siente como un documento unificado o como partes pegadas?

Puntuación Sistémica (0-5): ___
Evidencia: ...
Gaps identificados: ...

# ─────────────────────────────────────────────────────────────
# PROCESO DE EVALUACIÓN
# ─────────────────────────────────────────────────────────────
# 1. Leer el documento completo.
# 2. Evaluar cada criterio individualmente (0-5).
# 3. Calcular promedio por dimensión.
# 4. Identificar gaps específicos (qué falta o está débil).
# 5. Reportar: puntuaciones + gaps + recomendaciones.
#
# Nivel "ALTO" = todas las dimensiones ≥ 4.0
# Si alguna dimensión está < 4.0, el documento necesita iteración.
# ─────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════
# REGISTRO DE EVALUACIONES
# ═══════════════════════════════════════════════════════════════

# Evaluación 1: SPEC.md
# Fecha: TBD
# Puntuaciones:
#   Material:   ___
#   Formal:     ___
#   Eficiente:  ___
#   Final:      ___
#   Sistémica:  ___
#   Promedio:   ___
#   Nivel alto: Sí / No
# Gaps principales:
#   - ...
# Acción: ...

# Evaluación 2: UX-UI-BRIEF.md
# Fecha: TBD
# Puntuaciones:
#   Material:   ___
#   Formal:     ___
#   Eficiente:  ___
#   Final:      ___
#   Sistémica:  ___
#   Promedio:   ___
#   Nivel alto: Sí / No
# Gaps principales:
#   - ...
# Acción: ...

# ═══════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════
# EVALUACIÓN 1: SPEC.md
# ═══════════════════════════════════════════════════════════════

## Puntuaciones

| Dimensión | M1 | M2 | M3 | M4 | Promedio |
|-----------|----|----|----|----|----------|
| **Material** | 5 | 5 | 5 | 4 | **4.75** |
| **Formal** | 5 | 5 | 5 | 5 | **5.00** |
| **Eficiente** | 5 | 5 | 5 | 3 | **4.50** |
| **Final** | 5 | 5 | 5 | 5 | **5.00** |
| **Sistémica** | 5 | 5 | 4 | 4 | **4.50** |

**Promedio general: 4.75**
**Nivel alto: ✅ SÍ** (todas las dimensiones ≥ 4.0)

## Gaps identificados

1. **M4 — Completitud material**: La recursividad arista→nodo está declarada (R4, ExchangePhase.subRelations) pero no modelada como entidad explícita "RelationAsConcept". Se infiere pero no se formaliza.
2. **E4 — Visibilidad del proceso**: Como especificación técnica, no aborda cómo el usuario percibe el proceso. No es su propósito, pero podría sugerir indicadores.
3. **S3 — Recursividad**: Declarada en reglas pero no ejemplificada transversalmente dentro del documento.
4. **S4 — Coherencia global**: Faltan ejemplos que conecten todas las causas en un caso unificado.

## Recomendación

SPEC.md está en nivel alto. No requiere iteración. Puede usarse como base firme para el brief.


# ═══════════════════════════════════════════════════════════════
# EVALUACIÓN 2: UX-UI-BRIEF.md
# ═══════════════════════════════════════════════════════════════

## Puntuaciones

| Dimensión | C1 | C2 | C3 | C4 | Promedio |
|-----------|----|----|----|----|----------|
| **Material** | 3 | 2 | 3 | 2 | **2.50** |
| **Formal** | 2 | 1 | 1 | 1 | **1.25** |
| **Eficiente** | 2 | 2 | 3 | 2 | **2.25** |
| **Final** | 4 | 5 | 4 | 2 | **3.75** |
| **Sistémica** | 3 | 2 | 3 | 3 | **2.75** |

**Promedio general: 2.50**
**Nivel alto: ❌ NO** (ninguna dimensión alcanza 4.0)

## Gaps identificados vs SPEC.md

### Críticos (score < 2.0)

| Gap | Dimensión | SPEC.md dice | Brief no refleja |
|-----|-----------|-------------|-----------------|
| Estructura causal del brief | Formal (1) | El documento DEBE estar estructurado por 4 causas + vista sistémica | Usa secciones UX tradicionales (propósito, usuarios, user stories...) |
| Reglas R1-R6 como principios de diseño | Formal (2) | 6 reglas estructurales que gobiernan el sistema | No aparecen como guías de diseño |
| Arquitectura visual / flujo de interfaz | Formal (1) | Diagrama Frontend↔Orquestador↔Search↔Storage | No hay mapa de cómo el usuario navega entre componentes |
| Mapeo TGS↔Causas en hipótesis visuales | Formal (1) | Tabla de mapeo precisa | Hipótesis no evalúan si representan las 4 causas |

### Importantes (score 2.0-2.9)

| Gap | Dimensión | SPEC.md dice | Brief no refleja |
|-----|-----------|-------------|-----------------|
| Entidades del modelo como elementos UX | Material (2) | Concept, Relation, ExchangePhase, EpistemicState | El brief no referencia estas entidades como objetos de interacción |
| Completitud de interacciones | Material (2) | Pipeline, agentes, aprendizaje, intercambios | Faltan user stories para: ver progreso del pipeline, clic en arista→nodo, ver niveles de intercambio en grafo |
| Pipeline visible | Eficiente (2) | 7 etapas con agentes trabajando en paralelo | Es caja negra ("el sistema procesa") |
| Aprendizaje visible | Eficiente (2) | Patrones, ponderación, auto-corrección | "El sistema aprende" sin interacción de feedback visual |
| Visibilidad del proceso | Eficiente (2) | Estados epistémicos, confianza | No hay indicadores de confianza, fuente, progreso en la UX |
| Límites del sistema | Sistémica (2) | "Lo que NO es" explícito | No hay declaración de límites desde la perspectiva del usuario |
| Recursividad arista→nodo como interacción | Sistémica (3) | R4, ejemplos conceptuales | Brief tiene ejemplos pero no user story dedicada |

### Menores (score 3.0-3.9)

| Gap | Dimensión | Brief tiene | Pero le falta |
|-----|-----------|-------------|--------------|
| Propósito | Final (4) | Bien definido | Podría ser más preciso ("capa de análisis" vs "enciclopedia") |
| Criterios de éxito | Final (4) | 8 criterios concretos | Faltan: criterios epistémicos, de aprendizaje, de rendimiento |
| Visión evolutiva | Final (2) | Tabla multimodal diferencia MVP/post-MVP | User stories no marcan qué es MVP vs futuro. Modos opcionales no tienen criterio de priorización |
| Emergencia | Sistémica (3) | Navegación no lineal implícita | No se nombra como propiedad emergente del sistema |

# ═══════════════════════════════════════════════════════════════
# EVALUACIÓN 3: UX-UI-BRIEF.md (iterado) — RE-EVALUACIÓN
# ═══════════════════════════════════════════════════════════════

## Puntuaciones

| Dimensión | C1 | C2 | C3 | C4 | Promedio | Δ vs anterior |
|-----------|----|----|----|----|----------|--------------|
| **Material** | 5 | 5 | 5 | 5 | **5.00** | +2.50 ▲ |
| **Formal** | 5 | 5 | 5 | 4 | **4.75** | +3.50 ▲ |
| **Eficiente** | 5 | 5 | 5 | 5 | **5.00** | +2.75 ▲ |
| **Final** | 5 | 5 | 5 | 5 | **5.00** | +1.25 ▲ |
| **Sistémica** | 5 | 5 | 5 | 5 | **5.00** | +2.25 ▲ |

**Promedio general: 4.95**
**Nivel alto: ✅ SÍ** (todas las dimensiones ≥ 4.0)
**Mejora: +2.45 puntos vs evaluación anterior (2.50 → 4.95)**

## Gaps cerrados

| Gap crítico (eval anterior) | Estado ahora | Evidencia |
|----------------------------|-------------|-----------|
| Brief no estructurado por causas | ✅ Cerrado | Estructura = 4 causas + vista sistémica |
| Reglas R1-R6 ausentes | ✅ Cerrado | Sección 2.1: tabla regla→principio→significado |
| Sin arquitectura visual | ✅ Cerrado | Sección 2.2: diagrama completo de navegación |
| Sin mapeo TGS↔Causas | ✅ Cerrado | Principios R1-R6 integran el mapeo; hipótesis evaluadas contra C1-C4 |
| Entidades del modelo no integradas | ✅ Cerrado | Sección 1.1: mapeo entidad→objeto UX |
| Pipeline como caja negra | ✅ Cerrado | Sección 3.2: pipeline visible con indicador de progreso |
| Aprendizaje invisible | ✅ Cerrado | US-08: panel de patrones + reversión |
| Recursividad sin interacción | ✅ Cerrado | US-06: user story dedicada |
| Sin criterios epistémicos | ✅ Cerrado | Criterios 7-9 en sección 4.3 |
| Hipótesis no evaluadas contra modelo | ✅ Cerrado | Evaluación sistemática C1-C4, recomendación final |
| Límites ausentes | ✅ Cerrado | Sección 5.2: 5 límites explícitos |
| Visión evolutiva difusa | ✅ Cerrado | Tabla de fases con capacidades y criterios de activación |

## Gap menor remanente

- **F4 (4/5)**: El brief no incluye tabla explícita del puente TGS↔Causas (está en SPEC.md). El brief lo aplica implícitamente. Se podría agregar como referencia.

## Veredicto final

El UX-UI-BRIEF.md iterado alcanza **nivel alto** (4.95/5.0). Está listo para ser entregado a un agente especializado en diseño UX/UI.
