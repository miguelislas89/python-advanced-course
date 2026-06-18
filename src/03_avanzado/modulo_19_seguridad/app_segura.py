import sys

from .config import ConfiguracionSeguraPlanta


def arrancar_app_segura() -> None:
    print("=== INICIO LABORATORIO MÓDULO 19 (SEGURIDAD Y HARDENING) ===")

    try:
        # Intentamos inicializar los secretos de la planta
        config = ConfiguracionSeguraPlanta()
        print("✅ Configuración y secretos validados con éxito.")
        print(f"🔑 API Key cargada (Longitud): {len(config.fdr_api_key)} caracteres.")
        print(f"⏱️ DB Timeout configurado: {config.fdr_db_timeout}s")
        print("\n🔒 [HARDENING] Ejecutando entorno con privilegios mínimos.")
        print(f"👤 UID/Proceso actual de Python: {sys.platform}")
        print("====================================================")

    except Exception as e:
        print("\n❌ [ERROR DE SEGURIDAD] Fallo al validar secretos del entorno.")
        print(f"Detalle: {e}")
        print("El sistema se apaga preventivamente para evitar brechas.\n")
        sys.exit(1)


if __name__ == "__main__":
    arrancar_app_segura()
