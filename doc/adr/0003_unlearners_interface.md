# ADR 0003: Interfaz de los Unlearners

## Contexto
Diferentes estrategias de unlearning (FineTuning, Gradient Ascent, etc.) necesitan una API estandarizada para poder ser intercambiables durante los experimentos.

## Alternativas consideradas
1. **Pasar DataLoaders individuales a `fit`:** `fit(model, retain_loader, forget_loader, val_loader)`.
2. **Pasar un objeto contenedor/DataModule:** `fit(model, datamodule)`.

## Decisión
Usaremos una **clase abstracta `BaseUnlearner`**.
- El constructor (`__init__`) recibirá toda la configuración necesaria (`config`).
- El método principal será `fit(model, retain_loader, forget_loader, val_loader) -> None`.
- Se añadirá un método `get_best_model()` si la estrategia maneja checkpoints internos.

## Consecuencias
- La firma es explícita respecto a qué datos necesita el unlearner.
- El objeto instanciado es un callable stateful o expone métodos claros.
