"""Constants used across api endpoints"""

from fastapi.templating import Jinja2Templates

API_ROOT_PATH = "/api"
API_V1_PREFIX = f"{API_ROOT_PATH}/v1"
API_LATEST_PREFIX = f"{API_ROOT_PATH}/latest"

LATEST_API_PREFIXES = [API_V1_PREFIX]

templates = Jinja2Templates(directory="frontend/templates")
