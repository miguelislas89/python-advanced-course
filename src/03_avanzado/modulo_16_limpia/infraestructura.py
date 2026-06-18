from typing import Any

from .aplicacion import CasoUsoCrearPedidoAvanzado
from .dominio import EventoPedidoCreado
from .presentadores import PresentadorPedidoJson


# =====================================================================
# ADAPTADOR DE INFRAESTRUCTURA: UNIT OF WORK EN MEMORIA
# =====================================================================
class UnitOfWorkMemoria:
    """Implementación de infraestructura para simular transaccionalidad."""

    def __init__(self) -> None:
        self.committed = False

    def __enter__(self) -> Any:
        self.committed = False
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self.committed = True

    def rollback(self) -> None:
        self.committed = False


# =====================================================================
# MANEJADOR DE EVENTOS DE APLICACIÓN
# =====================================================================
# =====================================================================
# MANEJADOR DE EVENTOS DE APLICACIÓN
# =====================================================================
def manejador_evento_pedido_creado(evento: EventoPedidoCreado) -> None:
    """Reacciona al evento de dominio de forma totalmente desacoplada."""
    # 🌟 CORRECCIÓN: Separamos el mensaje en dos líneas para cumplir con E501
    msg = (
        f"📢 [EVENTO MANEJADO] Alerta: Pedido #{evento.pedido_id} "
        f"de '{evento.producto}' creado."
    )
    print(msg)


# =====================================================================
# ORQUESTADOR PRINCIPAL DEL PIPELINE
# =====================================================================
def iniciar_pipeline_limpio() -> None:
    print("=== INICIO LABORATORIO MÓDULO 16 (ARQUITECTURA LIMPIA) ===")

    # 1. Instanciamos la infraestructura transaccional
    infra_uow = UnitOfWorkMemoria()

    # 2. Inicializamos el caso de uso inyectando la Unidad de Trabajo
    caso_uso = CasoUsoCrearPedidoAvanzado(uow=infra_uow)

    # 3. Ejecutamos la lógica de negocio pura
    pedido_entidad = caso_uso.ejecutar(
        pedido_id=500, producto="Shampoo de Mango 500ml", cantidad=10
    )

    # 4. El caso de uso termina y la aplicación despacha los eventos del dominio
    for evento_dominio in pedido_entidad.eventos:
        manejador_evento_pedido_creado(evento_dominio)

    # 5. Pasamos la entidad por el Presenter para empaquetar la salida final
    json_salida = PresentadorPedidoJson.formatear_respuesta_cliente(pedido_entidad)
    print(f"\n✨ Salida formateada por el Presenter:\n{json_salida}")
    print("====================================================")


if __name__ == "__main__":
    iniciar_pipeline_limpio()
