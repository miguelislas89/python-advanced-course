from typing import List, Protocol

from .dominio import Pedido


class PedidoRepositoryPuerto(Protocol):
    """Puerto de salida que define las reglas para persistir pedidos."""

    def guardar(self, pedido: Pedido) -> None: ...

    def obtener_todos(self) -> List[Pedido]: ...


class NotificacionHttpPuerto(Protocol):
    """Puerto de salida que define cómo se envían las alertas externas."""

    def enviar_alerta_api(self, mensaje: str) -> bool: ...
