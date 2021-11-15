from pydantic import BaseSettings


class Settings(BaseSettings):
    API_TOKEN: str = ""
    MONGO_DB: str = ""
    MONGO_HOST: str = ""
    MONGO_PORT: int = 0

    @classmethod
    @property
    def api_token(cls) -> str:
        return cls().API_TOKEN

    @classmethod
    @property
    def mongo_config(cls) -> tuple[str, str, int]:
        instance = cls()
        return instance.MONGO_DB, instance.MONGO_HOST, instance.MONGO_PORT
