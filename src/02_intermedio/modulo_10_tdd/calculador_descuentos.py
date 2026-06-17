def calcular_precio_final(precio_base: float, cantidad: int) -> float:
    """Calcula el precio final aplicando reglas de descuento por volumen.

    - Menos de 10 unidades: 0%
    - 10 a 49 unidades: 10%
    - 50 o más unidades: 20%
    """
    if precio_base < 0 or cantidad < 0:
        raise ValueError("El precio base y la cantidad no pueden ser negativos.")

    if cantidad >= 50:
        descuento = 0.20
    elif cantidad >= 10:
        descuento = 0.10
    else:
        descuento = 0.0

    precio_con_descuento = precio_base * (1.0 - descuento)
    return round(precio_con_descuento * cantidad, 2)
