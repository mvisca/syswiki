# ═══════════════════════════════════════════════════════════
# ENCICLOPEDIA SISTÉMICA — ESPECIFICACIÓN DEL SISTEMA
# ═══════════════════════════════════════════════════════════
#
# Este documento es él mismo un sistema analizado por sus 4 causas.
# Su estructura refleja el modelo que describe.
#
# SISTEMA: "Enciclopedia Sistémica"
# ═══════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────
# CAUSA MATERIAL — ¿De qué está hecho?
# ─────────────────────────────────────────────────────────────
# Los componentes tangibles del sistema: interfaces, datos,
# artefactos de software que lo constituyen.
# ─────────────────────────────────────────────────────────────

## 1. Entidades del modelo de datos

### Concepto (Nodo)
Unidad fundamental. Cualquier concepto (cosa, persona, proceso, idea, relación).

```
Concept {
  qid: string                    // Wikidata QID — ID canónico
  title: string                  // Título principal
  aliases: string[]              // Sinónimos, traducciones
  language: string               // Idioma de la fuente
  source: string                 // "wikipedia" | "arxiv" | "pubmed" | ...
  causes: {
    material: CauseAnalysis      // Componentes del sistema
    formal: CauseAnalysis        // Estructura / organización
    efficient: CauseAnalysis     // Proceso generador / mantenedor
    final: CauseAnalysis         // Propósito / telos
  }
  systemView: SystemAnalysis     // Vista como sistema (opcional)
  curationStatus: "pending" | "confirmed" | "rejected" | "edited"
  epistemology: EpistemicState   // Estado del conocimiento
  createdAt: timestamp
  updatedAt: timestamp
}
```

### CauseAnalysis
Cada una de las 4 causas tiene:
```
CauseAnalysis {
  summary: string                // Descripción textual
  epistemicStatus: "known" | "partial" | "frontier" | "indeterminate"
  confidence: number             // 0-1
  evidence: string[]             // Fuentes que lo respaldan (URLs)
  relatedConcepts: string[]      // QIDs relacionados
  agentPrompt: string            // Prompt usado para generarlo
}
```

### SystemAnalysis
Vista del concepto como sistema total:
```
SystemAnalysis {
  components: string[]           // QIDs de subsistemas
  emergentProperties: string[]   // Propiedades que surgen del todo
  boundaries: string             // Qué está dentro vs fuera
  environment: string[]          // QIDs del entorno relevante
  relationships: Relation[]      // Relaciones con otros sistemas
}
```

### Relation (Arista = Intercambio)
```
Relation {
  type: "component_of"
      | "material_cause_of" | "formal_cause_of"
      | "efficient_cause_of" | "final_cause_of"
  sourceQid: string
  targetQid: string
  exchange: {                    // Opcional: naturaleza del intercambio
    substance: "matter" | "energy" | "information" | "mixed"
    phases: ExchangePhase[]      // handshake → intercambio → cierre
    level: "sub" | "same" | "supra"
  }
  curationStatus: "pending" | "confirmed" | "rejected" | "edited"
}
```

### ExchangePhase
Fase de un intercambio (puede verse como relación en sí misma):
```
ExchangePhase {
  name: string                   // "handshake" | "exchange" | "closure"
  order: number
  description: string
  substances: string[]
  subRelations?: Relation[]      // Recursividad: fase → relación → sistema
}
```

### EpistemicState
```
EpistemicState {
  overall: "known" | "partial" | "frontier" | "indeterminate"
  perCause: {
    material: string
    formal: string
    efficient: string
    final: string
  }
  notes: string                  // "La ciencia no ha determinado..."
}
```

## 2. Interfaces de infraestructura

### SearchSource (Fuente de datos — abstracción)
```
interface SearchSource {
  name: string
  weight: number                 // Confiabilidad 0-1
  domains: string[]              // Temas donde es autoritativa
  search(query, language, options?) → Result[]
  getConcept(identifier) → ConceptData
  getArticle(identifier, language) → ArticleData
}
```
Implementaciones planificadas:
- WikipediaSource (EN, DE, ES, ...)
- ArxivSource (científico)
- PubmedSource (médico)
- GenericWebSource (futuro: toda internet)

### SearchEngine (Orquestador de búsqueda)
```
SearchEngine {
  lookup(query, options?)
    mode: "simple" | "all" | "best" | "auto"
    source?: string              // Fuente específica o auto
    language?: string[]
    domain?: string              // Para ponderar fuentes
}
```

### Storage (Persistencia — abstracción Repository)
```
interface Storage {
  getConcept(qid: string) → Concept | null
  saveConcept(concept: Concept) → void
  saveAnalysis(qid: string, analysis: Analysis) → void
  saveRelation(from, to, type) → void
  getRelations(qid: string) → Relation[]
  saveUserCuration(qid, curation) → void
  getLearningPatterns() → Pattern[]
}
```
Implementaciones:
- NoopStorage (MVP — no persiste, solo declara interfaz)
- SQLiteStorage (post-MVP)
- PostgreSQLStorage (futuro escalado)

## 3. Tipos de arista (relaciones)

| Arista | Significado | Desde sistema A hacia sistema B |
|--------|-------------|--------------------------------|
| `es_componente_de` | A es parte de B | A es subsistema de B |
| `es_causa_material_de` | A constituye materialmente a B | A es insumo, materia de B |
| `es_causa_formal_de` | A da estructura/forma a B | A es patrón, diseño de B |
| `es_causa_eficiente_de` | A produce/genera/cambia B | A es proceso, agente de B |
| `es_causa_final_de` | A es el propósito de B | A es el telos, función de B |

## 4. Sustancias del intercambio

Las relaciones entre sistemas involucran intercambio de:
- **Materia** — transferencia física, masa, energía
- **Energía** — trabajo, calor, movimiento
- **Información** — señales, datos, significado, patrones
- **Mixto** — combinación de las anteriores (ej: el habla es materia+energía+información)

El orden del intercambio sigue fases: **handshake** (inicio / sincronización / acuerdo) → **intercambio** (flujo principal) → **cierre** (terminación /ack).


# ─────────────────────────────────────────────────────────────
# CAUSA FORMAL — ¿Cuál es su estructura?
# ─────────────────────────────────────────────────────────────
# La organización, arquitectura, patrones que definen al sistema
# como un todo coherente.
# ─────────────────────────────────────────────────────────────

## 5. Puente Teoría General de Sistemas ↔ Causas Aristotélicas

Cada causa aristotélica es una lente para analizar un sistema.
El sistema mismo aplica este mapeo a cada concepto que procesa.

| Causa | Concepto TGS asociado | Lo que pregunta |
|-------|----------------------|-----------------|
| **Material** | Componentes, flujos de materia/energía, subsistemas | ¿De qué partes está hecho el sistema? |
| **Formal** | Organización, isomorfismos, patrón sobre sustancia, límites | ¿Cuál es su estructura? ¿Qué lo define como tal? |
| **Eficiente** | Procesos dinámicos, feedback, equifinalidad, diferenciación | ¿Qué proceso lo genera, lo mantiene o lo transforma? |
| **Final** | Telos, direccionalidad, estado estacionario, función adaptativa | ¿Cuál es su propósito? ¿Hacia dónde tiende? |
| **(Emergencia)** | El todo > suma de partes — surge de la interacción entre causas | ¿Qué propiedades nuevas aparecen al integrar las causas? |

### Reglas estructurales

**R1 — Las 4 causas son obligatorias como dimensiones, no como contenidos.**
Todo concepto analizado tiene 4 slots causales. Cada slot puede estar en cualquier estado epistémico. "No sabemos" es un estado válido, no una ausencia.

**R2 — Toda relación es un intercambio.**
No existe relación sin sustancia intercambiada. Si dos sistemas se relacionan, algo fluye entre ellos (materia, energía o información).

**R3 — Toda relación tiene nivel jerárquico.**
El intercambio ocurre a nivel sub (entre subsistemas), same (entre pares) o supra (sistema-entorno).

**R4 — Una arista puede ser un nodo en otro nivel.**
La relación en sí misma puede ser vista como sistema con sus 4 causas. Esto permite la recursividad ontológica.

**R5 — Zoom y reframe mantienen contexto.**
El usuario navega cambiando de nivel (zoom in/out) o cambiando de lente (reframe sistema↔causa). En cada paso, el contexto anterior es accesible (breadcrumb).

**R6 — Aprendizaje por curación.**
El sistema sugiere relaciones automáticamente. El usuario cura (confirma/rechaza/edita). El sistema extrae patrones de las curaciones para mejorar sugerencias futuras.

## 6. Arquitectura del sistema

```
┌─────────────────────────────────────────────────────────┐
│                      FRONTEND                           │
│  (Web App — 2D graph MVP, 3D post-MVP)                  │
│  Navegación molecular, foco+contexto, split view         │
└────────────────────┬────────────────────────────────────┘
                     │ API REST / WebSocket
┌────────────────────┴────────────────────────────────────┐
│                    ORQUESTADOR                           │
│  SearchEngine: selecciona fuente según query/dominio     │
│  PipelineAgent: coordina agentes por causa               │
│  Synthesizer: combina perspectivas                       │
│  UserCuration: recibe feedback, extrae patrones          │
└──────┬──────────────────────┬───────────────────────────┘
       │                      │
┌──────┴──────┐      ┌───────┴──────────┐
│  Search     │      │   Storage        │
│  Sources    │      │   (Repository)   │
│  (abstract) │      │   (abstract)     │
│  Wikipedia  │      │   Noop / SQLite  │
│  arXiv      │      │   / PostgreSQL   │
│  ...        │      │                  │
└─────────────┘      └──────────────────┘
```

## 7. Identidad y multi-idioma

- **QID de Wikidata** como identificador canónico universal
- Input: cualquier idioma soportado (EN, DE, ES, IT, FR...)
- Output: configurable por el usuario en cualquier idioma
- Búsqueda inteligente: si no encuentra en idioma A, busca en B y C
- El análisis causal es independiente del idioma de la fuente


# ─────────────────────────────────────────────────────────────
# CAUSA EFICIENTE — ¿Qué proceso lo genera y mantiene?
# ─────────────────────────────────────────────────────────────
# El pipeline, los agentes, el flujo de trabajo que producen
# el análisis y mantienen el sistema vivo.
# ─────────────────────────────────────────────────────────────

## 8. Pipeline de generación multi-agente

Cada concepto nuevo pasa por este proceso:

```
  Usuario busca concepto
         │
         ▼
  ┌─────────────────────┐
  │ 1. SearchEngine     │─── ¿Ya curado? → Storage devuelve
  │    lookup(query)    │
  └─────────┬───────────┘
            │ No encontrado en caché
            ▼
  ┌─────────────────────┐
  │ 2. Explorador       │─── Fetch de Wikipedia / fuentes
  │    (agente)         │     Extrae: resumen, categorías,
  │                     │     infobox, enlaces, imagen
  └─────────┬───────────┘
            │ texto crudo del artículo
            ▼
  ┌─────────────────────┐
  │ 3. Agentes por      │
  │    causa (4 en      │─── Cada agente analiza desde
  │    paralelo)        │     su perspectiva específica
  │                     │
  │  ┌───────────────┐  │     Agente Material:
  │  │ Material      │  │       "¿De qué componentes está
  │  │               │  │        hecho? ¿Qué partes lo
  │  │               │  │        constituyen?"
  │  └───────────────┘  │
  │  ┌───────────────┐  │     Agente Formal:
  │  │ Formal        │  │       "¿Cuál es su estructura?
  │  │               │  │        ¿Qué patrón lo define?"
  │  └───────────────┘  │
  │  ┌───────────────┐  │     Agente Eficiente:
  │  │ Eficiente     │  │       "¿Qué proceso lo genera
  │  │               │  │        o mantiene?"
  │  └───────────────┘  │
  │  ┌───────────────┐  │     Agente Final:
  │  │ Final         │  │       "¿Cuál es su propósito?
  │  │               │  │        ¿Para qué existe?"
  │  └───────────────┘  │
  │  ┌───────────────┐  │     Agente Sistémico:
  │  │ Sistémico     │  │       "¿Cómo se relacionan
  │  │               │  │        las causas entre sí?
  │  │               │  │        ¿Qué emerge del todo?"
  │  └───────────────┘  │
  └─────────┬───────────┘
            │ 5 análisis parciales
            ▼
  ┌─────────────────────┐
  │ 4. Sintetizador     │─── Integra perspectivas en una
  │    (agente)         │     ficha coherente y unificada
  └─────────┬───────────┘
            │ Ficha completa del concepto
            ▼
  ┌─────────────────────┐
  │ 5. Presentación     │─── Se muestra al usuario en la
  │    al usuario       │     interfaz con estados epistémicos
  └─────────┬───────────┘
            │
            ▼
  ┌─────────────────────┐
  │ 6. Curación         │─── Usuario revisa, corrige, completa
  │    (usuario)        │     Confirmar | Rechazar | Editar
  └─────────┬───────────┘
            │
            ▼
  ┌─────────────────────┐
  │ 7. Aprendizaje      │─── El sistema extrae patrones:
  │    (sistema)        │     - "Cuando Wikipedia dice
  │                     │       'inventado por' → sugerir
  │                     │       causa eficiente"
  │                     │     - Ponderación por frecuencia
  │                     │       de confirmación
  └─────────────────────┘
```

### Roles de los agentes en detalle

| Agente | Input | Output | Prompt guía |
|--------|-------|--------|------------|
| **Explorador** | Query de usuario | Artículo(s) de fuente(s) | "Busca el concepto en las fuentes disponibles. Extrae: resumen, categorías taxonómicas, infobox, enlaces salientes principales." |
| **Material** | Artículo completo | CauseAnalysis | "Identifica los componentes, partes, ingredientes, materiales que constituyen este concepto como sistema." |
| **Formal** | Artículo completo | CauseAnalysis | "Identifica la estructura, organización, patrón, forma, arquitectura que define a este concepto." |
| **Eficiente** | Artículo completo | CauseAnalysis | "Identifica el proceso, mecanismo, agente, fuerza, causa productora que genera o mantiene este concepto." |
| **Final** | Artículo completo | CauseAnalysis | "Identifica el propósito, función, telos, finalidad, objetivo de este concepto como sistema." |
| **Sistémico** | Artículo completo + 4 análisis | SystemAnalysis | "Sintetiza cómo las 4 causas se relacionan. Identifica propiedades emergentes, límites, relaciones con el entorno." |
| **Sintetizador** | 5 análisis | Ficha unificada | "Combina los análisis en una ficha coherente. Resuelve contradicciones. Preserva estados epistémicos." |

### Mecanismo de aprendizaje

```
Patrón de curación:
  Usuario confirma: "inventado_por" → causa eficiente  (+1)
  Usuario confirma: "inventado_por" → causa eficiente  (+1)
  Usuario rechaza:  "inventado_por" → causa material   (-1)
  
  Resultado: sistema aprende que "inventado_por"
  tiene alta correlación con causa eficiente.
  → Lo sugiere automáticamente en adelante.
```

El sistema es **juez de sí mismo**: cuando detecta baja confianza en una sugerencia (patrón no consolidado), lo marca explícitamente. No sobre-aprende de un solo usuario — requiere múltiples confirmaciones para consolidar un patrón.


# ─────────────────────────────────────────────────────────────
# CAUSA FINAL — ¿Cuál es su propósito?
# ─────────────────────────────────────────────────────────────
# El telos del sistema: para qué existe, qué necesidad
# satisface, hacia dónde evoluciona.
# ─────────────────────────────────────────────────────────────

## 9. Propósito fundamental

> **"Permitir a cualquier persona explorar cualquier concepto como un sistema analizado por sus 4 causas aristotélicas, revelando relaciones que una enciclopedia lineal no muestra."**

El sistema no es un sustituto de Wikipedia. Es una **capa de análisis sistémico-causal** sobre cualquier fuente de conocimiento.

## 10. Usuarios y sus fines

| Usuario | Su finalidad al usar el sistema | Lo que el sistema le ofrece |
|---------|--------------------------------|---------------------------|
| **Explorador** | Saciar curiosidad intelectual, descubrir relaciones | Búsqueda, navegación del grafo, zoom/reframe |
| **Curador** | Aportar conocimiento, mejorar calidad del sistema | Interfaz de curación, confirmación/rechazo/edición |
| **Investigador** | Descubrir patrones causales entre dominios | Vista sistémica, cadenas causales, exportación |
| **Aprendiz** | Estudiar un tema desde múltiples perspectivas | Foco+contexto, zoom semántico, estados epistémicos |
| **Sistema mismo** | Mejorar sus predicciones y sugerencias | Patrones de curación, aprendizaje automático |

## 11. Criterios de éxito del sistema

- Un usuario nuevo comprende la navegación en < 2 minutos
- Reframear un concepto requiere 1 acción
- Zoom in/out requiere 1 acción
- El estado epistémico de cada causa es visible sin acciones extra
- No hay "callejones sin salida" — cada nodo tiene al menos una relación saliente
- El sistema puede auto-corregirse: si un patrón aprendido resulta incorrecto, el curador lo revierte y el sistema lo desaprende
- El costo marginal de analizar un nuevo concepto tiende a cero (por caché y aprendizaje)

## 12. Visión evolutiva (MVP → maduro)

| Fase | Capacidad |
|------|-----------|
| **MVP** | Búsqueda en Wikipedia, pipeline multi-agente básico, vista 2D, curación manual, NoopStorage |
| **V2** | SQLite, multi-idioma real, búsqueda en múltiples fuentes, cadenas causales |
| **V3** | Vista 3D, voz, aprendizaje por patrones consolidados |
| **V4** | Fuentes externas (arXiv, PubMed), video/imagen generada, comunidad de curadores |
| **Futuro** | Internet como fuente, modelo 3D como interfaz de navegación, realidad aumentada |


# ─────────────────────────────────────────────────────────────
# VISTA SISTÉMICA — El sistema como totalidad
# ─────────────────────────────────────────────────────────────
# Relaciones entre causas, propiedades emergentes, límites
# con el entorno, isomorfismos con otros sistemas.
# ─────────────────────────────────────────────────────────────

## 13. Relaciones entre las causas del sistema

El sistema no es la suma de sus partes — las causas interactúan:

``` 
  [CAUSA MATERIAL]         [CAUSA FORMAL]
  Datos, interfaces        Arquitectura, modelo
       │                          │
       │  La estructura           │  La arquitectura
       │  organiza los            │  define qué datos
       │  datos                  │  son necesarios
       └──────────┬──────────────┘
                  │
                  ▼
       [EMERGENCIA: navegación sistémica]
       El usuario puede moverse entre conceptos
       y niveles como no puede en una enciclopedia
       tradicional.
                  │
                  │
       ┌──────────┴──────────────┐
       │                          │
  [CAUSA EFICIENTE]          [CAUSA FINAL]
  Pipeline multi-agente      Exploración de conocimiento
  Curación y aprendizaje     como sistema vivo
```

### Propiedades emergentes del sistema
- **Navegación no lineal** — imposible en Wikipedia tradicional
- **Conexiones causales explícitas** — emerge al cruzar 4 perspectivas de análisis
- **Mapa epistémico** — emerge al registrar estados del conocimiento por causa
- **Auto-mejora** — el sistema refina sus sugerencias con cada curación
- **Recursividad ontológica** — lo que es relación en un nivel es sistema en otro

### Límites del sistema (lo que NO es)
- No es un motor de búsqueda general (usa Wikipedia como fuente principal)
- No es una herramienta de authoring (no edita Wikipedia, solo consume)
- No es un verificador de hechos (hereda la confiabilidad de sus fuentes)
- No es una red social (la curación no es colaborativa en MVP)

### Isomorfismos con otros sistemas

| Este sistema | Es isomorfo a | Porque |
|-------------|---------------|--------|
| Nodo con 4 causas + vista sistémica | Átomo con 4 orbitales + núcleo | Cada orbital es una lente sobre el núcleo |
| Relación como intercambio | Protocolo de comunicación | Handshake → datos → cierre |
| Navegación zoom/reframe | Exploración de grafo conceptual | Todo sistema se abre en subsistemas |
| Pipeline multi-agente | Sistema de producción industrial | Materia prima → proceso → producto → control de calidad |

### El sistema se aplica a sí mismo

Este documento es prueba de ello: la Enciclopedia Sistémica es un sistema,
y este documento la describe usando sus propias 4 causas + vista sistémica.

```
Material:  datos, interfaces, entidades, infraestructura
Formal:    arquitectura, puente TGS-Causas, reglas estructurales
Eficiente: pipeline multi-agente, curación, aprendizaje
Final:     exploración del conocimiento como sistema vivo

Sistema:   la totalidad que emerge de la interacción de estas causas
           → una enciclopedia que no solo informa, sino que revela
             la estructura causal y sistémica del conocimiento.
```
