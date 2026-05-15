# 4. Roadmap, MVP, testing y Git

## 4.1. Orden recomendado de implementación

### Fase 0 — Preparación del repositorio

**Objetivo:** Crear base instalable y testeable.

**Historias incluidas:**

- HU-0.1;
- HU-0.2.

**Dependencias previas:** Ninguna.

**Entregables:**

- `setup.py`;
- `environment.yml`;
- paquete `unlearning_benchmark`;
- `README.md`;
- `.gitignore`;
- `tests/`.

**Tests mínimos antes de avanzar:**

- `test_package_import.py`.

**Criterio de finalización:** El paquete se instala con `pip install -e .` y puede importarse desde Python.

---

### Fase 1 — Decisiones arquitectónicas mínimas

**Objetivo:** Resolver decisiones que bloquean la implementación limpia.

**Historias incluidas:**

- HU-1.1;
- HU-3.1, al menos decisión de ubicación;
- HU-5.2, al menos interfaz mínima;
- HU-1.2 parcialmente.

**Dependencias previas:** Fase 0.

**Entregables:**

- ADR de configuración;
- ADR de registry;
- ADR de interfaz de unlearners;
- esquema inicial de `config.yaml`.

**Tests mínimos antes de avanzar:**

- tests de carga de config;
- tests de registry.

**Criterio de finalización:** Se puede construir un objeto dataset/model/unlearner desde una configuración efectiva.

---

### Fase 2 — Dataset `spiral` y splits

**Objetivo:** Implementar el dataset de desarrollo/debug y la generación persistente de splits.

**Historias incluidas:**

- HU-2.1;
- HU-2.2;
- HU-2.3;
- HU-2.4.

**Dependencias previas:** Fase 1.

**Entregables:**

- `SpiralDataset`;
- `step_1_generate_splits.py`;
- índices `.npy`;
- `split_metadata.json`;
- `validation_report.json`;
- `status.json`.

**Tests mínimos antes de avanzar:**

- `test_datasets.py`;
- `test_splits.py`;
- `test_status.py`.

**Criterio de finalización:** Para una seed fija, el split `spiral` se reproduce exactamente y no hay solapamientos.

---

### Fase 3 — Modelo MLP y training loop mínimo

**Objetivo:** Poder entrenar un modelo simple sobre `spiral`.

**Historias incluidas:**

- HU-4.1;
- HU-4.2;
- HU-9.1 parcialmente.

**Dependencias previas:** Fase 2.

**Entregables:**

- `SpiralMLP`;
- training loop;
- evaluación de loss/accuracy;
- tests de forward y entrenamiento mínimo.

**Tests mínimos antes de avanzar:**

- `test_models.py`;
- `test_training.py`;
- `test_metrics.py`.

**Criterio de finalización:** El MLP entrena durante pocas épocas en `spiral` y produce métricas finitas.

---

### Fase 4 — Modelos `base.pth` y `naive.pth`

**Objetivo:** Crear las referencias experimentales del benchmark.

**Historias incluidas:**

- HU-4.3;
- HU-4.4;
- HU-10.1;
- HU-10.2.

**Dependencias previas:** Fase 3.

**Entregables:**

- `step_2_train_base_and_naive.py`;
- `init.pth`;
- `base.pth`;
- `naive.pth`;
- métricas de referencia;
- `environment_metadata.json`.

**Tests mínimos antes de avanzar:**

- `test_checkpoints.py`;
- `test_training.py`;
- `test_status.py`;
- `test_environment_metadata.py`.

**Criterio de finalización:** `base.pth` y `naive.pth` se entrenan desde la misma inicialización y se guardan/reutilizan correctamente.

---

### Fase 5 — `FineTuneUnlearner`

**Objetivo:** Implementar el primer método de Machine Unlearning.

**Historias incluidas:**

- HU-5.1;
- HU-5.3;
- HU-5.4.

**Dependencias previas:** Fase 4.

**Entregables:**

- `BaseUnlearner`;
- `FineTuneUnlearner`;
- `last.pth`;
- `best_val.pth`;
- `metrics_epoch.csv`.

**Tests mínimos antes de avanzar:**

- `test_unlearners.py`;
- `test_best_checkpoint_selection`;
- test que verifica que forget no se usa durante entrenamiento.

**Criterio de finalización:** `finetune` carga `base.pth`, entrena solo con retain y guarda checkpoints correctos.

---

### Fase 6 — Evaluación final mínima

**Objetivo:** Cerrar un pipeline completo sin Optuna.

**Historias incluidas:**

- HU-8.1 adaptada temporalmente a hiperparámetros manuales;
- HU-8.2;
- HU-9.1;
- HU-10.3;
- HU-12.1.

**Dependencias previas:** Fase 5.

**Entregables:**

- evaluación final básica;
- `metrics_final.json`;
- `report.md`;
- modo `--debug` completo.

**Tests mínimos antes de avanzar:**

- `test_evaluate_final.py`;
- `test_debug_pipeline.py`.

**Criterio de finalización:** Un comando debug ejecuta split, entrenamiento base/naive, finetune y evaluación final básica.

---

### Fase 7 — Optuna

**Objetivo:** Añadir búsqueda de hiperparámetros.

**Historias incluidas:**

- HU-6.1;
- HU-6.2;
- HU-7.1;
- HU-8.1 completa con `--trial_id`.

**Dependencias previas:** Fase 6.

**Entregables:**

- `step_3_optuna_unlearning.py`;
- `step_4_select_best_hp.py`;
- `trials.csv`;
- evaluación final por `--trial_id`.

**Tests mínimos antes de avanzar:**

- `test_optuna.py`;
- `test_optuna_export.py`;
- test con `n_trials=2`.

**Criterio de finalización:** Se puede lanzar Optuna en debug, exportar trials y evaluar manualmente un trial.

---

### Fase 8 — CIFAR-10 + ResNet18

**Objetivo:** Extender el MVP al dataset real principal.

**Historias incluidas:**

- loader CIFAR-10;
- `ResNet18CIFAR`;
- class-wise forgetting inicial;
- entrenamiento base/naive para CIFAR-10;
- finetune sobre retain.

**Dependencias previas:** Fase 7.

**Entregables:**

- dataset CIFAR-10 sin descarga automática;
- normalización configurable;
- ResNet18 adaptada a CIFAR;
- splits CIFAR-10;
- pipeline real.

**Tests mínimos antes de avanzar:**

- tests unitarios de loader;
- test forward ResNet18;
- test lento opcional marcado con `@pytest.mark.slow`.

**Criterio de finalización:** El pipeline puede ejecutarse para CIFAR-10 + ResNet18 en al menos una seed y una estrategia de forget cerrada.

---

### Fase 9 — Reportes, tablas y ejecución masiva

**Objetivo:** Escalar de experimentos individuales a batches.

**Historias incluidas:**

- HU-11.1;
- HU-11.2;
- HU-11.3;
- HU-10.3.

**Dependencias previas:** Fase 8.

**Entregables:**

- `experiments_manifest.csv`;
- comandos por step;
- ejecución paralela local;
- tabla global;
- tablas filtradas.

**Tests mínimos antes de avanzar:**

- `test_manifest.py`;
- `test_commands.py`;
- `test_run_commands.py`;
- tests de resumen de status.

**Criterio de finalización:** Se pueden generar comandos para múltiples seeds y ejecutar sin que un fallo detenga todo el batch.

---

### Fase 10 — MIA, residual knowledge y métricas avanzadas

**Objetivo:** Añadir evaluación científica avanzada.

**Historias incluidas:**

- HU-9.2;
- HU-9.3;
- métricas de distancia al naive/oracle;
- posible análisis estadístico futuro.

**Dependencias previas:** Fase 9.

**Entregables:**

- protocolo MIA;
- implementación de ataque inicial;
- protocolo residual knowledge;
- implementación de métrica inicial;
- extensión de reportes.

**Tests mínimos antes de avanzar:**

- tests unitarios de scores;
- tests de integración en evaluación final;
- tests que verifiquen que no se ejecutan en debug ni Optuna.

**Criterio de finalización:** Los experimentos reales pueden evaluarse con MIA y residual knowledge sin contaminar Optuna ni debug.

---

## 4.2. MVP recomendado

El MVP mínimo funcional debe centrarse en demostrar que la arquitectura funciona de extremo a extremo con coste bajo. No debe intentar resolver todas las métricas avanzadas ni ejecutar CIFAR-10 desde el primer día.

### Debe incluir

- instalación editable con `pip install -e .`;
- estructura modular del paquete `unlearning_benchmark/`;
- `environment.yml`;
- `README.md` inicial;
- sistema de configuración ya decidido;
- guardado de `config.yaml`;
- dataset `spiral`;
- decisión cerrada de `forget_class`, `theta_min`, `theta_max` para `spiral`;
- generación de splits persistentes;
- validación de no solapamiento;
- `split_metadata.json`;
- `validation_report.json`;
- `status.json`;
- `SpiralMLP`;
- training loop mínimo;
- control de seeds;
- entrenamiento de `init.pth`, `base.pth` y `naive.pth`;
- `FineTuneUnlearner`;
- guardado de `last.pth` y `best_val.pth`;
- criterio definido para `best_val.pth`;
- métricas básicas: loss, accuracy y runtime;
- `metrics_epoch.csv`;
- `metrics_final.json`;
- evaluación final básica;
- modo `--debug`;
- tests unitarios básicos;
- test end-to-end rápido con `spiral`.

### Puede quedar fuera del MVP

- CIFAR-10 + ResNet18 completo;
- Optuna real, aunque puede existir una versión mínima posterior;
- MIA;
- residual knowledge;
- ejecución masiva paralela;
- reportes globales complejos;
- análisis estadístico entre seeds;
- MNIST;
- dataset de superhéroes;
- multi-GPU;
- VRAM/FLOPs/energía;
- generación automática de figuras;
- selección automática de punto del Pareto front;
- fairness.

### Decisiones que deben resolverse antes de cerrar el MVP

- sistema de configuración;
- valores por defecto del forget angular en `spiral`;
- ubicación de registries;
- uso de `Subset` o wrapper propio;
- interfaz mínima de unlearners;
- criterio de `best_val.pth`;
- métricas básicas obligatorias de referencia;
- esquema mínimo de `metrics_final.json`;
- política de guardado bajo `--debug`.

---

## 4.3. Estrategia de testing

La estrategia debe basarse en `pytest`, separando tests rápidos, tests de integración y tests lentos. El principio central es que cada módulo científico debe tener tests de invariantes, no solo tests de ejecución.

### Estructura recomendada

```text
tests/
|-- test_package_import.py
|-- test_config.py
|-- test_datasets.py
|-- test_splits.py
|-- test_registries.py
|-- test_models.py
|-- test_training.py
|-- test_checkpoints.py
|-- test_unlearners.py
|-- test_metrics.py
|-- test_optuna.py
|-- test_optuna_export.py
|-- test_evaluate_final.py
|-- test_commands.py
|-- test_manifest.py
|-- test_status.py
|-- test_environment_metadata.py
|-- test_reports.py
`-- test_debug_pipeline.py
```

### Tests unitarios

#### Datasets

Archivo: `tests/test_datasets.py`

Debe comprobar:

- `SpiralDataset` tiene longitud esperada.
- Cada muestra devuelve `(x, y)`.
- `x` tiene dimensión 2.
- `y` pertenece a `{0, 1}`.
- La generación es reproducible con seed.
- Cambiar seed cambia el dataset, salvo casos degenerados.

#### Splits

Archivo: `tests/test_splits.py`

Debe comprobar:

- Se generan los cuatro índices.
- Los índices están en rango.
- No hay duplicados dentro de cada split.
- No hay solapamiento entre retain, forget y validation.
- Test no se mezcla con train.
- La suma de tamaños es consistente.
- `--overwrite=False` no sobrescribe.
- `--overwrite=True` permite regenerar.

#### Reproducibilidad

Archivo: `tests/test_reproducibility.py`

Debe comprobar:

- Misma seed produce mismos splits.
- Misma seed produce misma inicialización `init.pth` en CPU.
- La configuración efectiva se guarda.
- El modo reproducible fija seeds de Python, NumPy y PyTorch.

#### Modelos

Archivo: `tests/test_models.py`

Debe comprobar:

- `SpiralMLP` acepta input `(batch, 2)`.
- Devuelve output `(batch, 2)`.
- Todos los parámetros esperados son entrenables.
- El modelo se mueve correctamente a `cpu`.
- Si hay CUDA disponible, smoke test opcional en `cuda`.

#### Training loop

Archivo: `tests/test_training.py`

Debe comprobar:

- `train_one_epoch` devuelve loss finita.
- `evaluate` devuelve accuracy entre 0 y 1.
- El training loop no modifica datos.
- El training loop funciona con batch pequeño.
- El training loop soporta `num_epochs=1`.

#### Checkpoints

Archivo: `tests/test_checkpoints.py`

Debe comprobar:

- Se guarda `init.pth`.
- Se guarda `base.pth`.
- Se guarda `naive.pth`.
- Un checkpoint cargado produce forward pass válido.
- `base` y `naive` parten de la misma inicialización.
- `--overwrite=False` reutiliza checkpoints existentes.

#### Unlearners

Archivo: `tests/test_unlearners.py`

Debe comprobar:

- `BaseUnlearner` impone interfaz.
- `FineTuneUnlearner` entrena sobre retain.
- `FineTuneUnlearner` no usa forget durante fit.
- Se guarda `last.pth`.
- Se guarda `best_val.pth`.
- El criterio de best checkpoint es determinista.
- `metrics_epoch.csv` contiene columnas mínimas.

#### Métricas

Archivo: `tests/test_metrics.py`

Debe comprobar:

- Accuracy correcta en casos simples.
- Loss media correcta.
- Runtime serializable.
- Métricas convertibles a JSON.
- Métricas ausentes producen error claro, no valores silenciosos.

#### Status

Archivo: `tests/test_status.py`

Debe comprobar:

- Estado inicial `running`.
- Estado final `completed`.
- Ante excepción se guarda `failed`.
- Se guarda `error_type`.
- Se guarda `error_message`.
- Se guarda duración.

#### Configuración

Archivo: `tests/test_config.py`

Debe comprobar:

- Carga config base.
- Aplica overrides.
- Guarda config efectiva.
- Valida campos obligatorios.
- Falla si falta dataset/model/seed.
- Falla si paths requeridos son inválidos.

---

## 4.4. Tests de integración

### Pipeline mínimo de splits

Debe ejecutar `step_1_generate_splits.py` con `tmp_path` y verificar artefactos.

### Entrenamiento base/naive

Debe ejecutar una configuración pequeña de `spiral`, entrenar 1-2 epochs y comprobar checkpoints.

### FineTune

Debe cargar `base.pth`, ejecutar fine-tuning y comprobar checkpoints y métricas.

### Evaluación final

Debe ejecutar evaluación básica y comprobar `metrics_final.json`.

---

## 4.5. Tests end-to-end rápidos con `spiral`

Archivo: `tests/test_debug_pipeline.py`

Debe ejecutar el pipeline completo en modo debug:

1. generar splits;
2. entrenar `base.pth` y `naive.pth`;
3. ejecutar `finetune`;
4. evaluar modelo final;
5. comprobar artefactos finales.

Debe ser rápido y ejecutable localmente antes de cada commit relevante.

---

## 4.6. Tests lentos opcionales para CIFAR-10

Marcar con:

```python
@pytest.mark.slow
```

Deben incluir:

- carga de CIFAR-10 desde `data_dir`;
- comprobación de que no se descarga automáticamente;
- forward pass de `ResNet18CIFAR`;
- generación de split class-wise;
- entrenamiento smoke test de 1 epoch o pocos batches;
- evaluación básica.

Estos tests no deben bloquear el desarrollo diario, pero sí deben poder ejecutarse antes de experimentos reales.

---

## 4.7. Tests de generación de comandos

Archivo: `tests/test_commands.py`

Debe comprobar:

- `generate_commands.py` produce un fichero por step.
- Cada comando contiene dataset, model, seed y paths.
- No genera comandos para decisiones pendientes no resueltas.
- `--debug` genera comandos reducidos.
- Los comandos no sobrescriben artefactos por defecto.

---

## 4.8. Tests de manejo de errores

Debe comprobarse que:

- dataset inexistente produce `failed`;
- checkpoint ausente produce `failed`;
- `trial_id` inexistente produce `failed`;
- forget strategy sin parámetros obligatorios produce `failed`;
- incompatibilidad dataset/model produce `failed`;
- el error queda registrado en `status.json`;
- `run_commands.py` continúa con otros comandos.

---

## 4.9. Buenas prácticas de Git y calidad de código

Aunque la especificación indica que no se priorizarán inicialmente herramientas como black, ruff o linters, sí conviene aplicar disciplina mínima desde el principio:

- una rama por épica o fase;
- commits pequeños y descriptivos;
- no mezclar cambios de formato con cambios funcionales;
- todo commit que modifique lógica experimental debe incluir o actualizar tests;
- no versionar datasets, checkpoints ni runs;
- versionar configs base, ADRs, README y tests;
- etiquetar hitos:
  - `v0.1-spiral-mvp`;
  - `v0.2-finetune-debug`;
  - `v0.3-optuna`;
  - `v0.4-cifar10-resnet18`.

Antes de merge:

- `pytest` debe pasar;
- el pipeline debug debe ejecutarse;
- README debe reflejar cualquier cambio de uso.
