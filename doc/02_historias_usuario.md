# 2. Historias de usuario

## HU-0.1 — Crear el esqueleto instalable del benchmark

Como **desarrollador del benchmark**, quiero una estructura de paquete instalable en modo editable, para poder desarrollar, importar y testear módulos de forma consistente.

- **Prioridad:** Must.
- **Complejidad estimada:** Baja.
- **Dependencias:** Ninguna.
- **Criterios de aceptación:**
  - `pip install -e .` funciona.
  - `import unlearning_benchmark` funciona.
  - Existe estructura modular inicial.
  - Existe `environment.yml`.
  - Existe `README.md` inicial.
- **Tests asociados:** `test_package_import.py`.
- **Artefactos generados:** Ninguno experimental.
- **Notas técnicas:** No introducir dependencias innecesarias en esta fase.

---

## HU-0.2 — Definir convenciones mínimas de Git

Como **mantenedor del repositorio**, quiero una política mínima de ramas, commits y PRs, para mantener trazabilidad del desarrollo.

- **Prioridad:** Must.
- **Complejidad estimada:** Baja.
- **Dependencias:** HU-0.1.
- **Criterios de aceptación:**
  - Existe una sección en README con flujo Git.
  - Cada fase se desarrolla en una rama temática.
  - Los artefactos pesados no se versionan.
  - `.gitignore` excluye checkpoints, runs, datasets y caches.
- **Tests asociados:** Revisión manual.
- **Artefactos generados:** `.gitignore`.
- **Notas técnicas:** Versionar código, configs base y documentación; no versionar `artifacts/`.

---

## HU-1.1 — Resolver el sistema de configuración

Como **investigador de Machine Unlearning**, quiero una decisión explícita sobre el sistema de configuración, para que los experimentos sean reproducibles y no dependan de argumentos dispersos.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-0.1.
- **Criterios de aceptación:**
  - Existe un documento breve `ADR-001-config-system.md`.
  - Se decide entre Hydra, YAML simple + argparse o Python config files.
  - La decisión justifica ventajas, limitaciones y coste de mantenimiento.
  - No se implementan scripts definitivos hasta cerrar esta decisión.
- **Tests asociados:** No aplica.
- **Artefactos generados:** ADR de configuración.
- **Notas técnicas:** Esta decisión está pendiente en la especificación y no debe asumirse implícitamente.

---

## HU-1.2 — Guardar configuración efectiva de cada ejecución

Como **revisor científico**, quiero que cada experimento guarde su `config.yaml`, para poder reproducir exactamente la ejecución.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-1.1.
- **Criterios de aceptación:**
  - Cada step guarda `config.yaml`.
  - La configuración contiene dataset, modelo, seed, device, paths, forget strategy, entrenamiento, unlearner, Optuna y debug si aplica.
  - La configuración guardada representa la configuración efectiva final.
- **Tests asociados:** `test_config.py`, `test_debug_pipeline.py`.
- **Artefactos generados:** `config.yaml`.
- **Notas técnicas:** Para `--debug`, queda pendiente decidir si guardar también configuración original u overrides.

---

## HU-2.1 — Implementar dataset `spiral`

Como **desarrollador del benchmark**, quiero un dataset sintético `spiral`, para validar rápidamente el pipeline antes de usar CIFAR-10.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-0.1, HU-1.1.
- **Criterios de aceptación:**
  - Genera 1.000 muestras por defecto.
  - Es binario.
  - Devuelve `(x, y)` en formato PyTorch.
  - Es reproducible con seed.
  - Permite configurar tamaño.
- **Tests asociados:** `test_datasets.py`, `test_reproducibility.py`.
- **Artefactos generados:** Ninguno por sí mismo.
- **Notas técnicas:** Los valores por defecto de `forget_class`, `theta_min`, `theta_max` no están fijados; deben resolverse antes de generar forget set por defecto.

---

## HU-2.2 — Diseñar parámetros por defecto del forget angular en `spiral`

Como **investigador de Machine Unlearning**, quiero fijar formalmente `forget_class`, `theta_min` y `theta_max`, para que `spiral` pueda usarse en modo debug sin configuración manual.

- **Prioridad:** Must.
- **Complejidad estimada:** Baja.
- **Dependencias:** HU-2.1.
- **Criterios de aceptación:**
  - Existe decisión documentada.
  - Se justifica que el forget set no sea vacío ni trivial.
  - Se comprueba que la clase elegida tenga suficientes muestras.
- **Tests asociados:**
  - `test_spiral_forget_region_non_empty`;
  - `test_spiral_forget_region_reproducible`.
- **Artefactos generados:** Actualización de config base.
- **Notas técnicas:** Esta decisión está explícitamente pendiente en la especificación.

---

## HU-2.3 — Implementar generación persistente de splits

Como **usuario que ejecuta experimentos**, quiero generar splits persistentes, para reutilizar exactamente retain, forget, validation y test en distintos steps.

- **Prioridad:** Must.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-2.1, HU-2.2.
- **Criterios de aceptación:**
  - Existe `step_1_generate_splits.py`.
  - Guarda índices `.npy`.
  - Guarda `split_metadata.json`.
  - Guarda `status.json`.
  - Guarda `validation_report.json`.
  - No sobrescribe por defecto.
  - Permite `--overwrite`.
- **Tests asociados:** `test_splits.py`, `test_status.py`.
- **Artefactos generados:**
  - `retain_indices.npy`;
  - `forget_indices.npy`;
  - `validation_indices.npy`;
  - `test_indices.npy`;
  - `split_metadata.json`.
- **Notas técnicas:** En datasets con test oficial, como CIFAR-10, el test oficial debe mantenerse. En `spiral`, se genera split 80/20.

---

## HU-2.4 — Validar no solapamiento de splits

Como **revisor científico**, quiero que el benchmark valide que los splits no se solapan, para evitar contaminación experimental.

- **Prioridad:** Must.
- **Complejidad estimada:** Baja.
- **Dependencias:** HU-2.3.
- **Criterios de aceptación:**
  - `retain ∩ forget = ∅`.
  - `retain ∩ validation = ∅`.
  - `forget ∩ validation = ∅`.
  - `test` no se mezcla con train.
  - Si falla, el step termina en estado `failed`.
- **Tests asociados:**
  - `test_no_overlap_between_splits`;
  - `test_split_sizes_are_consistent`.
- **Artefactos generados:** `validation_report.json`.
- **Notas técnicas:** Aunque aparece como decisión pendiente, es científicamente necesario incluirlo desde el MVP.

---

## HU-3.1 — Implementar registries

Como **desarrollador del benchmark**, quiero resolver datasets, modelos y unlearners por nombre, para evitar lógica condicional rígida.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-0.1.
- **Criterios de aceptación:**
  - Existe registry de datasets.
  - Existe registry de modelos.
  - Existe registry de unlearners.
  - Resolver un nombre inexistente produce error claro.
- **Tests asociados:** `test_registries.py`.
- **Artefactos generados:** Ninguno experimental.
- **Notas técnicas:** La ubicación exacta del registry está pendiente; resolver mediante ADR breve o decisión documentada.

---

## HU-4.1 — Implementar `SpiralMLP`

Como **desarrollador del benchmark**, quiero un MLP para `spiral`, para ejecutar el primer pipeline completo.

- **Prioridad:** Must.
- **Complejidad estimada:** Baja.
- **Dependencias:** HU-2.1, HU-3.1.
- **Criterios de aceptación:**
  - Arquitectura `2 -> 16 -> 16 -> 2`.
  - Activación ReLU.
  - Forward pass correcto.
  - Compatible con batches.
- **Tests asociados:** `test_models.py`.
- **Artefactos generados:** Ninguno.
- **Notas técnicas:** Debe poder construirse desde config/registry.

---

## HU-4.2 — Implementar training loop mínimo

Como **desarrollador del benchmark**, quiero un training loop común, para entrenar modelos de referencia y unlearners sin duplicar lógica.

- **Prioridad:** Must.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-4.1.
- **Criterios de aceptación:**
  - Entrena durante `num_epochs`.
  - Calcula loss y accuracy.
  - Soporta device `cpu` y `cuda`.
  - Respeta seed.
  - Devuelve métricas por época.
- **Tests asociados:** `test_training.py`, `test_reproducibility.py`.
- **Artefactos generados:** Métricas en memoria.
- **Notas técnicas:** Para CIFAR-10 quedan pendientes optimizer/scheduler por defecto de base/naive.

---

## HU-4.3 — Entrenar `init.pth`, `base.pth` y `naive.pth`

Como **investigador de Machine Unlearning**, quiero entrenar modelos de referencia con inicialización común, para comparar el unlearning con un oracle/retraining baseline controlado.

- **Prioridad:** Must.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-2.3, HU-4.2.
- **Criterios de aceptación:**
  - Existe `step_2_train_base_and_naive.py`.
  - Guarda `init.pth`.
  - Entrena `base.pth` con `retain + forget`.
  - Entrena `naive.pth` con `retain`.
  - Reutiliza checkpoints si existen.
  - Permite `--overwrite`.
  - Guarda métricas, config, environment metadata y status.
- **Tests asociados:** `test_checkpoints.py`, `test_training.py`, `test_status.py`.
- **Artefactos generados:**
  - `init.pth`;
  - `base.pth`;
  - `naive.pth`;
  - `metrics_reference.json`;
  - `environment_metadata.json`.
- **Notas técnicas:** Las métricas finales obligatorias de base/naive están pendientes; crear historia de diseño antes de cerrarlas.

---

## HU-4.4 — Diseñar métricas finales de `base.pth` y `naive.pth`

Como **revisor científico**, quiero definir qué métricas se guardan para modelos de referencia, para que la comparación con unlearned sea interpretable.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-4.3.
- **Criterios de aceptación:**
  - Se define si se guarda loss, accuracy o ambas.
  - Se define en qué splits: retain, forget, validation, test.
  - La decisión queda documentada.
  - La evaluación final consume esas métricas de forma consistente.
- **Tests asociados:** `test_metrics.py`.
- **Artefactos generados:** ADR o sección en README técnico.
- **Notas técnicas:** No inventar esta decisión; está pendiente en la especificación.

---

## HU-5.1 — Implementar `BaseUnlearner`

Como **desarrollador del benchmark**, quiero una clase base de unlearners, para que todos los métodos futuros compartan una interfaz mínima.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-3.1, HU-4.2.
- **Criterios de aceptación:**
  - Define `fit`, `unlearn`, `evaluate`, `save`, `load`.
  - Métodos no implementados lanzan `NotImplementedError`.
  - Se documentan argumentos esperados.
- **Tests asociados:** `test_unlearners.py`.
- **Artefactos generados:** Ninguno.
- **Notas técnicas:** Los argumentos obligatorios exactos de cada unlearner están pendientes; crear tarea de diseño.

---

## HU-5.2 — Diseñar interfaz obligatoria de unlearners

Como **mantenedor del repositorio**, quiero definir qué objetos recibe cada unlearner, para evitar incompatibilidades entre métodos futuros.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-5.1.
- **Criterios de aceptación:**
  - Se decide si recibe `model`, loaders, `base_model`, `naive_model`, config completa o subconjunto.
  - Se justifica cómo se soportarán métodos que necesiten forget.
  - Se actualiza `BaseUnlearner`.
- **Tests asociados:** Tests de interfaz.
- **Artefactos generados:** ADR de interfaz.
- **Notas técnicas:** Decisión pendiente explícita.

---

## HU-5.3 — Implementar `FineTuneUnlearner`

Como **investigador de Machine Unlearning**, quiero ejecutar fine-tuning sobre retain desde `base.pth`, para tener el primer baseline de olvido.

- **Prioridad:** Must.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-4.3, HU-5.2.
- **Criterios de aceptación:**
  - Carga `base.pth`.
  - Entrena solo con retain.
  - Actualiza todas las capas.
  - Evalúa validation por época.
  - No usa forget en entrenamiento ni selección por época.
  - Guarda `last.pth`.
  - Guarda `best_val.pth`.
  - Guarda `metrics_epoch.csv`.
- **Tests asociados:** `test_unlearners.py`, `test_training.py`, `test_debug_pipeline.py`.
- **Artefactos generados:**
  - `last.pth`;
  - `best_val.pth`;
  - `metrics_epoch.csv`.
- **Notas técnicas:** El criterio exacto de `best_val.pth` está pendiente.

---

## HU-5.4 — Definir criterio de `best_val.pth`

Como **investigador de Machine Unlearning**, quiero decidir si `best_val.pth` se selecciona por validation loss, validation accuracy u otro criterio configurable, para evitar arbitrariedad en la evaluación final.

- **Prioridad:** Must.
- **Complejidad estimada:** Baja.
- **Dependencias:** HU-5.3.
- **Criterios de aceptación:**
  - Criterio documentado.
  - Implementación configurable si se decide así.
  - Empates resueltos de forma determinista.
- **Tests asociados:** `test_best_checkpoint_selection`.
- **Artefactos generados:** Actualización de config.
- **Notas técnicas:** No debe cerrarse por intuición sin documentarlo.

---

## HU-6.1 — Implementar Optuna para `finetune`

Como **usuario que ejecuta experimentos**, quiero lanzar búsqueda de hiperparámetros para `finetune`, para explorar trade-offs entre utilidad, olvido y eficiencia.

- **Prioridad:** Should para MVP, Must para versión completa inicial.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-5.3, HU-5.4.
- **Criterios de aceptación:**
  - Existe `step_3_optuna_unlearning.py`.
  - Usa `AdamW`.
  - Busca `learning_rate`, `weight_decay`, `batch_size`.
  - Usa `num_epochs=20` salvo debug.
  - Registra runtime.
  - Guarda resultados de trials.
- **Tests asociados:** `test_optuna.py`, `test_debug_pipeline.py`.
- **Artefactos generados:** Resultados de trials.
- **Notas técnicas:** Los objetivos multiobjetivo están pendientes; no codificar objetivos definitivos sin decisión.

---

## HU-6.2 — Definir objetivos multiobjetivo de Optuna

Como **investigador de Machine Unlearning**, quiero definir los objetivos de Optuna, para que la búsqueda represente correctamente el problema científico.

- **Prioridad:** Must antes de Optuna real.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-4.4, HU-5.3.
- **Criterios de aceptación:**
  - Se define cada objetivo.
  - Se especifica si se maximiza o minimiza.
  - Se define qué splits usa cada objetivo.
  - Se justifica por qué no induce leakage experimental.
  - Se documenta que MIA y residual knowledge no entran inicialmente en Optuna.
- **Tests asociados:**
  - `test_objective_values_are_finite`;
  - `test_objective_directions`.
- **Artefactos generados:** ADR de objetivos.
- **Notas técnicas:** La especificación lista opciones posibles, pero no cierra la decisión.

---

## HU-7.1 — Exportar trials a CSV

Como **revisor científico**, quiero exportar todos los trials de Optuna, para inspeccionar resultados sin depender del backend interno.

- **Prioridad:** Should para MVP, Must para versión completa inicial.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-6.1.
- **Criterios de aceptación:**
  - Existe `step_4_select_best_hp.py`.
  - Exporta todos los trials.
  - No selecciona automáticamente un único mejor trial.
  - Incluye columnas mínimas definidas por la especificación.
- **Tests asociados:** `test_optuna_export.py`.
- **Artefactos generados:** `trials.csv`.
- **Notas técnicas:** El almacenamiento persistente de Optuna está pendiente: SQLite, CSV o ambos.

---

## HU-8.1 — Evaluar un trial final con `--trial_id`

Como **usuario que ejecuta experimentos**, quiero evaluar un trial concreto, para obtener el resultado final principal de un método.

- **Prioridad:** Should para MVP, Must para versión completa inicial.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-7.1.
- **Criterios de aceptación:**
  - Existe `step_5_evaluate_final.py`.
  - Acepta `--trial_id`.
  - Recupera hiperparámetros.
  - Carga `base.pth`.
  - Reentrena el unlearner desde cero desde `base.pth`.
  - Usa la misma seed que Optuna.
  - Evalúa `best_val.pth`.
  - Guarda métricas finales e informe.
- **Tests asociados:** `test_evaluate_final.py`, `test_debug_pipeline.py`.
- **Artefactos generados:**
  - `metrics_final.json`;
  - `report.md`;
  - `status.json`.
- **Notas técnicas:** No usar checkpoint temporal de Optuna como resultado final principal.

---

## HU-8.2 — Diseñar comparación final entre modelos

Como **revisor científico**, quiero definir si la evaluación compara siempre `base`, `naive` y `unlearned`, para interpretar utilidad y olvido correctamente.

- **Prioridad:** Must antes de publicación.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-8.1.
- **Criterios de aceptación:**
  - Se define qué modelos se evalúan siempre.
  - Se define qué métricas se reportan por modelo.
  - Se define cómo se representa distancia al oracle/naive si aplica.
- **Tests asociados:** `test_final_metrics_schema`.
- **Artefactos generados:** Esquema de `metrics_final.json`.
- **Notas técnicas:** Decisión pendiente en la especificación.

---

## HU-9.1 — Implementar métricas básicas

Como **investigador de Machine Unlearning**, quiero medir accuracy, loss y runtime, para tener una evaluación mínima interpretable.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-4.2.
- **Criterios de aceptación:**
  - Accuracy y loss se calculan correctamente.
  - Runtime total se registra.
  - Las métricas son serializables a JSON/CSV.
- **Tests asociados:** `test_metrics.py`.
- **Artefactos generados:** `metrics_final.json`.
- **Notas técnicas:** El conjunto final obligatorio de métricas sigue pendiente; implementar núcleo extensible.

---

## HU-9.2 — Diseñar MIA inicial

Como **investigador de Machine Unlearning**, quiero decidir el primer tipo de Membership Inference Attack, para medir riesgo de pertenencia de forma coherente.

- **Prioridad:** Could para MVP, Should para versión completa real.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-8.1, HU-9.1.
- **Criterios de aceptación:**
  - Se decide entre loss-based, confidence-based, entropy-based o combinación.
  - Se define protocolo experimental.
  - Se define qué datos son miembros/no miembros.
  - Se documentan limitaciones.
- **Tests asociados:** Tests posteriores de ataque.
- **Artefactos generados:** ADR de MIA.
- **Notas técnicas:** No usar MIA en spiral, debug ni Optuna inicialmente.

---

## HU-9.3 — Diseñar residual knowledge

Como **investigador de Machine Unlearning**, quiero definir una métrica concreta de residual knowledge, para evaluar si queda información asociada al forget set.

- **Prioridad:** Could para MVP, Should para versión completa real.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-8.1, HU-9.1.
- **Criterios de aceptación:**
  - Se decide entre relearning speed, representation similarity, logit similarity o probe classifier.
  - Se define hipótesis experimental.
  - Se define protocolo y coste computacional.
  - Se documenta qué mide y qué no mide.
- **Tests asociados:** Tests posteriores.
- **Artefactos generados:** ADR de residual knowledge.
- **Notas técnicas:** No usar residual knowledge en Optuna ni debug inicialmente.

---

## HU-10.1 — Guardar `status.json`

Como **usuario que ejecuta experimentos**, quiero que cada step guarde su estado, para diagnosticar ejecuciones fallidas sin perder el resto del batch.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-1.2.
- **Criterios de aceptación:**
  - Estados: `pending`, `running`, `completed`, `failed`, `skipped`.
  - Guarda error type, error message, tiempos, duración y log path.
  - Ante fallo, el estado queda en `failed`.
- **Tests asociados:** `test_status.py`.
- **Artefactos generados:** `status.json`.
- **Notas técnicas:** Debe usarse en todos los steps.

---

## HU-10.2 — Guardar metadata de entorno

Como **revisor científico**, quiero guardar metadata del entorno, para auditar diferencias entre ejecuciones.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-1.2.
- **Criterios de aceptación:**
  - Guarda Python, PyTorch, CUDA, device, hostname, timestamp, git commit y package versions.
- **Tests asociados:** `test_environment_metadata.py`.
- **Artefactos generados:** `environment_metadata.json`.
- **Notas técnicas:** El `git_commit` debe capturarse aunque el repo tenga cambios no commiteados; en ese caso registrar flag `dirty`.

---

## HU-10.3 — Generar reportes `.md`

Como **revisor científico**, quiero reportes legibles por experimento, para interpretar resultados sin abrir manualmente todos los JSON/CSV.

- **Prioridad:** Should.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-8.1, HU-9.1.
- **Criterios de aceptación:**
  - Incluye configuración, split, método, hiperparámetros, métricas, runtime, comparación con referencias, errores y warnings.
  - Si MIA/residual knowledge no aplican, se indica explícitamente.
- **Tests asociados:** `test_reports.py`.
- **Artefactos generados:** `report.md`.
- **Notas técnicas:** El informe global queda pendiente de definición.

---

## HU-11.1 — Crear `experiments_manifest.csv`

Como **usuario que ejecuta experimentos**, quiero un manifest explícito de experimentos planificados, para generar comandos de forma controlada.

- **Prioridad:** Should.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-1.2.
- **Criterios de aceptación:**
  - Existe manifest en `artifacts/manifests/`.
  - Se documentan columnas elegidas.
  - Cada fila identifica un experimento planificado.
- **Tests asociados:** `test_manifest.py`.
- **Artefactos generados:** `experiments_manifest.csv`.
- **Notas técnicas:** Las columnas exactas están pendientes; decidir entre mínimas, extendidas o completas.

---

## HU-11.2 — Generar comandos por step

Como **usuario que ejecuta experimentos**, quiero generar ficheros de comandos, para lanzar el pipeline por fases.

- **Prioridad:** Should.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-11.1.
- **Criterios de aceptación:**
  - Existe `generate_commands.py`.
  - Genera un `.txt` por step.
  - Cada línea es un comando ejecutable.
  - Soporta `--debug`.
- **Tests asociados:** `test_commands.py`.
- **Artefactos generados:**
  - `commands/step_1_generate_splits.txt`;
  - `commands/step_2_train_base_and_naive.txt`;
  - etc.
- **Notas técnicas:** Evitar comandos dependientes de rutas absolutas no configuradas.

---

## HU-11.3 — Ejecutar comandos en paralelo local

Como **usuario que ejecuta experimentos**, quiero ejecutar comandos en paralelo con tolerancia a fallos, para acelerar experimentos sin detener todo el batch.

- **Prioridad:** Could para MVP, Should para versión completa inicial.
- **Complejidad estimada:** Alta.
- **Dependencias:** HU-10.1, HU-11.2.
- **Criterios de aceptación:**
  - Existe `run_commands.py`.
  - Acepta `--jobs`.
  - Si un comando falla, continúa con los demás.
  - Registra fallos.
- **Tests asociados:** `test_run_commands.py`.
- **Artefactos generados:** Logs de ejecución.
- **Notas técnicas:** La política exacta de logs está pendiente.

---

## HU-12.1 — Implementar modo `--debug`

Como **desarrollador del benchmark**, quiero un modo debug rápido, para validar el pipeline completo sin coste computacional alto.

- **Prioridad:** Must.
- **Complejidad estimada:** Media.
- **Dependencias:** HU-1.2, HU-2.1, HU-4.1, HU-5.3.
- **Criterios de aceptación:**
  - Usa `spiral`.
  - Reduce muestras/epochs/trials.
  - Desactiva MIA y residual knowledge.
  - Ejecuta pipeline completo rápido.
  - Guarda configuración efectiva.
- **Tests asociados:** `test_debug_pipeline.py`.
- **Artefactos generados:** Artefactos completos en versión reducida.
- **Notas técnicas:** Decidir si guardar configuración original y overrides.
