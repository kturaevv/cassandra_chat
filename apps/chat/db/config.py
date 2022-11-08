from pydantic import BaseSettings, Field
from functools import lru_cache

from cassandra.cluster import Cluster
from cassandra.cluster import Session

class Settings(BaseSettings):
    keyspace: str = Field(..., env="KEYSPACE")
    address: str = Field(..., env="ADDRESS")

    cluster: Cluster | None = None
    session: Session | None = None

    fetch_size: int = 25
    
    class Config:
        env_file = '.env'

@lru_cache()
def get_settings():
    return Settings()


if __name__ == "__main__":
    print("Checking settings...")
    settings = get_settings()
    for variable in settings: 
        print(*variable, sep=' : ')
