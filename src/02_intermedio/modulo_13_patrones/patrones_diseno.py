from typing import Any, Callable, Dict


# =====================================================================
# 1. PATRÓN IDIOMÁTICO: DECORATOR DE CACHÉ
# =====================================================================
def cache_calculo(funcion: Callable[..., float]) -> Callable[..., float]:
    """Decorador personalizado para almacenar en caché los resultados

    de los cálculos financieros de Flor del Río.
    """
    memoria_cache: Dict[str, float] = {}

    def envoltura(*args: Any) -> float:
        # Generamos una llave única basada en los argumentos de la función
        llave = str(args)
        if llave not in memoria_cache:
            print(f"📊 [CACHÉ] Miss para {llave}. Calculando en tiempo real...")
            memoria_cache[llave] = funcion(*args)
        else:
            print(f"🚀 [CACHÉ] Hit para {llave}. Recuperando de RAM...")
        return memoria_cache[llave]

    return envoltura


# =====================================================================
# 2. PATRÓN COMPORTAMIENTO: STRATEGY PARA PRECIOS
# =====================================================================
class EstrategiaPrecioLocal:
    """Calcula el costo del producto sin modificaciones de divisa."""

    def calcular(self, costo_base: float) -> float:
        return round(costo_base, 2)


class EstrategiaPrecioExportacion:
    """Aplica una tasa de cambio de divisa y un arancel de aduana."""

    def __init__(self, tipo_cambio: float, arancel: float) -> None:
        self.tipo_cambio = tipo_cambio
        self.arancel = arancel

    def calcular(self, costo_base: float) -> float:
        costo_convertido = costo_base * self.tipo_cambio
        return round(costo_convertido + self.arancel, 2)


class CalculadoraPreciosContexto:
    """Contexto del patrón Strategy que coordina la ejecución."""

    def __init__(self, estrategia: Any) -> None:
        self._estrategia = estrategia

    @cache_calculo
    def procesar_precio_final(self, costo_base: float) -> float:
        return self._estrategia.calcular(costo_base)


# =====================================================================
# 3. PATRÓN ESTRUCTURAL: ADAPTER PARA PROVEEDOR EXTERNO
# =====================================================================
class ProveedorPagoExternoAPI:
    """Simula una API externa que devuelve datos estructurados de forma

    incompatible (usa llaves raras como 'monto_raw' y 'id_transaccion').
    """

    def ejecutar_cobro(self) -> dict:
        return {"id_transaccion": "TX-9982", "monto_raw": 180.0}


class AdaptadorPagoInterno:
    """Adapta la respuesta del proveedor externo a la interfaz limpia

    esperada por nuestro sistema Core de Flor del Río.
    """

    def __init__(self, servicio_externo: ProveedorPagoExternoAPI) -> None:
        self._servicio = servicio_externo

    def procesar_pago_estandar(self) -> dict:
        datos_externos = self._servicio.ejecutar_cobro()
        # Mapeamos a las llaves que nuestro sistema sí entiende
        return {
            "transaccion_id": datos_externos["id_transaccion"],
            "total_neto": datos_externos["monto_raw"],
            "estado": "CONFIRMADO",
        }


# =====================================================================
# 4. PIPELINE DE EJECUCIÓN DEL LABORATORIO
# =====================================================================
if __name__ == "__main__":
    print("=== INICIO LABORATORIO MÓDULO 13 (PATRONES DE DISEÑO) ===")

    # --- 1. Probando Strategy + Decorator de Caché ---
    print("\n📦 Configurando Estrategia Local con un Shampoo de Mango ($180.00)...")
    calculadora_local = CalculadoraPreciosContexto(EstrategiaPrecioLocal())

    # Primera llamada: Debe calcularse
    precio_1 = calculadora_local.procesar_precio_final(180.00)
    # Segunda llamada idéntica: Debe recuperarse de la caché
    precio_2 = calculadora_local.procesar_precio_final(180.00)

    print(f"Resultado final local verificado: ${precio_2}")

    print("\n✈️ Cambiando a Estrategia de Exportación (USD)...")
    estrategia_usa = EstrategiaPrecioExportacion(tipo_cambio=0.055, arancel=2.50)
    calculadora_export = CalculadoraPreciosContexto(estrategia_usa)

    precio_export_1 = calculadora_export.procesar_precio_final(180.00)
    precio_export_2 = calculadora_export.procesar_precio_final(180.00)
    print(f"Resultado final exportación verificado: ${precio_export_2}")

    # --- 2. Probando el Adapter ---
    print("\n💳 Ejecutando cobro mediante Adaptador Estructural...")
    api_externa = ProveedorPagoExternoAPI()
    adaptador = AdaptadorPagoInterno(api_externa)

    datos_sistema_limpio = adaptador.procesar_pago_estandar()
    print("✅ Datos adaptados exitosamente para el core:")
    print(datos_sistema_limpio)
    print("====================================================")
