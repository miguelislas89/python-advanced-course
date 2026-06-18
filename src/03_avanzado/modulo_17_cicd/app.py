import sys


def iniciar_servidor() -> None:
    """Simula el arranque de un microservicio de distribución en producción."""
    print("=== CONTROL DE DISTRIBUCIÓN DE FLOR DEL RÍO ===")
    print(f"🐍 Python Executable Runtime: {sys.version}")
    print("🚀 Microservicio web levantado con éxito en el puerto 8080.")
    print("================================================")


if __name__ == "__main__":
    iniciar_servidor()
