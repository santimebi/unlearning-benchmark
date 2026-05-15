# 5. Decisiones pendientes y tareas de análisis

Este documento recoge las decisiones que no deben implementarse mediante supuestos arbitrarios. Cada punto debe convertirse en una tarea de análisis, diseño experimental o ADR antes de cerrar la implementación correspondiente.

---

## 5.1. Forget sets

### Pendiente 1 — Clase concreta para class-wise forgetting

No se ha definido si:

- se olvidará siempre una clase fija;
- se probarán las 10 clases de CIFAR-10 por separado;
- se olvidarán varias clases;
- se empezará con una clase y luego se extenderá.

**Tarea recomendada:** crear `ADR-forget-class-wise.md`.

**Criterio de cierre:** dejar definida la política inicial y su extensión futura.

---

### Pendiente 2 — Regla para partial class forgetting

No se ha definido si el subconjunto parcial se elegirá por:

- porcentaje fijo;
- número fijo de muestras;
- dificultad;
- configuración semi-manual.

**Tarea recomendada:** posponer fuera del MVP, salvo que se necesite para CIFAR-10 en la primera versión real.

---

### Pendiente 3 — Regla para hard-sample forgetting

No se ha definido cómo identificar hard samples:

- mayor loss;
- menor confidence;
- mayor entropía;
- muestras mal clasificadas;
- combinación configurable.

**Tarea recomendada:** definir protocolo después de tener entrenamiento base estable.

---

## 5.2. Validation

### Pendiente 4 — Política exacta de validation

No se ha decidido si validation será:

- validation general con todas las clases;
- validation solo retain;
- `retain_validation` y `forget_validation`;
- configurable por estrategia.

**Riesgo científico:** usar una validation que contenga datos conceptualmente cercanos al forget set puede sesgar la selección de checkpoints o hiperparámetros.

**Tarea recomendada:** crear ADR antes de cerrar Optuna y `best_val.pth`.

---

## 5.3. Entrenamiento base/naive

### Pendiente 5 — Optimizer y scheduler para `base.pth` y `naive.pth`

Está definido que el entrenamiento será configurable y que por defecto habrá 100 epochs, pero no se ha fijado:

- optimizer;
- learning rate;
- weight decay;
- scheduler.

**Tarea recomendada:** cerrar antes de CIFAR-10 + ResNet18, no necesariamente antes del MVP `spiral`.

---

### Pendiente 6 — Métricas finales de `base.pth` y `naive.pth`

No se ha definido si guardar:

- accuracy y loss en retain/forget/validation/test;
- solo accuracy;
- solo validation/test;
- métricas configurables.

**Tarea recomendada:** cerrar antes de implementar comparación final.

---

## 5.4. Unlearners

### Pendiente 7 — Entradas obligatorias de cada `Unlearner`

No se ha cerrado si cada unlearner recibirá:

- `model`;
- `retain_loader`;
- `forget_loader`;
- `val_loader`;
- `test_loader`;
- `base_model`;
- `naive_model`;
- configuración completa.

**Tarea recomendada:** crear `ADR-unlearner-interface.md` antes de implementar `FineTuneUnlearner`.

---

### Pendiente 8 — Otros baselines iniciales

Solo se ha fijado `finetune`. No se ha decidido si añadir:

- gradient ascent sobre forget;
- retain fine-tuning + gradient ascent;
- NegGrad;
- random labels sobre forget.

**Tarea recomendada:** dejar fuera del MVP. Reabrir después de validar `finetune`.

---

## 5.5. Optuna

### Pendiente 9 — Objetivos multiobjetivo

No se ha definido qué objetivos optimizará Optuna. Opciones posibles:

- maximizar validation accuracy;
- minimizar validation loss;
- maximizar retain accuracy;
- minimizar forget accuracy;
- minimizar distancia a `naive.pth`;
- minimizar runtime;
- combinación multiobjetivo.

**Tarea recomendada:** crear `ADR-optuna-objectives.md` antes de implementar búsqueda real.

---

### Pendiente 10 — Criterio de selección del mejor punto del Pareto front

Aunque la primera versión evaluará manualmente mediante `--trial_id`, todavía no hay una regla automática para recomendar candidatos.

**Tarea recomendada:** dejar fuera del MVP. No bloquear `step_4_select_best_hp.py`, ya que este solo debe exportar trials.

---

### Pendiente 11 — Almacenamiento persistente de Optuna

No se ha decidido si usar:

- SQLite;
- CSV;
- ambos.

**Tarea recomendada:** decidir antes de implementar `step_3_optuna_unlearning.py`.

---

## 5.6. Checkpoints

### Pendiente 12 — Criterio exacto de `best_val.pth`

No se ha decidido si `best_val.pth` se define por:

- menor validation loss;
- mayor validation accuracy;
- criterio configurable.

**Tarea recomendada:** cerrar antes de implementar `FineTuneUnlearner` de forma definitiva.

---

## 5.7. Métricas finales

### Pendiente 13 — Métricas finales obligatorias

No se ha cerrado el conjunto mínimo de métricas finales para modelos evaluados.

**Tarea recomendada:** definir un esquema mínimo para MVP y un esquema extendido para evaluación real.

---

### Pendiente 14 — Comparación final entre modelos

No se ha decidido si la evaluación final comparará siempre:

- `base.pth`;
- `naive.pth`;
- `unlearned`.

**Tarea recomendada:** cerrar antes de `step_5_evaluate_final.py` completo.

---

### Pendiente 15 — Distancia explícita al naive/oracle

No se ha decidido si medir distancia respecto a `naive.pth` usando:

- métricas agregadas;
- logits;
- probabilidades;
- KL divergence;
- representaciones internas.

**Tarea recomendada:** dejar fuera del MVP, salvo distancia agregada simple si se decide explícitamente.

---

## 5.8. MIA

### Pendiente 16 — Tipo de Membership Inference Attack inicial

No se ha decidido si implementar primero:

- loss-based MIA;
- confidence-based MIA;
- entropy-based MIA;
- las tres.

**Tarea recomendada:** posponer a fase avanzada. No usar MIA en `spiral`, debug ni Optuna.

---

## 5.9. Residual Knowledge

### Pendiente 17 — Métrica concreta de residual knowledge

No se ha decidido si priorizar:

- relearning speed;
- representation similarity;
- logit similarity;
- probe classifier.

**Tarea recomendada:** posponer a fase avanzada. Definir hipótesis científica antes de implementar.

---

## 5.10. Resultados y almacenamiento

### Pendiente 18 — Formato general de resultados

No se ha decidido si guardar resultados en:

- CSV/JSON por experimento;
- SQLite;
- ambos.

**Tarea recomendada:** para el MVP, usar JSON/CSV simples; para la versión completa, evaluar SQLite solo si aporta valor operativo.

---

### Pendiente 19 — Logs de `run_commands.py`

No se ha decidido si guardar:

- un log individual por comando;
- un log global;
- ambos;
- solo salida por terminal.

**Tarea recomendada:** cerrar antes de implementar ejecución masiva.

---

## 5.11. Figuras e informes

### Pendiente 20 — Generación automática de figuras

No se ha decidido si generar:

- gráficos básicos;
- gráficos completos;
- solo en fase final;
- ninguno inicialmente.

**Tarea recomendada:** dejar fuera del MVP.

---

### Pendiente 21 — Contenido exacto del informe global

Se ha decidido que habrá informe global `.md`, pero no su contenido exacto.

**Tarea recomendada:** cerrar después de tener tablas globales.

---

## 5.12. Configuración

### Pendiente 22 — Sistema de configuración

No se ha decidido entre:

- Hydra;
- YAML simple + argparse;
- Python config files.

**Tarea recomendada:** primera decisión arquitectónica del proyecto.

---

### Pendiente 23 — Guardado de configuración bajo `--debug`

Está decidido que se guardará la configuración efectiva final. No se ha decidido si guardar también:

- configuración original;
- bloque `debug_overrides`;
- ambas.

**Tarea recomendada:** cerrar antes de implementar modo debug.

---

## 5.13. Tests y validación

### Pendiente 24 — Tests de no solapamiento entre splits

No se ha decidido explícitamente si los tests comprobarán:

- `retain ∩ forget = ∅`;
- `retain ∩ validation = ∅`;
- `forget ∩ validation = ∅`.

**Recomendación:** incluirlo desde el MVP. Es una propiedad mínima de validez experimental.

---

## 5.14. Registries

### Pendiente 25 — Ubicación de los registries

No se ha decidido si usar:

- un único archivo `registry.py`;
- un `registry.py` por módulo;
- solución híbrida.

**Tarea recomendada:** cerrar junto al diseño modular inicial.

---

## 5.15. Subsets

### Pendiente 26 — Uso de `Subset` o wrapper propio

No se ha decidido si cargar subsets mediante:

- `torch.utils.data.Subset`;
- wrapper propio;
- empezar con `Subset` y migrar si hace falta.

**Tarea recomendada:** para MVP, decidir explícitamente una solución simple. Si se elige `Subset`, documentar limitaciones.

---

## 5.16. Manifest

### Pendiente 27 — Columnas de `experiments_manifest.csv`

No se ha decidido si usar columnas:

**Mínimas:**

```text
dataset,model,forget_strategy,unlearner,seed
```

**Extendidas:**

```text
dataset,model,forget_strategy,forget_config,unlearner,seed,debug,device
```

**Completas:**

```text
experiment_id,dataset,model,forget_strategy,forget_config,unlearner,seed,config_path,split_path,device,debug,status
```

**Tarea recomendada:** usar columnas mínimas o extendidas en el MVP; reservar columnas completas para ejecución masiva.
