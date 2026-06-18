from .dominio import Pedido
from .puertos import NotificacionHttpPuerto, PedidoRepositoryPuerto


class CasoUsoCrearPedido:
    """Orquestador de aplicación.

    Depende de los puertos mediante inversión de dependencias.
    """

    def __init__(
        self,
        repo: PedidoRepositoryPuerto,
        notificador: NotificacionHttpPuerto,
    ) -> None:
        self.repo = repo
        self.notificador = notificador

    def ejecutar(self, pedido_id: int, producto: str, monto: float) -> str:
        # 1. Instanciamos el modelo del dominio
        nuevo_pedido = Pedido(pedido_id, producto, monto)

        if not nuevo_pedido.validar_monto_valido():
            raise ValueError("El monto del pedido es inválido para el dominio.")

        # 2. Persistimos usando el puerto
        self.repo.guardar(nuevo_pedido)

        # 3. Notificamos usando el puerto de mensajería externa
        self.notificador.enviar_alerta_api(
            f"Pedido #{pedido_id} de {producto} procesado con éxito."
        )

        return f"Procesamiento exitoso del pedido {pedido_id}."
