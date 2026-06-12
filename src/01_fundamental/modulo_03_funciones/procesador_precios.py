from functools import reduce
from typing import Any, Dict


def aplicar_impuestos_dinamicos(base_impositiva: float, **impuestos: float) -> float:
    """Calcula el factor multiplicador sumando todos los impuestos pasados

    dinámicamente por nombre y lo aplica a una tasa base.
    """
    total_tasas = sum(impuestos.values())
    return base_impositiva * (1.0 + total_tasas)


def ejecutar_pipeline_financiero(
    *precios_base: float, impuesto_config: Dict[str, float]
) -> Dict[str, Any]:
    """Procesa un flujo de costos aplicando programación funcional:

    transforma con map, filtra con filter y consolida el total con reduce.
    """
    print(f"📊 Recibidos {len(precios_base)} registros de costos bases.")

    # 1. Transformación (MAP): Aplicar la tasa impositiva dinámica a cada costo
    precios_con_iva = list(
        map(
            lambda precio: aplicar_impuestos_dinamicos(precio, **impuesto_config),
            precios_base,
        )
    )

    # 2. Filtrado (FILTER): Conservar costos significativos mayores a $100.00
    # Modificado a minúsculas (umbral) para cumplir con la regla PEP 8 (N806)
    umbral = 100.00
    costos_auditables = list(filter(lambda precio: precio > umbral, precios_con_iva))

    # 3. Agregación (REDUCE): Sumar todo el flujo filtrado para el total
    if costos_auditables:
        gasto_total_consolidado = reduce(lambda acc, x: acc + x, costos_auditables)
    else:
        gasto_total_consolidado = 0.0

    return {
        "conteo_original": len(precios_base),
        "conteo_filtrado": len(costos_auditables),
        "precios_finales_procesados": [round(p, 2) for p in precios_con_iva],
        "gasto_total_auditable": round(gasto_total_consolidado, 2),
    }


if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 3 ===")

    # Lote dinámico enviado como argumentos posicionales sueltos (*args)
    LOTES_COSTOS = (45.50, 120.00, 15.00, 85.00, 250.00)

    # Configuración dinámica de tasas impositivas (**kwargs internos)
    CONFIG_TAX = {"iva": 0.16, "ieps": 0.08}

    # Invocación de la tubería analítica
    reporte = ejecutar_pipeline_financiero(*LOTES_COSTOS, impuesto_config=CONFIG_TAX)

    import json

    print(
        f"📝 Reporte Consolidado Final:\n"
        f"{json.dumps(reporte, indent=2, ensure_ascii=False)}"
    )
    print("===================================")
