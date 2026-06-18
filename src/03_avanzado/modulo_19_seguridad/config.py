from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfiguracionSeguraPlanta(BaseSettings):
    """Mapea y valida secretos del entorno para Flor del Río.

    Realiza validación de tipos automática en el arranque.
    """

    # Secretos obligatorios que el sistema exigirá validar
    fdr_api_key: str
    fdr_db_timeout: int = 30  # Valor por defecto seguro

    # Configuración de lectura para el archivo .env
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
