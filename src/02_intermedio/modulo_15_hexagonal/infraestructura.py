from typing import List

from .aplicacion import CasoUsoCrearPedido
from .dominio import Pedido


# =====================================================================
# ADAPTADORES COMPATIBLES CON LOS PUERTOS
# =====================================================================
class AdaptadorRepositorioMemoria:
    """Adaptador de infraestructura que implementa almacenamiento en RAM."""

    def __init__(self) -> None:
        self._almacen: List[Pedido] = []

    def guardar(self, pedido: Pedido) -> None:
        self._almacen.append(pedido)

    def obtener_todos(self) -> List[Pedido]:
        return self._almacen


class AdaptadorNotificacionHttpSimulado:
    """Adaptador de infraestructura que simula el envío a una API REST."""

    def enviar_alerta_api(self, mensaje: str) -> bool:
        print(f"🌐 [HTTP CLIENT] Disparando POST Webhook -> {mensaje}")
        return True


# =====================================================================
# INYECCIÓN DE DEPENDENCIAS EN TIEMPO DE EJECUCIÓN (ORQUESTACIÓN)
# =====================================================================
def iniciar_pipeline_hexagonal():
    print("=== INICIO LABORATORIO MÓDULO 15 (ARQUITECTURA HEXAGONAL) ===")

    # 1. Instanciamos la infraestructura deseada de forma aislada
    infra_repo = AdaptadorRepositorioMemoria()
    infra_http = AdaptadorNotificacionHttpSimulado()

    # 2. Cableamos la infraestructura dentro de la aplicación (Wiring)
    caso_uso = CasoUsoCrearPedido(repo=infra_repo, notificador=infra_http)

    # 3. Ejecutamos la operación simulando una petición entrante de Flor del Río
    resultado = caso_uso.ejecutar(
        pedido_id=2026, producto="Agua de Rosas 500ml", monto=150.0
    )
    print(f"📝 Respuesta del Caso de Uso: {resultado}")

    # Validamos que los datos se guardaron correctamente en la infraestructura
    pedidos_guardados = (
        infra_repo.obtain_todos()
        if hasattr(infra_repo, "obtain_todos")
        else infra_repo.obtener_todos()
    )
    print(f"📊 Total de registros en base de datos: {len(pedidos_guardados)}")
    print("====================================================")


if __name__ == "__main__":
    iniciar_pipeline_hexagonal()
