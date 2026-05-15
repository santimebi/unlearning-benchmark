# 3. Tareas técnicas derivadas

Este documento traduce las historias de usuario en tareas accionables de implementación. La intención es que cada bloque pueda convertirse fácilmente en issues de GitHub/GitLab.

---

## HU-0.1 — Crear el esqueleto instalable del benchmark

- Crear `setup.py`.
- Crear `environment.yml`.
- Crear paquete `unlearning_benchmark/`.
- Crear submódulos:
  - `datasets/`;
  - `models/`;
  - `training/`;
  - `unlearning/`;
  - `evaluation/`;
  - `metrics/`;
  - `attacks/`;
  - `configs/`;
  - `scripts/`.
- Crear `tests/`.
- Añadir `__init__.py` donde corresponda.
- Crear test `tests/test_package_import.py`.
- Verificar instalación editable con `pip install -e .`.

---

## HU-0.2 — Definir convenciones mínimas de Git

- Crear `.gitignore`.
- Excluir:
  - `artifacts/`;
  - `data/`;
  - `datasets/`;
  - `*.pth`;
  - `*.pt`;
  - `*.npy`;
  - `.pytest_cache/`;
  - `__pycache__/`;
  - outputs temporales.
- Añadir sección de Git al README:
  - ramas por feature;
  - commits pequeños;
  - no mezclar refactor + funcionalidad;
  - tests antes de merge;
  - no versionar checkpoints.
- Definir convención de nombres:
  - `feature/splits`;
  - `feature/finetune-unlearner`;
  - `fix/status-json`;
  - `exp/cifar10-resnet18-debug`.

---

## HU-1.1 — Resolver el sistema de configuración

- Crear carpeta de decisiones técnicas, por ejemplo `docs_decisions/` o `adr/`.
- Crear `ADR-001-config-system.md`.
- Comparar Hydra, YAML simple + argparse y Python config files.
- Evaluar:
  - reproducibilidad;
  - simplicidad;
  - soporte para overrides;
  - coste de mantenimiento;
  - facilidad de guardar configuración efectiva;
  - compatibilidad con ejecución por scripts directos.
- Cerrar decisión antes de implementar scripts definitivos.

---

## HU-1.2 — Guardar configuración efectiva de cada ejecución

- Implementar función `load_config(path, overrides=None)`.
- Implementar función `save_effective_config(config, output_path)`.
- Definir esquema mínimo de config.
- Añadir sección `paths`.
- Añadir sección `dataset`.
- Añadir sección `model`.
- Añadir sección `training`.
- Añadir sección `unlearner`.
- Añadir sección `optuna`.
- Añadir sección `debug`.
- Añadir validación de campos obligatorios.
- Crear tests de serialización.

---

## HU-2.1 — Implementar dataset `spiral`

- Crear `unlearning_benchmark/datasets/spiral.py`.
- Implementar generación determinista con seed.
- Devolver tensores o arrays compatibles con PyTorch.
- Implementar `__len__`.
- Implementar `__getitem__`.
- Añadir parámetros:
  - `n_samples`;
  - `noise`;
  - `seed`;
  - parámetros geométricos si aplican.
- Añadir tests de tamaño, forma, clases y reproducibilidad.

---

## HU-2.2 — Diseñar parámetros por defecto del forget angular en `spiral`

- Crear documento de decisión sobre forget angular.
- Implementar función `select_spiral_forget_indices(...)`.
- Validar que `forget_class` existe.
- Validar que `theta_min < theta_max` o documentar convención circular.
- Validar que el forget set no es vacío.
- Añadir tests con seeds fijas.
- Añadir error claro si faltan parámetros obligatorios.

---

## HU-2.3 — Implementar generación persistente de splits

- Crear `unlearning_benchmark/scripts/step_1_generate_splits.py`.
- Implementar carga de dataset desde registry.
- Implementar split 80/20 para `spiral`.
- Implementar validation 10% del train.
- Implementar selección de forget.
- Implementar retain como complemento.
- Guardar:
  - `retain_indices.npy`;
  - `forget_indices.npy`;
  - `validation_indices.npy`;
  - `test_indices.npy`.
- Guardar `split_metadata.json`.
- Añadir `--overwrite`.
- Añadir `status.json`.
- Añadir `validation_report.json`.

---

## HU-2.4 — Validar no solapamiento de splits

- Implementar `validate_split_disjointness`.
- Implementar `validate_split_sizes`.
- Implementar `validate_indices_in_range`.
- Añadir validación de duplicados.
- Añadir validación de cobertura esperada.
- Hacer que errores graves bloqueen el step.
- Guardar warnings y errores en `validation_report.json`.
- Añadir tests con splits válidos e inválidos.

---

## HU-3.1 — Implementar registries

- Resolver ubicación del registry.
- Implementar `Registry` genérico o diccionarios explícitos.
- Crear:
  - `DATASET_REGISTRY`;
  - `MODEL_REGISTRY`;
  - `UNLEARNER_REGISTRY`;
  - `METRIC_REGISTRY`;
  - `ATTACK_REGISTRY`.
- Implementar `get_dataset(name)`.
- Implementar `get_model(name)`.
- Implementar `get_unlearner(name)`.
- Añadir errores con nombres disponibles.
- Añadir tests para registro correcto y nombre inexistente.

---

## HU-4.1 — Implementar `SpiralMLP`

- Crear `unlearning_benchmark/models/mlp.py`.
- Implementar `SpiralMLP`.
- Registrar como `mlp_spiral`.
- Añadir forward test:
  - input shape `(batch_size, 2)`;
  - output shape `(batch_size, 2)`.
- Añadir test de parámetros entrenables.
- Añadir test de compatibilidad CPU.

---

## HU-4.2 — Implementar training loop mínimo

- Crear `unlearning_benchmark/training/loops.py`.
- Implementar `train_one_epoch`.
- Implementar `evaluate`.
- Implementar `fit_model`.
- Añadir cálculo de loss media.
- Añadir cálculo de accuracy.
- Añadir soporte para device.
- Añadir control de seed.
- Añadir progreso opcional.
- Añadir retorno de métricas por época.
- Añadir tests con dataset pequeño.

---

## HU-4.3 — Entrenar `init.pth`, `base.pth` y `naive.pth`

- Crear `unlearning_benchmark/scripts/step_2_train_base_and_naive.py`.
- Implementar carga de splits.
- Implementar construcción de dataloaders:
  - base: retain + forget;
  - naive: retain.
- Crear `init.pth` si no existe.
- Cargar `init.pth` antes de entrenar base.
- Cargar `init.pth` antes de entrenar naive.
- Guardar checkpoints.
- Implementar política `--overwrite`.
- Guardar métricas.
- Guardar metadata de entorno.
- Guardar status.
- Añadir tests con `spiral`.

---

## HU-4.4 — Diseñar métricas finales de `base.pth` y `naive.pth`

- Crear documento `ADR-002-reference-metrics.md`.
- Definir métricas para `base` y `naive`.
- Definir splits de evaluación.
- Definir esquema JSON.
- Implementar función `evaluate_reference_models`.
- Añadir tests del esquema.

---

## HU-5.1 — Implementar `BaseUnlearner`

- Crear `unlearning_benchmark/unlearning/base.py`.
- Implementar `BaseUnlearner`.
- Añadir métodos abstractos o métodos que lancen `NotImplementedError`.
- Añadir docstrings.
- Añadir tests de interfaz.

---

## HU-5.2 — Diseñar interfaz obligatoria de unlearners

- Crear `ADR-003-unlearner-interface.md`.
- Definir argumentos mínimos.
- Definir cómo pasar loaders.
- Definir cómo pasar modelos de referencia si un método futuro los necesita.
- Definir cómo guardar checkpoints.
- Definir contrato de retorno de métricas.
- Actualizar `BaseUnlearner`.

---

## HU-5.3 — Implementar `FineTuneUnlearner`

- Crear `unlearning_benchmark/unlearning/finetune.py`.
- Implementar `FineTuneUnlearner`.
- Registrar `finetune`.
- Cargar modelo base.
- Entrenar con retain loader.
- Evaluar con validation loader.
- Guardar `last.pth`.
- Guardar `best_val.pth`.
- Guardar `metrics_epoch.csv`.
- Evitar cualquier uso de forget durante entrenamiento.
- Añadir tests con `spiral`.

---

## HU-5.4 — Definir criterio de `best_val.pth`

- Crear `ADR-004-best-val-criterion.md`.
- Definir criterio.
- Implementar selector de checkpoint.
- Añadir desempate determinista.
- Añadir test con métricas simuladas.
- Añadir campo en config:
  - `checkpoint_selection.metric`;
  - `checkpoint_selection.mode`.

---

## HU-6.1 — Implementar Optuna para `finetune`

- Crear `unlearning_benchmark/scripts/step_3_optuna_unlearning.py`.
- Implementar creación/carga de estudio.
- Implementar espacio de búsqueda de `finetune`.
- Implementar ejecución de trial.
- Medir runtime.
- Guardar métricas del trial.
- Guardar estado.
- Soportar `--debug` con pocos trials.
- Añadir tests con `n_trials=2`.

---

## HU-6.2 — Definir objetivos multiobjetivo de Optuna

- Crear `ADR-005-optuna-objectives.md`.
- Definir objetivos.
- Definir dirección de cada objetivo.
- Definir splits usados.
- Justificar exclusión de MIA y residual knowledge de Optuna.
- Implementar función `compute_objective_values`.
- Añadir tests de outputs finitos y orden de objetivos.

---

## HU-7.1 — Exportar trials a CSV

- Crear `unlearning_benchmark/scripts/step_4_select_best_hp.py`.
- Implementar lectura de resultados.
- Exportar `trials.csv`.
- Incluir columnas:
  - `trial_id`;
  - `state`;
  - `learning_rate`;
  - `weight_decay`;
  - `batch_size`;
  - `num_epochs`;
  - `objective_values`;
  - `relevant_metrics`;
  - `runtime`.
- No seleccionar automáticamente mejor trial.
- Añadir tests con estudio dummy.

---

## HU-8.1 — Evaluar un trial final con `--trial_id`

- Crear `unlearning_benchmark/scripts/step_5_evaluate_final.py`.
- Parsear `--trial_id`.
- Validar existencia del trial.
- Recuperar hiperparámetros.
- Cargar `base.pth`.
- Reentrenar `FineTuneUnlearner`.
- Guardar checkpoints.
- Evaluar `best_val.pth`.
- Guardar `metrics_final.json`.
- Guardar `report.md`.
- Guardar `status.json`.
- Añadir tests end-to-end con `spiral`.

---

## HU-8.2 — Diseñar comparación final entre modelos

- Crear `ADR-006-final-comparison.md`.
- Definir si se evalúan siempre `base`, `naive`, `unlearned`.
- Definir esquema de comparación.
- Implementar `evaluation/compare_models.py`.
- Añadir tests de schema.

---

## HU-9.1 — Implementar métricas básicas

- Crear `unlearning_benchmark/metrics/basic.py`.
- Implementar `accuracy`.
- Implementar `mean_loss`.
- Implementar `runtime_seconds`.
- Implementar serialización JSON-safe.
- Añadir tests numéricos simples.
- Registrar métricas básicas.

---

## HU-9.2 — Diseñar MIA inicial

- Crear `ADR-007-mia-protocol.md`.
- Definir ataque inicial.
- Definir datos miembros/no miembros.
- Definir score.
- Definir métrica de ataque.
- Posponer implementación hasta fase avanzada.
- Añadir placeholder seguro que falle con mensaje claro si se llama sin configurar.

---

## HU-9.3 — Diseñar residual knowledge

- Crear `ADR-008-residual-knowledge.md`.
- Definir métrica inicial.
- Definir protocolo experimental.
- Definir coste computacional.
- Posponer implementación hasta evaluación final real.
- Añadir interfaz extensible en `metrics/residual.py`.

---

## HU-10.1 — Guardar `status.json`

- Crear `unlearning_benchmark/utils/status.py`.
- Implementar `write_status`.
- Implementar context manager `experiment_status`.
- Registrar:
  - `started_at`;
  - `finished_at`;
  - `duration_seconds`;
  - `error_type`;
  - `error_message`;
  - `log_path`.
- Añadir tests de éxito y fallo.

---

## HU-10.2 — Guardar metadata de entorno

- Crear `unlearning_benchmark/utils/environment.py`.
- Capturar versiones.
- Capturar CUDA.
- Capturar hostname.
- Capturar git commit.
- Capturar estado dirty del repo.
- Guardar `environment_metadata.json`.
- Añadir test que valide claves obligatorias.

---

## HU-10.3 — Generar reportes `.md`

- Crear `unlearning_benchmark/reporting/experiment_report.py`.
- Implementar render Markdown.
- Incluir configuración, split, métricas, runtime, referencias y warnings.
- Indicar explícitamente métricas no aplicables.
- Añadir tests de contenido mínimo.

---

## HU-11.1 — Crear `experiments_manifest.csv`

- Crear `manifests/create_manifest.py` o script equivalente.
- Resolver columnas del manifest mediante ADR.
- Validar filas.
- Guardar en `artifacts/manifests/experiments_manifest.csv`.
- Añadir tests de lectura y validación.

---

## HU-11.2 — Generar comandos por step

- Crear `unlearning_benchmark/scripts/generate_commands.py`.
- Leer manifest.
- Generar comandos por step.
- Validar paths.
- Soportar `--debug`.
- Añadir tests de comandos esperados.

---

## HU-11.3 — Ejecutar comandos en paralelo local

- Crear `unlearning_benchmark/scripts/run_commands.py`.
- Leer comandos línea a línea.
- Ejecutar con `subprocess`.
- Añadir `--jobs`.
- Continuar ante fallos.
- Guardar logs según decisión pendiente.
- Añadir tests con comandos dummy.

---

## HU-12.1 — Implementar modo `--debug`

- Implementar aplicación de overrides debug.
- Reducir muestras, epochs y trials.
- Forzar dataset/modelo pequeño.
- Desactivar MIA/residual knowledge.
- Guardar config efectiva.
- Añadir test end-to-end rápido:
  - split;
  - train base/naive;
  - finetune;
  - evaluación básica.
