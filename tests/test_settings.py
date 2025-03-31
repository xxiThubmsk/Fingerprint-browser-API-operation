import unittest
import os
from config.settings import (
    API_HOST,
    API_PORT,
    API_TOKEN,
    BASE_URL,
    DEFAULT_WORKSPACE_ID,
    API_ENDPOINTS,
    DEFAULT_HEADERS
)

class TestSettings(unittest.TestCase):
    def test_config_loaded(self):
        """测试配置是否成功加载"""
        self.assertIsNotNone(API_HOST)
        self.assertIsNotNone(API_PORT)
        self.assertIsNotNone(API_TOKEN)
        self.assertTrue(len(API_TOKEN) > 0)  # 确保 TOKEN 不为空
        self.assertEqual(BASE_URL, f"http://{API_HOST}:{API_PORT}")

    def test_api_endpoints(self):
        """测试API端点配置"""
        required_endpoints = [
            "health_check",
            "workspaces",
            "list_profiles",
            "create_profile",
            "modify_profile",
            "open_profile",
            "close_profile",
            "random_fingerprint",
            "delete_profile",
            "connection_info",
            "clear_local_cache"
        ]
        for endpoint in required_endpoints:
            self.assertIn(endpoint, API_ENDPOINTS)
            self.assertTrue(API_ENDPOINTS[endpoint].startswith("/"))

    def test_headers_with_token(self):
        """测试请求头是否包含正确的 Token"""
        self.assertIn("Authorization", DEFAULT_HEADERS)
        self.assertEqual(DEFAULT_HEADERS["Authorization"], API_TOKEN)
        self.assertEqual(DEFAULT_HEADERS["Content-Type"], "application/json")

if __name__ == "__main__":
    unittest.main()