# ═══════════════════════════════════════════════════════════════
# ENCICLOPEDIA SISTÉMICA — BRIEF DE DISEÑO DE EXPERIENCIA
# ═══════════════════════════════════════════════════════════════
#
# Este brief describe qué debe experimentar el usuario y cómo
# debe comportarse el sistema. Está estructurado por las 4 causas
# sistémicas + vista de totalidad, igual que el sistema que describe.
# Sirve como input no-condicionado para un agente de diseño UX/UI.
#
# SISTEMA REFERENCIA: "Enciclopedia Sistémica" (ver SPEC.md)
# ═══════════════════════════════════════════════════════════════


# ─────────────────────────────────────────────────────────────
# CAUSA MATERIAL — ¿Qué componentes experienciales tiene?
# ─────────────────────────────────────────────────────────────
# Los elementos tangibles de la interfaz con los que el usuario
# interactúa: superficies, objetos, modos de salida, artefactos
# multimodales. No son botones ni layouts — son los "materiales"
# de la experiencia.
# ─────────────────────────────────────────────────────────────

## 1.1 Objetos de interacción fundamentales

El usuario interactúa con los mismos objetos que el modelo de datos
(ver SPEC.md sección 1), pero presentados como entidades experienciales:

| Objeto UX | Entidad SPEC | Qué hace el usuario con él |
|-----------|--------------|---------------------------|
| **Concepto** | Concept | Lo busca, lo selecciona, lo abre, lo navega |
| **Causa** | CauseAnalysis | La lee, expande, edita, cambia su estado epistémico |
| **Vista sistémica** | SystemAnalysis | Ve componentes, emergencia, relaciones con otros |
| **Relación** | Relation | La sigue, examina su intercambio, la convierte en nodo |
| **Intercambio** | Exchange | Ve fases (handshake→flujo→cierre), las expande |
| **Estado epistémico** | EpistemicState | Ve si es conocido/parcial/frontera/indeterminado |
| **Grafo** | (vista agregada) | Navega, hace zoom, filtra por causa o nivel |

## 1.2 Modos de salida

### Requeridos (MVP)
- **Texto estructurado**: Ficha del concepto con causas, estados epistémicos, relaciones
- **Grafo 2D navegable**: Mapa conceptual con nodos (conceptos) y aristas (relaciones). Navegación por clic, arrastre, zoom
- **Indicadores de proceso**: Visualización del estado del análisis multi-agente

### Opcionales (post-MVP, priorizados)
| Prioridad | Modo | Dependencia técnica |
|-----------|------|-------------------|
| 1 | **Modelo 3D interactivo** | Motor 3D (Three.js, WebGL) |
| 2 | **Voz** (narración + comandos) | API de voz (Web Speech) |
| 3 | **Artefactos interactivos** | Simulaciones embedidas |
| 4 | **Video/imagen generada** | Pipeline de generación visual |
| 5 | **Audio ambiental** | Sonificación de estados |

## 1.3 Indicadores de estado siempre visibles

Cada concepto en la interfaz debe mostrar, sin interacción extra:

- **Estado epistémico de cada causa**: ✅ ❓ ❌ ⬜ (color/icono por causa)
- **Nivel de confianza del análisis**: barra o indicador numérico (0-1)
- **Fuente del análisis**: Wikipedia EN, arXiv, múltiple...
- **Estado de curación**: pendiente/confirmado/rechazado/editado
- **Nivel jerárquico actual**: sub/same/supra (visible en el contexto de navegación)

## 1.4 Gaps cerrados vs evaluación anterior

| Gap (evaluación previa) | Solución en este brief |
|-------------------------|----------------------|
| Entidades del modelo no integradas en UX | Sección 1.1 mapea cada entidad SPEC a objeto UX |
| Completitud de interacciones | Las 10 user stories cubren todos los casos (ver causa eficiente) |
| Indicadores epistémicos ausentes | Sección 1.3: estados siempre visibles |


# ─────────────────────────────────────────────────────────────
# CAUSA FORMAL — ¿Qué estructura tiene la experiencia?
# ─────────────────────────────────────────────────────────────
# La organización de la interfaz, los principios de diseño que
# rigen la navegación, los patrones estructurales que el usuario
# internaliza para moverse por el sistema.
# ─────────────────────────────────────────────────────────────

## 2.1 Principios de diseño (derivados de reglas estructurales R1-R6)

| Regla SPEC | Principio de diseño UX | Significado para la interfaz |
|-----------|----------------------|---------------------------|
| **R1** — 4 causas como dimensiones obligatorias | **Visibilidad permanente de las 4 causas** | Las 4 causas están SIEMPRE presentes como ejes o lentes. Nunca se ocultan. Una causa en estado "indeterminado" se muestra vacía pero presente. |
| **R2** — Toda relación es intercambio | **Intercambio visible** | Cada arista en el grafo muestra explícitamente la sustancia (materia/energía/información) al ser seleccionada. |
| **R3** — Toda relación tiene nivel jerárquico | **Navegación por nivel** | El usuario puede ver y cambiar entre nivel sub/same/supra. El nivel actual es visible como contexto. |
| **R4** — Arista puede ser nodo | **Relaciones clickeables como sistemas** | Toda arista se puede abrir como si fuera un nodo, revelando sus 4 causas como sistema. |
| **R5** — Zoom/reframe mantienen contexto | **Rastro de navegación + transiciones suaves** | El usuario nunca pierde el contexto al cambiar de nivel o lente. Breadcrumb + animaciones de transición. |
| **R6** — Aprendizaje por curación | **Feedback visible del aprendizaje** | El usuario ve qué aprendió el sistema de sus curaciones. Puede corregir patrones erróneos. |

## 2.2 Arquitectura de navegación

```
                            ┌──────────────────────┐
                            │    BUSCADOR GLOBAL   │
                            │  (barra permanente)  │
                            └──────────┬───────────┘
                                       │ buscar concepto
                                       ▼
 ┌────────────────────────────────────────────────────────────┐
 │                     VISTA PRINCIPAL                        │
 │  ┌──────────────────────┐  ┌────────────────────────────┐ │
 │  │   GRAFO NAVEGABLE    │  │   FICHA DEL CONCEPTO      │ │
 │  │   (mapa conceptual)  │  │   (split view)             │ │
 │  │                      │  │                            │ │
 │  │  Nodos clickeables   │  │  Causa Material:    ✅    │ │
 │  │  Aristas activas     │  │  Causa Formal:      ❓    │ │
 │  │  Zoom in/out         │  │  Causa Eficiente:   ✅    │ │
 │  │  Filtro por causa    │  │  Causa Final:       ❌    │ │
 │  │  Reframe             │  │                            │ │
 │  └──────────────────────┘  │  [Expandir] [Editar]      │ │
 │                            │  [Ver como sistema]        │ │
 │                            └────────────────────────────┘ │
 └────────────────────────────────────────────────────────────┘
          │                        │
          │                        ▼
          │           ┌────────────────────────┐
          │           │ VISTA DE RELACIÓN      │
          │           │ (al hacer clic en      │
          │           │  una arista)           │
          │           │                        │
          │           │ Intercambio: energía   │
          │           │ Nivel: sub             │
          │           │ Fases:                 │
          │           │  ▶ Handshake           │
          │           │  ▶ Intercambio         │
          │           │  ▶ Cierre              │
          │           │ [Ver como sistema]     │
          │           └────────────────────────┘
          │
          ▼
 ┌────────────────────┐
 │ VISTA DE CURACIÓN  │
 │ (modo curador)     │
 │                    │
 │ Editar texto       │
 │ Cambiar estado     │
 │ epistémico         │
 │ Ver patrón         │
 │ aprendido          │
 └────────────────────┘
```

## 2.3 Reglas de navegación

1. **Un clic en un nodo** → ese concepto se convierte en el foco (se actualiza la ficha)
2. **Un clic en una arista** → se abre la vista de relación (intercambio, fases, nivel)
3. **Doble clic en una arista** → reframe: la relación se abre como sistema con sus 4 causas
4. **Zoom in** (scroll/gesto) → el sistema se abre en subsistemas
5. **Zoom out** (scroll/gesto) → se muestra el supersistema contenedor
6. **Reframe** (botón/lente) → cambiar entre "ver como sistema" y "ver como causa de otro"
7. **Breadcrumb** siempre visible → ruta: Carpintería > Martillo > Mango > Madera
8. **El grafo nunca está vacío** → siempre hay al menos una relación de salida

## 2.4 Gaps cerrados vs evaluación anterior

| Gap previo | Solución |
|-----------|----------|
| Brief no estructurado por causas | Ahora el brief ES una estructura causal |
| Reglas R1-R6 ausentes | Sección 2.1: tabla regla→principio→significado |
| Sin arquitectura visual | Sección 2.2: diagrama completo de navegación |
| Sin mapeo TGS↔Causas en diseño | Principios integran el mapeo |


# ─────────────────────────────────────────────────────────────
# CAUSA EFICIENTE — ¿Qué procesos experimenta el usuario?
# ─────────────────────────────────────────────────────────────
# Los flujos de interacción, el pipeline visible, los mecanismos
# de curación y aprendizaje. No solo qué ve el usuario, sino qué
# hace y qué ve que el sistema hace.
# ─────────────────────────────────────────────────────────────

## 3.1 User Stories (interacciones fundamentales)

### US-01: Búsqueda y descubrimiento
> "Como usuario, quiero buscar un concepto y verlo presentado como sistema con sus causas."

- El usuario escribe un término
- El sistema muestra **indicador de progreso**: "Buscando en Wikipedia EN... → Analizando causas (4/4 agentes) → Sintetizando..."
- El resultado muestra: ficha con 4 causas + vista sistémica + grafo de relaciones
- Si ya estaba curado, se muestra instantáneamente con ícono 🗸

### US-02: Zoom in — profundizar en subsistemas
> "Como usuario, quiero hacer clic en un componente del sistema para verlo con sus causas."

- Ejemplo: "Martillo" → clic en "Mango" → "Mango" es ahora el foco
- Transición animada (el nodo se expande al centro)
- Breadcrumb actualizado: Carpintería > Martillo > Mango

### US-03: Zoom out — ver el supersistema
> "Como usuario, quiero ver de qué sistema más grande soy parte."

- Desde "Mango", zoom out → "Martillo" → "Caja herramientas" → "Carpintería"
- El grafo se aleja mostrando niveles superiores
- El breadcrumb muestra la jerarquía completa

### US-04: Reframe — cambiar lente causal
> "Como usuario, quiero cambiar la perspectiva de 'sistema' a 'causa de otro sistema'."

- Un botón/lente permite elegir: "Ver como sistema" | "Ver como causa de..."
- Al seleccionar "causa de...", se muestran las relaciones salientes del concepto
- La ficha cambia de "4 causas del concepto" a "4 relaciones del concepto como causa"

### US-05: Examinar una relación
> "Como usuario, quiero hacer clic en cualquier línea del grafo para ver qué intercambio ocurre."

- Al hacer clic en una arista, se abre panel de relación
- Muestra: sustancia intercambiada (⚡materia | 🔥energía | 💡información)
- Muestra fases: handshake → intercambio → cierre
- **Cada fase es expandible** (clic → sub-relación)

### US-06: Convertir relación en sistema (recursividad)
> "Como usuario, quiero ver cualquier relación como si fuera un sistema con sus 4 causas."

- Opción "Ver como sistema" en el panel de relación
- La relación se abre como un nodo más: "Intercambio Martillo↔Madera" como sistema
- Causa material: martillo + madera; formal: técnica; eficiente: movimiento; final: unir

### US-07: Curación de análisis
> "Como usuario curador, quiero corregir el análisis del sistema."

- Desde la ficha, editar cualquier causa
- Cambiar texto, cambiar estado epistémico (✅❓❌⬜)
- Confirmar/Rechazar sugerencias del sistema
- **Cada curación muestra feedback**: "Patrón actualizado" + barra de confianza del patrón

### US-08: Ver y corregir patrones aprendidos
> "Como usuario curador, quiero ver qué ha aprendido el sistema de mis curaciones."

- Panel de "Patrones aprendidos": ver correlaciones (ej: "inventado_por" → causa eficiente, 92% confianza)
- **El usuario puede revertir patrones**: "Este patrón está mal"
- El sistema muestra cuántos usuarios confirmaron cada patrón
- Protección: un patrón necesita 3+ confirmaciones para consolidarse

### US-09: Exploración del grafo
> "Como usuario, quiero navegar el mapa de conceptos sin buscar específicamente."

- Vista de grafo completa, no solo el entorno del concepto activo
- Filtros: por tipo de causa, por nivel jerárquico, por estado epistémico, por dominio
- Búsqueda visual: nodos más grandes = más relaciones (centralidad)
- Color de nodo según tipo: concepto, persona, proceso, idea...

### US-10: Cambio de nivel de intercambio
> "Como usuario, quiero ver si un intercambio ocurre entre subsistemas, pares o con el entorno."

- Indicador de nivel en cada arista: SUB | SAME | SUPRA
- Al cambiar de nivel, el grafo se reconfigura: nivel sub muestra componentes, nivel supra muestra contexto

## 3.2 Pipeline visible al usuario

El sistema no procesa en segundo plano invisible. El usuario ve:

```
[🔍 Buscando "Martillo"…]
   ├─ [📡 Wikipedia EN] → Artículo encontrado (2.4 KB)
   ├─ [🤖 Analizando causas…]
   │   ├─ Material: ✅ completo
   │   ├─ Formal:   ✅ completo
   │   ├─ Eficiente:⏳ procesando…
   │   └─ Final:    ⏳ esperando…
   ├─ [🧩 Sistémico: sintetizando…]
   └─ [📄 Ficha generada ✅]
```

Este indicador aparece en la primera búsqueda. En conceptos ya curados, aparece instantáneo (con marca 🗸).

## 3.3 Gaps cerrados vs evaluación anterior

| Gap previo | Solución |
|-----------|----------|
| Pipeline como caja negra | 3.2: pipeline visible con indicadores de progreso |
| Aprendizaje invisible | US-08: panel de patrones con reversión |
| Agentes no mencionados en UX | Pipeline visible muestra agentes por nombre |
| Sin feedback de confianza | Indicadores de confianza en fichas + curación |


# ─────────────────────────────────────────────────────────────
# CAUSA FINAL — ¿Para qué existe esta experiencia?
# ─────────────────────────────────────────────────────────────
# El propósito del sistema desde la perspectiva del usuario,
# los tipos de usuario y lo que cada uno busca lograr,
# los criterios que determinan si la experiencia es exitosa.
# ─────────────────────────────────────────────────────────────

## 4.1 Propósito de la experiencia

> "Permitir a cualquier persona explorar cualquier concepto como un sistema, viendo sus 4 causas aristotélicas y las relaciones de intercambio con otros sistemas, revelando conexiones que una enciclopedia tradicional oculta."

La experiencia no es leer — es **explorar, navegar, descubrir, cuestionar y curar**.

## 4.2 Usuarios y sus finalidades

| Usuario | Lo que busca | Lo que la experiencia debe ofrecerle |
|---------|-------------|--------------------------------------|
| **Explorador curioso** | Entender cómo se relacionan las cosas | Búsqueda simple, grafo navegable, descubrimiento casual |
| **Estudiante / Aprendiz** | Estudiar un tema en profundidad | Foco+contexto, zoom semántico, cadenas causales |
| **Investigador** | Descubrir patrones entre dominios | Filtros, búsqueda por relación, exportación de hallazgos |
| **Curador / Experto** | Aportar conocimiento al sistema | Curación, corrección de patrones, vista de aprendizaje |
| **El sistema mismo** | Mejorar sus sugerencias | Feedback explícito, patrones consolidados |

## 4.3 Criterios de éxito de la experiencia

### Funcionales
1. Un usuario nuevo comprende la navegación básica en < 2 minutos sin tutorial
2. Reframear un concepto (sistema ↔ causa) requiere 1 acción
3. Zoom in/out requiere 1 acción
4. Examinar una relación (clic en arista) requiere 1 acción
5. Convertir una relación en sistema requiere 2 acciones
6. No hay "callejones sin salida" — cada nodo tiene ≥ 1 relación saliente

### Epistémicos
7. El estado epistémico de cada causa es visible sin ninguna acción extra
8. El origen de cada análisis (fuente + confianza) es visible en ≤ 2 clics
9. El usuario puede distinguir visualmente entre "conocido", "parcial", "frontera" e "indeterminado"

### De aprendizaje
10. El usuario ve feedback inmediato al curar: "patrón actualizado"
11. El usuario puede acceder al panel de patrones aprendidos en ≤ 3 clics
12. El sistema muestra cuántas confirmaciones respaldan cada patrón

### De rendimiento (MVP)
13. El grafo renderiza ≥ 500 nodos sin pérdida de frames
14. Una búsqueda nueva (no cacheada) muestra resultado en ≤ 30s
15. Un concepto cacheado se muestra en ≤ 2s

## 4.4 Visión evolutiva (MVP → maduro)

| Fase | Capacidades UX | Criterio de activación |
|------|---------------|----------------------|
| **MVP** | Split view (grafo 2D + ficha), búsqueda, 10 user stories, pipeline visible, curación básica, feedback de aprendizaje | Lanzamiento inicial |
| **V2** | Multi-idioma, búsqueda multi-fuente, cadenas causales, panel de patrones avanzado | MVP validado con usuarios |
| **V3** | Modelo 3D, voz (narración + comandos), exportación de hallazgos | Base de conceptos > 1000 |
| **V4** | Artefactos interactivos, video/imagen generada, sonificación | Motor 3D estable |
| **Futuro** | Realidad aumentada, curación colaborativa, internet como fuente | Comunidad activa de curadores |

## 4.5 Gaps cerrados vs evaluación anterior

| Gap previo | Solución |
|-----------|----------|
| Sin criterios epistémicos | 4.3: criterios 7-9 específicamente epistémicos |
| Sin criterios de aprendizaje | 4.3: criterios 10-12 sobre feedback del aprendizaje |
| Visión evolutiva difusa | 4.4: tabla con fases, capacidades y criterio de activación |


# ─────────────────────────────────────────────────────────────
# VISTA SISTÉMICA — La experiencia como totalidad
# ─────────────────────────────────────────────────────────────
# Cómo se integran las dimensiones anteriores en una experiencia
# coherente. Propiedades emergentes, límites de la experiencia,
# hipótesis de visualización evaluadas contra el modelo completo.
# ─────────────────────────────────────────────────────────────

## 5.1 Propiedades emergentes de la experiencia

La experiencia no es la suma de sus componentes. Estas propiedades emergen:

| Propiedad emergente | Cómo surge | Qué siente el usuario |
|-------------------|-----------|----------------------|
| **Navegación no lineal** | Cruce de zoom in/out + reframe + cambio de nivel | "Puedo moverme en múltiples direcciones, no solo adelante/atrás" |
| **Mapa epistémico** | Estados por causa + fuentes + confianza visibles | "Sé qué se sabe, qué no, y cuán seguro es" |
| **Descubrimiento serendípico** | Grafo navegable + relaciones no obvias | "Encontré algo que no buscaba pero me interesa" |
| **Comprensión multi-perspectiva** | 4 causas simultáneas + vista sistémica | "Entiendo esto desde ángulos que no había considerado" |
| **Sistema que mejora con uso** | Curación + feedback visible + patrones | "Mis correcciones hacen que el sistema sea mejor para todos" |

## 5.2 Límites de la experiencia (lo que NO es)

- **No es una enciclopedia de lectura lineal** — no hay "página siguiente". La navegación es libre
- **No es un motor de búsqueda + Wikipedia** — el valor está en el análisis causal, no en el contenido crudo
- **No requiere conocimiento previo** — pero recompensa a quien profundiza
- **No es una red social** — en MVP no hay perfiles, comentarios ni colaboración entre usuarios
- **No resuelve CAPTCHAs ni logins** — depende de APIs públicas

## 5.3 Hipótesis de visualización evaluadas

Cada hipótesis se evalúa contra 4 criterios derivados del modelo:

| Criterio | Pregunta |
|----------|----------|
| **C1: Causas visibles** | ¿Las 4 causas tienen representación natural en la metáfora? |
| **C2: Estados epistémicos** | ¿La metáfora puede mostrar conocido/parcial/frontera/indeterminado? |
| **C3: Niveles jerárquicos** | ¿Sub/same/supra se representan naturalmente? |
| **C4: Recursividad** | ¿La metáfora permite que una relación se convierta en nodo? |

### H1: Molécula conceptual (recomendada para MVP)
| Criterio | Evaluación |
|----------|-----------|
| C1: Causas | ⭐ 4 orbitales = 4 causas. Excelente mapeo uno a uno. |
| C2: Epistémicos | ⭐ Color/opacidad del orbital. Intuitivo. |
| C3: Niveles | ✅ Moléculas dentro de células, células dentro de organismos. |
| C4: Recursividad | ✅ Un enlace molecular puede ser una molécula más pequeña. |

**Riesgo**: Saturación visual con >100 nodos.
**Mitigación**: Agrupación semántica al alejar (zoom semántico).
**Veredicto**: ✅ RECOMENDADA para MVP. Extensible a 3D.

### H2: Árbol fractal
| Criterio | Evaluación |
|----------|-----------|
| C1: Causas | ❌ Las causas no tienen lugar natural en la metáfora del árbol. |
| C2: Epistémicos | ⚠️ Color de hojas/ramas, pero forzado. |
| C3: Niveles | ⭐ Excelente para jerarquía. |
| C4: Recursividad | ✅ Cada rama es un subárbol. |

**Veredicto**: ❌ NO RECOMENDADA. No representa bien las 4 causas.

### H3: Sistema solar
| Criterio | Evaluación |
|----------|-----------|
| C1: Causas | ⚠️ Causas como planetas funciona pero confunde (el sol sería la causa final). |
| C2: Epistémicos | ⚠️ Brillo/color del planeta. |
| C3: Niveles | ❌ No hay representación natural. |
| C4: Recursividad | ❌ Un planeta no es un sistema solar. |

**Veredicto**: ❌ NO RECOMENDADA. Confunde causa final con centralidad.

### H4: Corte geológico
| Criterio | Evaluación |
|----------|-----------|
| C1: Causas | ❌ No hay lugar para causas laterales. |
| C2: Epistémicos | ⚠️ Color/textura del estrato. |
| C3: Niveles | ⭐ Excelente para profundidad jerárquica. |
| C4: Recursividad | ❌ Un estrato no contiene estratos. |

**Veredicto**: ⚠️ Útil como vista complementaria de niveles, no como metáfora principal.

### H5: Habitación / Espacio físico
| Criterio | Evaluación |
|----------|-----------|
| C1: Causas | ⭐ 4 puertas = 4 causas. Intuitivo. |
| C2: Epistémicos | ✅ Luz de la puerta (abierta/cerrada/oscura). |
| C3: Niveles | ⚠️ Edificio → habitaciones → objetos. Funciona pero limitado. |
| C4: Recursividad | ✅ Una puerta puede ser una habitación. |

**Veredicto**: ⚠️ Buena metáfora conceptual, difícil de escalar a grafos densos en 2D. Posible para onboarding/tutorial.

### Recomendación final
**H1 (Molécula)** como metáfora principal de navegación + **H4 (Corte geológico)** como vista complementaria de niveles jerárquicos.

## 5.4 Patrones de navegación (integrados)

| Patrón | Cómo implementa las 4 dimensiones |
|--------|----------------------------------|
| **Foco + Contexto** | Nodo central con detalle (causas visibles), periferia con relaciones (grafo). Reframe cambia el foco. |
| **Breadcrumb trail** | Ruta de zoom: Carpintería > Martillo > Mango. Cada nivel es un sistema. |
| **Split view** | Grafo (vista sistémica) + Ficha (4 causas). Las dos caras del modelo. |
| **Lentes superpuestos** | Filtros: por causa, por estado epistémico, por nivel, por tipo de relación. Un lente por dimensión. |
| **Zoom semántico** | Alejado: agrupación por dominio. Acercado: nodos individuales con causas. La profundidad visual = profundidad sistémica. |

## 5.5 Gaps cerrados vs evaluación anterior

| Gap previo | Solución |
|-----------|----------|
| Emergencia no nombrada | 5.1: 5 propiedades emergentes explícitas |
| Límites ausentes | 5.2: 5 límites claros desde perspectiva del usuario |
| Recursividad sin interacción | US-06: "Convertir relación en sistema" como user story dedicada |
| Hipótesis no evaluadas contra modelo | 5.3: evaluación sistemática contra C1-C4 |
| Falta de integración entre patrones e hipótesis | 5.4: patrones mapeados a dimensiones del modelo |
