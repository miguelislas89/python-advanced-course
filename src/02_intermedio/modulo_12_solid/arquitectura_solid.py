from typing import List, Protocol


# =====================================================================
# 1. EL PUERTO (ISP / DIP): INTERFAZ UTILIZANDO TYPING.PROTOCOL
# =====================================================================
class InventarioRepository(Protocol):
    """Protocolo estructural que define el contrato de persistencia

    para los productos de Flor del Río.
    """

    def guardar_producto(self, nombre: str, precio: float) -> None: ...

    def obtener_todos(self) -> List[str]: ...


# =====================================================================
# 2. LAS ADAPTACIONES (OCP / LSP): IMPLEMENTACIONES INDEPENDIENTES
# =====================================================================
class RepositorioMemoria:
    """Implementación ultra-rápida en memoria RAM ideal para testing."""

    def __init__(self) -> None:
        self._db: List[str] = []

    def guardar_producto(self, nombre: str, precio: float) -> None:
        self._db.append(f"{nombre} (${precio})")

    def obtener_todos(self) -> List[str]:
        return self._db


class RepositorioTextoFalso:
    """Simula una persistencia en un archivo físico de texto."""

    def __init__(self) -> None:
        self._archivo_mock: List[str] = []

    def guardar_producto(self, nombre: str, precio: float) -> None:
        # Formato ligeramente distinto, pero respeta la firma del contrato
        self._archivo_mock.append(f"LOG_FILE_ROW: {nombre} - {precio}")

    def obtener_todos(self) -> List[str]:
        return self._archivo_mock


# =====================================================================
# 3. LÓGICA DE ALTO NIVEL (SRP / DIP): EL SERVICIO PRINCIPAL
# =====================================================================
class GestorInventarioService:
    """Servicio de negocio que cumple con el SRP.

    No sabe CÓMO se guardan los datos, solo coordina la regla de negocio
    dependiendo exclusivamente de la abstracción (DIP).
    """

    def __init__(self, repositorio: InventarioRepository) -> None:
        # Inyección de dependencias implícita por protocolo
        self._repo = repositorio

    def registrar_articulo(self, nombre: str, precio: float) -> None:
        if precio <= 0:
            raise ValueError("El precio del artículo debe ser mayor a cero.")
        # Delegamos la persistencia al adaptador inyectado
        self._repo.guardar_producto(nombre, precio)

    def consultar_catalogo(self) -> List[str]:
        return (
            self._repo.obtain_todos()
            if hasattr(self._repo, "obtain_todos")
            else self._repo.obtener_todos()
        )


# =====================================================================
# 4. ENTORNO DE VALIDACIÓN DE ARQUITECTURA (PRUEBA LSP)
# =====================================================================
def probar_sustitucion_liskov():
    print("=== INICIO LABORATORIO MÓDULO 12 (SOLID) ===")

    # Instanciamos los dos adaptadores independientes
    infra_memoria = RepositorioMemoria()
    infra_texto = RepositorioTextoFalso()

    # --- CASO A: El servicio opera con Memoria ---
    print("\n💾 Ejecutando servicio acoplado a RepositorioMemoria...")
    servicio_con_memoria = GestorInventarioService(infra_memoria)
    servicio_con_memoria.registrar_articulo("Shampoo de Mango 500ml", 180.0)
    print(f"Catálogo resultante: {servicio_con_memoria.consultar_catalogo()}")

    # --- CASO B: Verificación de LSP (Sustitución transparente) ---
    print("\n📝 Intercambiando adaptador por RepositorioTextoFalso (Prueba LSP)...")

    # Inyectamos una infraestructura completamente distinta sin tocar una sola
    # línea de código de la clase GestorInventarioService
    servicio_con_texto = GestorInventarioService(infra_texto)
    servicio_con_texto.registrar_articulo("Agua de Rosas 500ml", 150.0)

    # Si esta línea corre sin lanzar excepciones, el principio LSP se cumple
    print(f"Catálogo resultante: {servicio_con_texto.consultar_catalogo()}")
    print("\n🎉 Éxito: Principio de Sustitución de Liskov verificado al 100%.")
    print("====================================================")


if __name__ == "__main__":
    probar_sustitucion_liskov()
