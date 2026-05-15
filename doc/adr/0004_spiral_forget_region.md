# ADR 0004: Región de Forget para el Dataset Spiral

## Contexto
Para el desarrollo y pruebas rápidas (modo debug), necesitamos un dataset sintético (`spiral`). Debemos definir qué porción de este dataset representará el "forget set" de forma predeterminada, para que no requiera configuración manual en cada ejecución.

## Alternativas consideradas
1. **Olvido aleatorio:** Seleccionar un porcentaje aleatorio de muestras. No representa bien el machine unlearning estructurado.
2. **Olvido de una clase entera:** Eliminar completamente la clase 0. Demasiado simple para evaluar métodos que no operan a nivel de clase.
3. **Olvido angular (partial class):** Eliminar muestras de una clase dentro de un rango específico del ángulo $\theta$ en coordenadas polares.

## Decisión
Usaremos **olvido angular (partial class)**.
Por defecto, el forget set estará compuesto por las muestras de la **clase 0** cuyo ángulo original de generación $\theta$ esté en el rango **$[2\pi, 3\pi]$**.

## Consecuencias
- El forget set no es vacío y representa una porción continua y no trivial de la distribución subyacente.
- Permite evaluar si los métodos de unlearning generalizan espacialmente o solo olvidan datos exactos.
- La clase `SpiralDataset` debe guardar el atributo `theta` internamente para que `step_1_generate_splits.py` pueda identificar la región a olvidar.
