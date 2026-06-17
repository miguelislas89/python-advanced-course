import logging
from pathlib import Path

import httpx

# =====================================================================
# CONFIGURACIÓN DE BITÁCORA (LOGGING)
# =====================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


def descargar_catalogo_streaming(url_objetivo: str, nombre_salida: str) -> bool:
    """Cliente HTTP robusto utilizando HTTPX que implementa timeouts,

    descarga por streaming fragmentada y guardado directo en disco.
    """
    ruta_destino = Path(__file__).parent / nombre_salida

    # 1. Configuración de límites y resiliencia (Timeout estricto de 10s)
    limites_tiempo = httpx.Timeout(10.0, connect=5.0)

    logging.info(f"🌐 Conectando al endpoint de datos: {url_objetivo}")

    try:
        # 2. Uso del Cliente HTTPX con soporte HTTP/2 habilitado
        with httpx.Client(timeout=limites_tiempo, http2=True) as cliente:
            # 3. Abrimos la conexión en modo STREAM para no saturar la RAM
            with cliente.stream("GET", url_objetivo) as respuesta:
                # Si el servidor responde con un código de error (4xx, 5xx), truena aquí
                respuesta.raise_for_status()

                logging.info(
                    f"📥 Conexión establecida (Código: {respuesta.status_code}). "
                    f"Iniciando descarga por streaming a disco..."
                )

                # 4. Iteración por fragmentos (Chunks de 4 Kilobytes)
                with open(ruta_destino, mode="wb") as archivo_disco:
                    for fragmento in respuesta.iter_bytes(chunk_size=4096):
                        if fragmento:
                            archivo_disco.write(fragmento)

        logging.info(f"🎉 Descarga exitosa. Archivo preservado en: {ruta_destino.name}")
        return True

    # Manejo de errores granular para tuberías de datos de producción
    except httpx.TimeoutException:
        logging.error(
            "🚨 [FALLO] El servidor externo agotó el tiempo de espera (Timeout)."
        )
        return False
    except httpx.HTTPStatusError as error_status:
        logging.error(
            f"🚨 [FALLO] Error de respuesta HTTP del servidor: {error_status}"
        )
        return False
    except Exception as error_general:
        logging.error(
            f"🚨 [FALLO] Error inesperado en el pipeline HTTP: {error_general}"
        )
        return False


# =====================================================================
# EJECUCIÓN DEL ENTORNO DE PRUEBAS
# =====================================================================
if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 7 (HTTP & STREAMING) ===")

    # Usaremos una URL pública y segura que simula una respuesta JSON masiva
    URL_API_PRODUCCIÓN = "https://jsonplaceholder.typicode.com/photos"
    ARCHIVO_REPORTE = "catalogo_productos_raw.json"

    exito = descargar_catalogo_streaming(URL_API_PRODUCCIÓN, ARCHIVO_REPORTE)

    if exito:
        print("\n📊 Validación: Revisa la nueva carpeta del módulo 7.")
        print(
            f"El archivo '{ARCHIVO_REPORTE}' se descargó consumiendo un mínimo de RAM."
        )
    else:
        print("\n❌ El proceso falló. Revisa los logs de auditoría arriba.")

    print("======================================================")
