from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    api_host: str = Field(default="0.0.0.0", alias="RECALLOPS_API_HOST")
    api_port: int = Field(default=8000, alias="RECALLOPS_API_PORT")
    postgres_dsn: str = Field(
        default="postgresql://recallops:recallops@localhost:5432/recallops",
        alias="POSTGRES_DSN",
    )
    qdrant_url: str = Field(default="http://localhost:6333", alias="QDRANT_URL")
    default_collection: str = Field(default="research_ops", alias="DEFAULT_COLLECTION")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL"
    )
    vector_size: int = Field(default=384, alias="VECTOR_SIZE")
    chunk_size: int = Field(default=700, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=120, alias="CHUNK_OVERLAP")
    search_top_k: int = Field(default=5, alias="SEARCH_TOP_K")
    search_ef: int = Field(default=64, alias="SEARCH_EF")


@lru_cache
def get_settings() -> Settings:
    return Settings()
