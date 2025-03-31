import requests
from typing import Dict, List, Union, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.settings import (
    BASE_URL,
    API_TOKEN,
    API_ENDPOINTS,
    DEFAULT_HEADERS,
    REQUEST_TIMEOUT,
    MAX_RETRIES
)
from utils import get_logger

logger = get_logger(__name__)

class RoxyAPIClient:
    def __init__(self, base_url: str = BASE_URL, token: str = API_TOKEN):
        self.base_url = base_url
        self.headers = DEFAULT_HEADERS.copy()
        self.headers["Authorization"] = token
        
        # 配置重试策略
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
        
        logger.debug(f"初始化 RoxyAPIClient: base_url={base_url}")

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """发送 GET 请求到指定端点"""
        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug(f"发送 GET 请求: {url}, params={params}")
            response = self.session.get(
                url,
                headers=self.headers,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"GET 请求失败: {url}, 错误: {str(e)}")
            raise

    def _post(self, endpoint: str, data: Dict) -> Dict:
        """发送 POST 请求到指定端点"""
        url = f"{self.base_url}{endpoint}"
        try:
            logger.debug(f"发送 POST 请求: {url}, data={data}")
            response = self.session.post(
                url,
                headers=self.headers,
                json=data,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"POST 请求失败: {url}, 错误: {str(e)}")
            raise

    def health_check(self) -> Dict:
        """检查 API 服务健康状态"""
        return self._get(API_ENDPOINTS["health_check"])

    def get_workspaces(self) -> Dict:
        """获取所有工作区列表"""
        return self._get(API_ENDPOINTS["workspaces"])

    def list_profiles(self, workspace_id: int, sort_nums: str = "", page: int = 1, size: int = 20) -> Dict:
        """获取指定工作区的配置文件列表"""
        params = {
            "workspaceId": workspace_id,
            "sortNums": sort_nums,
            "page": page,
            "size": size
        }
        return self._get(API_ENDPOINTS["list_profiles"], params)

    def get_accounts(self, workspace_id: int, account_id: int = 0, page: int = 1, size: int = 15) -> Dict:
        """获取已配置的平台账号列表"""
        params = {
            "workspaceId": workspace_id,
            "accountId": account_id,
            "page_index": page,
            "page_size": size
        }
        return self._get(API_ENDPOINTS["accounts"], params)

    def get_labels(self, workspace_id: int) -> Dict:
        """获取已配置的标签信息"""
        params = {"workspaceId": workspace_id}
        return self._get(API_ENDPOINTS["labels"], params)

    def create_profile(self, data: Dict) -> Dict:
        """创建新的配置文件"""
        return self._post(API_ENDPOINTS["create_profile"], data)

    def modify_profile(self, data: Dict) -> Dict:
        """修改现有配置文件"""
        return self._post(API_ENDPOINTS["modify_profile"], data)

    def open_profile(self, dir_id: Union[str, int], args: Optional[Union[str, int]] = None) -> Dict:
        """打开指定的配置文件"""
        data = {"dirId": dir_id}
        if args:
            data["args"] = args
        return self._post(API_ENDPOINTS["open_profile"], data)

    def close_profile(self, dir_id: Union[str, int]) -> Dict:
        """关闭指定的配置文件"""
        data = {"dirId": dir_id}
        return self._post(API_ENDPOINTS["close_profile"], data)

    def random_fingerprint(self, workspace_id: int, dir_id: Union[str, int]) -> Dict:
        """为指定配置文件随机生成指纹"""
        data = {
            "workspaceId": workspace_id,
            "dirId": dir_id
        }
        return self._post(API_ENDPOINTS["random_fingerprint"], data)

    def delete_profile(self, workspace_id: int, dir_ids: List[Union[str, int]]) -> Dict:
        """删除指定的配置文件"""
        data = {
            "workspaceId": workspace_id,
            "dirIds": dir_ids
        }
        return self._post(API_ENDPOINTS["delete_profile"], data)

    def get_connection_info(self, dir_ids: Optional[List[Union[str, int]]] = None) -> Dict:
        """获取已打开窗口的连接信息"""
        data = {}
        if dir_ids:
            data["dirIds"] = dir_ids
        return self._post(API_ENDPOINTS["connection_info"], data)

    def clear_local_cache(self, dir_ids: List[Union[str, int]]) -> Dict:
        """清空指定配置文件的本地缓存"""
        data = {"dirIds": dir_ids}
        return self._post(API_ENDPOINTS["clear_local_cache"], data)

    def clear_server_cache(self, workspace_id: int, dir_ids: List[Union[str, int]]) -> Dict:
        """清空指定配置文件的服务器缓存"""
        data = {
            "workspaceId": workspace_id,
            "dirIds": dir_ids
        }
        return self._post(API_ENDPOINTS["clear_server_cache"], data)