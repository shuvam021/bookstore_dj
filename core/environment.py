from pydantic import BaseSettings


class EnvConfig(BaseSettings):
    secret_key: str
    algorithm: str
    db_user: str
    db_password: str
    db_port: int
    db_host: str
    db_name: str

    class Config:
        env_file = ".env"


env = EnvConfig()  # type: ignore
