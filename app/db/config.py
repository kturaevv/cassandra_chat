from pydantic import BaseSettings, Field
from functools import lru_cache

from cassandra.cluster import Cluster
from cassandra.cluster import Session

class Settings(BaseSettings):
    keyspace: str = Field(..., env="CASSANDRA_KEYSPACE")
    address: str = Field(..., env="CASSANDRA_ADDRESS")
    port: str = Field(..., env="CASSANDRA_PORT")
    fetch_size: int = 50
    
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
