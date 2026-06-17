from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


# =====================================================================
# 1. ENTIDAD CORE DE NEGOCIO (DATACLASS CON OPERADORES DE ORDEN)
# =====================================================================
@dataclass(order=True)
class Order:
    """Entidad de negocio que representa una Orden de Compra.

    Configurada con order=True para habilitar ordenamiento nativo.
    """

    # Primer atributo declarado = Criterio principal de ordenamiento (.sort())
    total_costo: float = field(init=False)

    # Excluimos los demás campos de la comparación para que no interfieran
    order_id: int = field(compare=False)
    product_name: str = field(compare=False)
    price: float = field(compare=False)
    quantity: int = field(compare=False)

    def __post_init__(self) -> None:
        """Cálculo derivado automático posterior a la instanciación."""
        self.total_costo = round(self.price * self.quantity, 2)


# =====================================================================
# 2. MODELOS DE FRONTERA Y VALIDACIÓN (PYDANTIC V2)
# =====================================================================
class OrderIn(BaseModel):
    """Modelo encargado de auditar estrictamente los datos de entrada."""

    product_name: str = Field(min_length=3, max_length=50)
    price: PositiveFloat  # Valida que sea flotante y > 0
    quantity: PositiveInt  # Valida que sea entero y >= 1


class OrderOut(BaseModel):
    """Modelo encargado de estructurar los datos finales de salida."""

    order_id: int
    product_name: str
    quantity: int
    total_costo: float
    fecha_procesamiento: datetime


# =====================================================================
# 3. PIPELINE DE CONVERSIÓN (DATA TRANSFORMATION)
# =====================================================================
def transformar_y_validar_pedido(id_interno: int, payload: Dict[str, Any]) -> Order:
    """Valida los datos crudos con Pydantic y los convierte en una

    entidad segura DataClass 'Order'.
    """
    # Si los datos no cumplen el contrato, Pydantic levanta una excepción aquí
    datos_validados = OrderIn(**payload)

    # Mapeo y retorno hacia la entidad core de la aplicación
    return Order(
        order_id=id_interno,
        product_name=datos_validados.product_name,
        price=datos_validados.price,
        quantity=datos_validados.quantity,
    )


# =====================================================================
# EJECUCIÓN DEL ENTORNO DE PRUEBAS
# =====================================================================
if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 4 ===")

    # 1. Simulación de Payloads JSON entrantes desde el exterior
    payload_shampoo = {
        "product_name": "Shampoo de Mango 500ml",
        "price": 180.00,
        "quantity": 5,
    }
    payload_rosas = {
        "product_name": "Agua de Rosas 500ml",
        "price": 150.00,
        "quantity": 2,
    }
    payload_carbon = {
        "product_name": "Jabón de Carbón Activado",
        "price": 85.00,
        "quantity": 12,
    }

    # 2. Procesamiento a través de la tubería de validación y conversión
    orden_1 = transformar_y_validar_pedido(1001, payload_shampoo)
    orden_2 = transformar_y_validar_pedido(1002, payload_rosas)
    orden_3 = transformar_y_validar_pedido(1003, payload_carbon)

    # 3. Demostración de Comparaciones y Ordenamiento de DataClasses
    lista_ordenes: List[Order] = [orden_1, orden_2, orden_3]

    print("\n📦 Estado original del inventario de pedidos:")
    for o in lista_ordenes:
        print(f"   - ID: {o.order_id} | {o.product_name} | Total: ${o.total_costo}")

    # Ejecutamos el ordenamiento nativo potenciado por order=True (Menor a Mayor)
    lista_ordenes.sort()

    print("\n📈 Pedidos ordenados automáticamente por impacto financiero:")
    for o in lista_ordenes:
        print(f"   - ID: {o.order_id} | {o.product_name} | Total: ${o.total_costo}")

    # 4. Formateo y Generación del Esquema de Salida Comercial (OrderOut)
    print("\n✨ Transformando entidad a esquema de salida Pydantic (OrderOut):")
    reporte_cliente = OrderOut(
        order_id=orden_1.order_id,
        product_name=orden_1.product_name,
        quantity=orden_1.quantity,
        total_costo=orden_1.total_costo,
        fecha_procesamiento=datetime.now(),
    )
    print(reporte_cliente.model_dump_json(indent=2))

    # 5. Prueba de Robustez: Envío intencional de datos corruptos
    print("\n🛡️ Evaluando resistencia perimetral con datos inválidos...")
    try:
        payload_corrupto = {
            "product_name": "X",  # Falla: Menos de 3 caracteres
            "price": -45.00,  # Falla: No es positivo
            "quantity": 0,  # Falla: Debe ser al menos 1
        }
        transformar_y_validar_pedido(1004, payload_corrupto)
    except Exception as error_pydantic:
        print("❌ Pydantic interceptó el fraude exitosamente:")
        print(error_pydantic)

    print("====================================")
