from dataclasses import dataclass


@dataclass
class Pedido:
    """Entrada pura de Dominio. No conoce frameworks ni bases de datos."""

    pedido_id: int
    producto: str
    monto: float

    def validar_monto_valido(self) -> bool:
        return self.monto > 0
