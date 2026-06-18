from typing import Any, Protocol

from .dominio import PedidoAvanzado


class UnitOfWorkPuerto(Protocol):
    """Protocolo que define el comportamiento atómico de una transacción."""

    def __enter__(self) -> Any: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class CasoUsoCrearPedidoAvanzado:
    """Caso de uso de Arquitectura Limpia que orquesta transacciones y eventos."""

    def __init__(self, uow: UnitOfWorkPuerto) -> None:
        self.uow = uow

    def ejecutar(self, pedido_id: int, producto: str, cantidad: int) -> PedidoAvanzado:
        # Ejecutamos toda la lógica bajo el resguardo de la Unidad de Trabajo (UoW)
        with self.uow:
            pedido = PedidoAvanzado(
                pedido_id=pedido_id, producto=producto, cantidad=cantidad
            )
            pedido.registrar_creacion()

            # Confirmamos la transacción atómica
            self.uow.commit()
            return pedido
