"""
Configuration loaded from environment variables or a .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Neo4j
    neo4j_uri: str = Field(
        default="neo4j+s://be29599c.databases.neo4j.io",
        alias="NEO4J_URI",
    )
    neo4j_user: str = Field(default="be29599c", alias="NEO4J_USER")
    neo4j_password: str = Field(
        default="Vvmm49Tbvs4_zdwXjvEA2-W_-0_Baw6sA__AgZdsL3g",
        alias="NEO4J_PASSWORD",
    )

    # Model checkpoint
    checkpoint_path: str = Field(default="final_model.pt", alias="CHECKPOINT_PATH")

    # Architecture (must match training)
    hidden_dim: int = Field(default=256, alias="HIDDEN_DIM")
    num_layers: int = Field(default=4, alias="NUM_LAYERS")
    dropout: float = Field(default=0.2, alias="DROPOUT")

    # Runtime
    device: str = Field(default="cpu", alias="DEVICE")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        populate_by_name=True,
    )