# 1. Épicas principales

## E0 — Configuración inicial del repositorio

**Descripción:** Crear la base técnica del proyecto, instalación editable, estructura modular, entorno reproducible y convenciones mínimas de desarrollo.

**Objetivo:** Permitir que cualquier desarrollador pueda instalar, ejecutar tests y comenzar a implementar módulos sin ambigüedad.

**Dependencias:** Ninguna.

**Entregables esperados:**

- `setup.py`;
- `environment.yml`;
- paquete `unlearning_benchmark/`;
- `README.md` inicial;
- estructura `tests/`;
- `.gitignore`;
- estructura base de artefactos;
- primer test de importación del paquete.

---

## E1 — Sistema de configuración y paths

**Descripción:** Definir cómo se cargan, validan y guardan las configuraciones efectivas de cada experimento.

**Objetivo:** Separar configuración, ejecución y evaluación; garantizar trazabilidad experimental.

**Dependencias:** E0.

**Entregables esperados:**

- decisión formal sobre sistema de configuración;
- esquema de `config.yaml`;
- validación de paths;
- guardado de configuración efectiva;
- soporte inicial para `--debug`;
- tests de carga y serialización de configuración.

**Nota:** La especificación deja pendiente si usar Hydra, YAML simple + argparse o Python config files. Esta épica incluye una tarea de decisión previa.

---

## E2 — Gestión de datasets y splits persistentes

**Descripción:** Implementar datasets, generación de splits y persistencia de índices.

**Objetivo:** Garantizar que retain, forget, validation y test sean reproducibles, reutilizables y auditables.

**Dependencias:** E0, E1.

**Entregables esperados:**

- `SpiralDataset`;
- loader inicial de CIFAR-10 sin descarga automática;
- `step_1_generate_splits.py`;
- `retain_indices.npy`;
- `forget_indices.npy`;
- `validation_indices.npy`;
- `test_indices.npy`;
- `split_metadata.json`;
- `validation_report.json`;
- `status.json`;
- tests de no solapamiento y reproducibilidad.

---

## E3 — Registries y construcción modular

**Descripción:** Implementar un mecanismo de registro para datasets, modelos, unlearners, métricas y ataques.

**Objetivo:** Evitar lógica hardcodeada y permitir extensiones futuras.

**Dependencias:** E0.

**Entregables esperados:**

- registry de datasets;
- registry de modelos;
- registry de unlearners;
- registry de métricas;
- registry de ataques;
- tests de registro y resolución por nombre.

**Nota:** La ubicación exacta de los registries está pendiente. Debe resolverse mediante una tarea de diseño.

---

## E4 — Modelos y entrenamiento base/naive

**Descripción:** Implementar modelos, training loop común y entrenamiento de `init.pth`, `base.pth` y `naive.pth`.

**Objetivo:** Construir las referencias experimentales contra las que se evaluará el unlearning.

**Dependencias:** E1, E2, E3.

**Entregables esperados:**

- `SpiralMLP`;
- `ResNet18CIFAR`;
- training loop;
- `step_2_train_base_and_naive.py`;
- checkpoints `init.pth`, `base.pth`, `naive.pth`;
- métricas finales de referencia;
- metadata de entorno;
- tests de forward, entrenamiento mínimo y checkpointing.

---

## E5 — Implementación de unlearners

**Descripción:** Crear la clase base de unlearners y el primer método `FineTuneUnlearner`.

**Objetivo:** Permitir ejecutar métodos de unlearning con una interfaz común.

**Dependencias:** E2, E3, E4.

**Entregables esperados:**

- `BaseUnlearner`;
- `FineTuneUnlearner`;
- entrenamiento sobre retain;
- evaluación por época en validation;
- guardado de `last.pth`;
- guardado de `best_val.pth`;
- `metrics_epoch.csv`;
- tests unitarios e integración rápida.

---

## E6 — Optuna y búsqueda de hiperparámetros

**Descripción:** Implementar búsqueda multiobjetivo para unlearners.

**Objetivo:** Explorar configuraciones de forma trazable sin reducir prematuramente utilidad, olvido, similitud al oracle y eficiencia a un único score.

**Dependencias:** E4, E5.

**Entregables esperados:**

- `step_3_optuna_unlearning.py`;
- espacio de búsqueda de `finetune`;
- registro de trials;
- runtime por trial;
- exportación de resultados;
- tests rápidos con pocos trials.

**Nota:** Los objetivos concretos de Optuna están pendientes y deben cerrarse mediante una tarea de diseño.

---

## E7 — Selección/exportación de hiperparámetros

**Descripción:** Exportar todos los trials a CSV sin seleccionar automáticamente un único mejor modelo.

**Objetivo:** Separar exploración de hiperparámetros y decisión científica.

**Dependencias:** E6.

**Entregables esperados:**

- `step_4_select_best_hp.py`;
- CSV con `trial_id`, `state`, hiperparámetros, `objective_values`, métricas relevantes y runtime;
- tests de exportación.

---

## E8 — Evaluación final

**Descripción:** Ejecutar evaluación final a partir de un `trial_id` manual.

**Objetivo:** Reentrenar el unlearner desde `base.pth` con los hiperparámetros seleccionados y evaluar el checkpoint final.

**Dependencias:** E5, E6, E7.

**Entregables esperados:**

- `step_5_evaluate_final.py`;
- argumento `--trial_id`;
- reentrenamiento desde `base.pth`;
- guardado de `last.pth`, `best_val.pth`, `metrics_final.json`;
- comparación mínima contra referencias;
- informe por experimento.

---

## E9 — Métricas, MIA y residual knowledge

**Descripción:** Implementar métricas básicas primero y dejar MIA/residual knowledge para evaluación final real.

**Objetivo:** Medir utilidad, olvido y desviaciones respecto a referencias, sin contaminar Optuna ni debug con métricas avanzadas todavía no cerradas.

**Dependencias:** E8.

**Entregables esperados:**

- accuracy/loss por split;
- runtime total;
- interfaz de métricas;
- tareas de diseño para MIA;
- tareas de diseño para residual knowledge;
- implementación posterior de ataques/métricas avanzadas.

---

## E10 — Logging, artefactos, status y reportes

**Descripción:** Estandarizar almacenamiento de artefactos, logs, errores, warnings y reportes.

**Objetivo:** Hacer que cada experimento sea trazable, auditable y recuperable ante fallos.

**Dependencias:** E1, E4, E5, E8.

**Entregables esperados:**

- estructura `artifacts/`;
- `status.json`;
- `validation_report.json`;
- `environment_metadata.json`;
- `metrics_epoch.csv`;
- `metrics_final.json`;
- `report.md`;
- tablas globales y filtradas.

---

## E11 — Ejecución masiva de experimentos

**Descripción:** Generar comandos por step y ejecutarlos en paralelo local.

**Objetivo:** Permitir experimentación escalable sin perder control sobre logs, errores y estado.

**Dependencias:** E1, E2, E4, E6, E8, E10.

**Entregables esperados:**

- `experiments_manifest.csv`;
- `generate_commands.py`;
- ficheros `commands/*.txt`;
- `run_commands.py`;
- `summarize_status.py`;
- tests de generación de comandos;
- política de errores por comando.

---

## E12 — Testing, calidad y Git

**Descripción:** Crear una estrategia de calidad con `pytest`, commits pequeños, ramas temáticas y validación continua.

**Objetivo:** Evitar que el benchmark crezca como una colección frágil de scripts.

**Dependencias:** Todas, de forma transversal.

**Entregables esperados:**

- suite de tests;
- fixtures para `tmp_path`;
- tests rápidos para CI/local;
- marcadores para tests lentos;
- convenciones de commits;
- checklist de PR;
- README actualizado.
