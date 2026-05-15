# ADR 0001: Sistema de Configuración

## Contexto
Necesitamos un sistema de configuración para los experimentos de unlearning. Se requiere reproducibilidad, facilidad de uso y la posibilidad de sobrescribir valores desde la línea de comandos de forma sencilla, además de poder guardar la "configuración efectiva" para auditoría de cada experimento.

## Alternativas consideradas
1. **Hydra:** Muy potente, pero introduce una dependencia pesada y a veces demasiada magia.
2. **Archivos Python puros:** Difíciles de modificar dinámicamente desde CLI.
3. **YAML simple + diccionarios:** Usar `PyYAML` (ya en dependencias).

## Decisión
Usaremos **YAML simple + diccionarios de Python**. 
Se cargará un archivo base `config.yaml`. La configuración efectiva final se guardará en la carpeta de salida del experimento.

## Consecuencias
- Mantenemos las dependencias mínimas (`pyyaml`).
- El código de `config.py` validará las claves requeridas (ej. `dataset`, `model`, `seed`).
