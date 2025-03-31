import unittest
from unittest.mock import patch, Mock
from tasks.create_profiles import create_multiple_profiles
from tasks.modify_proxies import modify_profile_proxies
from tasks.random_all_fp import random_fingerprints
from tasks.run_login import run_login_task

class TestTasks(unittest.TestCase):
    def setUp(self):
        """测试前的准备工作"""
        self.test_workspace_id = 1
        self.test_dir_id = "test_123"
        # 创建一个通用的 mock response
        self.mock_success_response = {"code": 0, "msg": "success", "data": None}

    @patch('core.RoxyAPIClient')
    def test_create_multiple_profiles(self, mock_client):
        """测试批量创建配置文件"""
        # 设置 mock 返回值
        mock_instance = Mock()
        mock_instance.create_profile.return_value = {
            "code": 0,
            "msg": "success",
            "data": {"dirId": self.test_dir_id}
        }
        mock_client.return_value = mock_instance

        result = create_multiple_profiles(2, self.test_workspace_id)
        self.assertEqual(len(result), 2)
        self.assertEqual(mock_instance.create_profile.call_count, 2)

    @patch('core.RoxyAPIClient')
    def test_modify_proxies(self, mock_client):
        """测试修改代理设置"""
        mock_instance = Mock()
        mock_instance.modify_profile.return_value = self.mock_success_response
        mock_client.return_value = mock_instance

        test_proxy = {"proxyMethod": "custom", "proxyHost": "127.0.0.1", "proxyPort": 8080}
        result = modify_profile_proxies(self.test_dir_id, test_proxy)
        self.assertTrue(result)
        mock_instance.modify_profile.assert_called_once()

    @patch('core.RoxyAPIClient')
    def test_random_fingerprints_with_dir_ids(self, mock_client):
        """测试为指定配置文件随机指纹"""
        mock_instance = Mock()
        mock_instance.random_fingerprint.return_value = self.mock_success_response
        mock_client.return_value = mock_instance

        result = random_fingerprints(dir_ids=[self.test_dir_id])
        self.assertTrue(result)
        mock_instance.random_fingerprint.assert_called_once()

    @patch('core.RoxyAPIClient')
    def test_random_fingerprints_all_profiles(self, mock_client):
        """测试为所有配置文件随机指纹"""
        mock_instance = Mock()
        mock_instance.list_profiles.return_value = {
            "code": 0,
            "msg": "success",
            "data": {
                "list": [
                    {"dirId": "test_1"},
                    {"dirId": "test_2"}
                ]
            }
        }
        mock_instance.random_fingerprint.return_value = self.mock_success_response
        mock_client.return_value = mock_instance

        result = random_fingerprints()
        self.assertTrue(result)
        self.assertEqual(mock_instance.random_fingerprint.call_count, 2)

    @patch('core.RoxyAPIClient')
    @patch('selenium.webdriver.Chrome')
    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_run_login(self, mock_wait, mock_chrome, mock_client):
        """测试登录功能"""
        # 设置 RoxyAPIClient 的 mock
        mock_instance = Mock()
        mock_instance.open_profile.return_value = self.mock_success_response
        mock_instance.get_connection_info.return_value = {
            "code": 0,
            "msg": "success",
            "data": {
                str(self.test_dir_id): {"http": "127.0.0.1:1234"}
            }
        }
        mock_instance.close_profile.return_value = self.mock_success_response
        mock_client.return_value = mock_instance

        # 设置 WebDriver 的 mock
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        # 设置 WebDriverWait 的 mock
        mock_wait_instance = Mock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.return_value = Mock()

        result = run_login_task(
            self.test_dir_id,
            "https://example.com",
            "test_user",
            "test_pass",
            "#username",
            "#password",
            "#submit",
            "#success"
        )
        
        self.assertTrue(result)
        mock_instance.open_profile.assert_called_once()
        mock_instance.get_connection_info.assert_called_once()

if __name__ == "__main__":
    unittest.main()