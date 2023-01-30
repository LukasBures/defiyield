from starlette.config import Config
from starlette.datastructures import Secret

config: Config = Config(".env")

# API related configurations
API_KEY: Secret = config("API_KEY", cast=Secret)
API_URL: str = config("API_URL", default="https://public-api.defiyield.app/graphql/")
