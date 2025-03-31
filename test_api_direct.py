import requests
import os
from dotenv import load_dotenv

# 加载.env文件
env_path = os.path.join(os.path.dirname(__file__), 'config', '.env')
load_dotenv(env_path)

# 获取配置
API_HOST = os.getenv("ROXY_API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("ROXY_API_PORT", 50000))
API_TOKEN = os.getenv("ROXY_API_TOKEN")
BASE_URL = f"http://{API_HOST}:{API_PORT}"

# 设置请求头
headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

def test_health_check():
    """测试健康检查接口"""
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url, headers=headers)
        print(f"健康检查接口状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"健康检查请求失败: {str(e)}")

def test_workspaces():
    """测试工作区列表接口"""
    url = f"{BASE_URL}/browser/workspace"
    try:
        response = requests.get(url, headers=headers)
        print(f"\n工作区列表接口状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"工作区列表请求失败: {str(e)}")

if __name__ == "__main__":
    print(f"使用的API地址: {BASE_URL}")
    print(f"使用的Token: {API_TOKEN}\n")
    
    test_health_check()
    test_workspaces()