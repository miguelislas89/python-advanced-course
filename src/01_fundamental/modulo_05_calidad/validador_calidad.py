from dataclasses import dataclass, field
from typing import List, Literal, Protocol, TypedDict

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt

# =====================================================================
# 1. TYPING AVANZADO: RESTRICCIONES Y CONTRATOS (PEP 484)
# =====================================================================
# Restringimos los estados del negocio a opciones fijas con Literal
EstadoRegistro = Literal["ACTIVO", "SUSPENDIDO", "PROCESADO"]


class InsumoDict(TypedDict):
    """Contrato estático que describe la estructura que debe tener

    un diccionario de insumos médicos o artesanales.
    """

    product_name: str
    price: float
    quantity: int


# =====================================================================
# 2. PROTOCOL (TIPADO ESTRUCTURAL / DUCK TYPING ESTÁTICO)
# =====================================================================
class Evaluables(Protocol):
    """Protocolo que exige que cualquier clase que lo implemente

    tenga una propiedad o atributo llamado 'total_costo'.
    """

    total_costo: float


# =====================================================================
# 3. ENTIDAD CORE DE NEGOCIO (DATACLASS)
# =====================================================================
@dataclass(order=True)
class ItemInsumo:
    """Entidad core anotada y auditable estáticamente."""

    total_costo: float = field(init=False)
    item_id: int = field(compare=False)
    product_name: str = field(compare=False)
    price: float = field(compare=False)
    quantity: int = field(compare=False)
    status: EstadoRegistro = field(default="ACTIVO", compare=False)

    def __post_init__(self) -> None:
        """Cálculo financiero derivado post-instanciación."""
        self.total_costo = round(self.price * self.quantity, 2)


# =====================================================================
# 4. MODELOS DE VALIDACIÓN PERIMETRAL (PYDANTIC V2)
# =====================================================================
class InsumoIn(BaseModel):
    """Modelo encargado de la validación en tiempo de ejecución (Runtime)."""

    product_name: str = Field(min_length=3, max_length=50)
    price: PositiveFloat
    quantity: PositiveInt


# =====================================================================
# 5. PIPELINE DE CONVERSIÓN Y AUDITORÍA ESTÁTICA
# =====================================================================
def procesar_alta_insumo(id_sistema: int, payload: InsumoDict) -> ItemInsumo:
    """Recibe un TypedDict, lo audita con Pydantic y devuelve

    una entidad pura ItemInsumo.
    """
    # Validación perimetral
    datos_limpios = InsumoIn(**payload)

    # Construcción de la entidad mapeada
    return ItemInsumo(
        item_id=id_sistema,
        product_name=datos_limpios.product_name,
        price=datos_limpios.price,
        quantity=datos_limpios.quantity,
        status="PROCESADO",
    )


def calcular_impacto_total(elementos: List[Evaluables]) -> float:
    """Función polimórfica basada en un Protocolo. Suma los costos totales

    de cualquier objeto que cumpla con la estructura 'Evaluables'.
    """
    return sum(item.total_costo for item in elementos)


if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 5 (NUEVA CARPETA) ===")

    # Payload que cumple perfectamente con el contrato estático de InsumoDict
    datos_lote: InsumoDict = {
        "product_name": "Shampoo de Mango 500ml",
        "price": 180.50,
        "quantity": 4,
    }

    # Procesamos la información a través del pipeline seguro
    insumo_final = procesar_alta_insumo(5001, datos_lote)
    print(f"📦 Entidad validada y tipada con éxito: {insumo_final}")

    # Demostración del Protocolo
    lista_auditoria: List[Evaluables] = [insumo_final]
    gran_total = calcular_impacto_total(lista_auditoria)
    print(f"💰 Impacto financiero calculado vía Protocolo: ${gran_total:.2f}")

    print("====================================================")
