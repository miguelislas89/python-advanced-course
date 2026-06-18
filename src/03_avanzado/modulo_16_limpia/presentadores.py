from .dominio import PedidoAvanzado


class PresentadorPedidoJson:
    """Transforma las entidades de dominio en contratos de salida específicos."""

    @staticmethod
    def formatear_respuesta_cliente(pedido: PedidoAvanzado) -> dict:
        """Genera un diccionario limpio listo para ser serializado por una API."""
        return {
            "estatus": "exito",
            "codigo_respuesta": 201,
            "data": {
                "identificador_orden": f"FDR-{pedido.pedido_id}",
                "item_solicitado": pedido.producto,
                "volumen": pedido.cantidad,
            },
        }
