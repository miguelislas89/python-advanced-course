import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx


# =====================================================================
# 1. TAREA CPU-BOUND: SIMULACIÓN DE CÁLCULO FINANCIERO PESADO
# =====================================================================
def calculo_pesado_cpu(id_lote: int) -> int:
    """Función pura que satura la CPU calculando una sumatoria masiva.

    Debe ejecutarse en un proceso aislado para evadir el GIL.
    """
    print(f"⚙️ [CPU] Iniciando cálculo matemático del lote {id_lote}...")
    contador = 0
    for i in range(15_000_000):
        contador += i
    print(f"✨ [CPU] Cálculo finalizado para el lote {id_lote}.")
    return contador


# =====================================================================
# 2. TAREA I/O-BOUND: FETCHING CONCURRENTE ASÍNCRONO
# =====================================================================
async def consultar_endpoint_asincrono(
    cliente: httpx.AsyncClient, id_post: int, semaforo: asyncio.Semaphore
) -> dict:
    """Consulta una API de forma asíncrona controlando la concurrencia

    mediante un semáforo de protección.
    """
    url = f"https://jsonplaceholder.typicode.com/posts/{id_post}"

    async with semaforo:  # Solo permite que entren 'N' hilos concurrentes aquí
        respuesta = await cliente.get(url, timeout=5.0)
        return respuesta.json()


async def pipeline_io_asincrono(urls_a_consultar: list) -> list:
    """Coordina el ciclo de eventos para descargar todas las peticiones

    de forma masiva y simultánea.
    """
    # El semáforo restringe a un máximo de 3 peticiones simultáneas activas
    limite_concurrencia = asyncio.Semaphore(3)

    async with httpx.AsyncClient(http2=True) as cliente:
        tareas = [
            consultar_endpoint_asincrono(cliente, i, limite_concurrencia)
            for i in urls_a_consultar
        ]
        # Ejecuta la lista completa de corrutinas en paralelo
        resultados = await asyncio.gather(*tareas)
        return resultados


# =====================================================================
# 3. PIPELINE DE CONTROL Y MEDICIÓN DE RENDIMIENTO
# =====================================================================
def ejecutar_laboratorio():
    print("=== INICIO LABORATORIO MÓDULO 11 (CONCURRENCIA) ===")
    ids_inventarios = [1, 2, 3, 4, 5]

    # --- FASE 1: Medición de I/O Asíncrono masivo ---
    print("\n🌐 Iniciando descargas asíncronas concurrentes (I/O)...")
    inicio_io = time.perf_counter()

    # Lanzamos el bucle de eventos nativo de asyncio
    resultados_api = asyncio.run(pipeline_io_asincrono(ids_inventarios))

    fin_io = time.perf_counter()
    print(f"✅ Descargados {len(resultados_api)} reportes de inventario.")
    print(f"⏱️ Tiempo total de descarga I/O: {fin_io - inicio_io:.4f} segundos")

    # --- FASE 2: Medición de CPU-Bound con Multiprocesamiento ---
    print("\n🚀 Iniciando procesamiento paralelo en núcleos de CPU...")
    inicio_cpu = time.perf_counter()

    # Levantamos un pool de procesos independientes basado en los cores del sistema
    with ProcessPoolExecutor() as ejecutor_procesos:
        # Reparte las ejecuciones de la función pesada entre los cores físicos
        resultados_calculo = list(ejecutor_procesos.map(calculo_pesado_cpu, [1, 2, 3]))

    fin_cpu = time.perf_counter()
    print(f"📊 Resultados financieros consolidados: {len(resultados_calculo)}")
    print(f"⏱️ Tiempo total del procesamiento CPU: {fin_cpu - inicio_cpu:.4f} segundos")
    print("====================================================")


if __name__ == "__main__":
    ejecutar_laboratorio()
