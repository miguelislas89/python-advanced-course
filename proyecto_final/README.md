# 📦 Servicio Core de Gestión de Órdenes - Flor del Río

Servicio Web API construido bajo la **Arquitectura Hexagonal (Puertos y Adaptadores)** y alineado de forma estricta a los **Lineamientos de Diseño Web API de Axity**[cite: 1].

---

## 📐 Arquitectura del Sistema

El proyecto separa el dominio de los detalles técnicos mediante la siguiente estructura:

* **`src/dominio`**: Entidades e inmutabilidad de negocio puro.
* **`src/aplicacion`**: Casos de uso y definición de puertos de entrada/salida.
* **`src/infraestructura`**: Adaptadores (FastAPI, Redis Simulado, Repositorios).

---

## 🚀 Cumplimiento de Lineamientos Axity API

1. **Versionamiento y URL Base**: Acceso expuesto bajo la ruta `/api/v1/orders`.
2. **Verbos HTTP Semánticos**: Uso estricto de `POST` (Creación) y `GET` (Consultas).
3. **Paginación en Consultas**: Implementación de `limit` y `offset` vía QueryString.
4. **Manejo de Errores Estandarizado**: Respuestas en formato JSON corporativo conteniendo `errorCode`, `errorMessage`, `userError` e `info`.
5. **Documentación Swagger/OpenAPI**: Exposición interactiva y viva a través de `/api/v1/docs`.

---

## 🛠️ Comandos de Ejecución Local

### 1. Iniciar la aplicación FastAPI
```powershell
poetry run uvicorn src.infraestructura.adaptadores.api_rest:app --reload --port 8000
