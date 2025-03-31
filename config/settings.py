import os
from dotenv import load_dotenv

# 指定 .env 文件的路径
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# API 基础配置
API_HOST = os.getenv("ROXY_API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("ROXY_API_PORT", 50000))
API_TOKEN = os.getenv("ROXY_API_TOKEN", "YOUR_API_KEY_HERE")
BASE_URL = f"http://{API_HOST}:{API_PORT}"

# 工作区配置
DEFAULT_WORKSPACE_ID = int(os.getenv("ROXY_DEFAULT_WORKSPACE_ID", 1))

# API 端点配置
API_ENDPOINTS = {
    "health_check": "/health",
    "workspaces": "/browser/workspace",
    "list_profiles": "/browser/list_v2",
    "create_profile": "/browser/create",
    "modify_profile": "/browser/mdf",
    "open_profile": "/browser/open",
    "close_profile": "/browser/close",
    "random_fingerprint": "/browser/random_env",
    "delete_profile": "/browser/delete",
    "connection_info": "/browser/connection_info",
    "clear_local_cache": "/browser/clear_local_cache",
    "clear_server_cache": "/browser/clear_server_cache",
    "accounts": "/browser/account",
    "labels": "/browser/label"
}

# 默认请求头
DEFAULT_HEADERS = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

# 其他配置项
REQUEST_TIMEOUT = int(os.getenv("ROXY_REQUEST_TIMEOUT", 30))
MAX_RETRIES = int(os.getenv("ROXY_MAX_RETRIES", 3))