# Backlog profesional — Benchmark de Machine Unlearning

Este paquete de documentación transforma la especificación funcional y técnica del benchmark de Machine Unlearning en una planificación profesional de desarrollo. Está organizado para poder usarse como guía de implementación desde cero, con un enfoque incremental, reproducible y científicamente auditable.

## Objetivo del benchmark

Construir una infraestructura modular y extensible para evaluar métodos de Machine Unlearning. El benchmark debe permitir trabajar con datasets, modelos, métodos de unlearning, splits persistentes, entrenamiento de modelos de referencia, búsqueda de hiperparámetros, evaluación final, logging, generación de informes y tests automáticos.

La primera versión debe avanzar en dos niveles:

1. **MVP rápido y controlado:** `spiral + MLP + finetune`.
2. **Extensión real principal:** `CIFAR-10 + ResNet18`.

## Ficheros incluidos

```text
backlog_machine_unlearning_md/
|-- README_BACKLOG.md
|-- 01_epicas.md
|-- 02_historias_usuario.md
|-- 03_tareas_tecnicas.md
|-- 04_roadmap_mvp_testing_git.md
`-- 05_decisiones_pendientes.md
```

## Lectura recomendada

1. Leer primero `01_epicas.md` para entender la arquitectura general del backlog.
2. Leer `02_historias_usuario.md` para ver el desarrollo desde el punto de vista funcional y científico.
3. Usar `03_tareas_tecnicas.md` como lista accionable para implementación.
4. Usar `04_roadmap_mvp_testing_git.md` como orden de desarrollo.
5. Revisar `05_decisiones_pendientes.md` antes de implementar módulos que dependan de decisiones no cerradas.

## Principios de diseño

- No inventar decisiones que la especificación deja pendientes.
- Convertir cada decisión pendiente en una tarea explícita de análisis o diseño.
- Separar configuración, ejecución, evaluación y reporting.
- Guardar siempre artefactos reproducibles: `config.yaml`, `status.json`, `validation_report.json`, checkpoints y métricas.
- Usar seeds configurables y splits persistentes.
- Priorizar tests automáticos desde el MVP.
- Evitar que el benchmark crezca como una colección frágil de scripts.

## MVP recomendado

El MVP mínimo debe incluir:

- instalación editable con `pip install -e .`;
- estructura modular del paquete `unlearning_benchmark/`;
- dataset `spiral`;
- generación de splits persistentes;
- MLP para `spiral`;
- entrenamiento de `init.pth`, `base.pth` y `naive.pth`;
- unlearner `finetune`;
- evaluación final básica;
- guardado de métricas;
- `status.json`;
- `config.yaml`;
- tests unitarios básicos;
- README inicial.

Quedan fuera del MVP: CIFAR-10 completo, MIA, residual knowledge, ejecución masiva paralela, análisis estadístico entre seeds, fairness, multi-GPU y generación automática de figuras.
