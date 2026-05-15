# ADR 0002: Ubicación e Implementación de los Registries

## Contexto
El framework necesita instanciar dinámicamente datasets, modelos y unlearners basándose en strings del `config.yaml`.

## Alternativas consideradas
1. **Un único `registry.py` global:** Concentra todos los decoradores de registro en un solo lugar.
2. **Un registry por submódulo:** e.g., `datasets/registry.py`, `models/registry.py`.

## Decisión
Usaremos **un único archivo `registry.py`** en la raíz de `unlearning_benchmark`. Esto simplifica la importación para los módulos (solo tienen que importar `@register_model`, `@register_dataset`, etc., de un solo lugar) y para el evaluador.

## Consecuencias
- Interfaz clara: `get_model("name")`, `get_dataset("name")`.
- Fácil de testear.
