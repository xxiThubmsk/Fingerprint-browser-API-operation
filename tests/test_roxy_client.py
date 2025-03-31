import unittest
from unittest.mock import patch, Mock
from core import RoxyAPIClient
from config.settings import API_ENDPOINTS

class TestRoxyAPIClient(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.client = RoxyAPIClient()
        self.test_workspace_id = 1
        self.test_dir_id = "test_dir_123"

    @patch('requests.get')
    def test_health_check(self, mock_get):
        """测试健康检查接口"""
        mock_response = Mock()
        mock_response.json.return_value = {"code": 0, "msg": "success"}
        mock_get.return_value = mock_response

        response = self.client.health_check()
        
        mock_get.assert_called_once()
        self.assertEqual(response["code"], 0)

    @patch('requests.get')
    def test_get_workspaces(self, mock_get):
        """测试获取工作区列表"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": [{"id": 1, "name": "默认工作区"}]
        }
        mock_get.return_value = mock_response

        response = self.client.get_workspaces()
        
        self.assertEqual(response["code"], 0)
        self.assertTrue("data" in response)

    @patch('requests.post')
    def test_create_profile(self, mock_post):
        """测试创建配置文件"""
        test_data = {
            "workspaceId": self.test_workspace_id,
            "windowName": "测试窗口",
            "os": "Windows",
            "proxyInfo": {"proxyMethod": "noproxy"},
            "fingerInfo": {"randomFingerprint": True}
        }
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "data": {"dirId": self.test_dir_id}
        }
        mock_post.return_value = mock_response

        response = self.client.create_profile(test_data)
        
        mock_post.assert_called_once()
        self.assertEqual(response["code"], 0)
        self.assertEqual(response["data"]["dirId"], self.test_dir_id)

    @patch('requests.post')
    def test_open_and_close_profile(self, mock_post):
        """测试打开和关闭配置文件"""
        mock_response = Mock()
        mock_response.json.return_value = {"code": 0}
        mock_post.return_value = mock_response

        # 测试打开配置文件
        open_response = self.client.open_profile(self.test_dir_id)
        self.assertEqual(open_response["code"], 0)

        # 测试关闭配置文件
        close_response = self.client.close_profile(self.test_dir_id)
        self.assertEqual(close_response["code"], 0)

    def test_api_endpoints_mapping(self):
        """测试所有API端点是否都有对应的方法"""
        method_mapping = {
            "health_check": self.client.health_check,
            "workspaces": self.client.get_workspaces,
            "list_profiles": self.client.list_profiles,
            "create_profile": self.client.create_profile,
            "modify_profile": self.client.modify_profile,
            "open_profile": self.client.open_profile,
            "close_profile": self.client.close_profile,
            "random_fingerprint": self.client.random_fingerprint,
            "delete_profile": self.client.delete_profile,
            "connection_info": self.client.get_connection_info,
            "clear_local_cache": self.client.clear_local_cache
        }
        
        for endpoint in API_ENDPOINTS:
            self.assertIn(endpoint, method_mapping)
            self.assertTrue(callable(method_mapping[endpoint]))

if __name__ == "__main__":
    unittest.main()