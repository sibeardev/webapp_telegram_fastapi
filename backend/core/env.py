from functools import cached_property

from pydantic import AnyHttpUrl, BaseModel, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseModel):
    TOKEN: str
    ADMINS: list[int]
    SECRET: str


class RabbitMQSettings(BaseModel):
    URL: str


class EnvSettings(BaseSettings):
    MONGO_DSN: MongoDsn
    RABBITMQ: RabbitMQSettings
    TELEGRAM: TelegramSettings
    EXTERNAL_URL: AnyHttpUrl
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    DEBUG: bool = True
    PROJECT_NAME: str = "fridrik"
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        validate_default=True,
        ignored_types=(cached_property,),
        extra="allow",
        use_attribute_docstrings=True,
    )
