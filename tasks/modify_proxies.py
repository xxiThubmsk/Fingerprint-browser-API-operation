from typing import Union, List, Dict
from core import RoxyAPIClient
from config.settings import DEFAULT_WORKSPACE_ID

def modify_profile_proxies(
    dir_ids: Union[str, List[str]],
    proxy_info: Dict,
    workspace_id: int = DEFAULT_WORKSPACE_ID
) -> bool:
    """修改指定配置文件的代理设置"""
    client = RoxyAPIClient()
    
    if isinstance(dir_ids, str):
        dir_ids = [dir_ids]

    success_count = 0
    for dir_id in dir_ids:
        modify_data = {
            "workspaceId": workspace_id,
            "dirId": dir_id,
            "proxyInfo": proxy_info
        }
        
        response = client.modify_profile(modify_data)
        if response and response.get("code") == 0:
            success_count += 1
            print(f"成功修改配置文件 {dir_id} 的代理设置")
        else:
            print(f"修改配置文件 {dir_id} 的代理设置失败: {response}")

    return success_count == len(dir_ids)