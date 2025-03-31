from typing import List, Optional
from core import RoxyAPIClient
from config.settings import DEFAULT_WORKSPACE_ID

def random_fingerprints(
    workspace_id: int = DEFAULT_WORKSPACE_ID,
    dir_ids: Optional[List[str]] = None
) -> bool:
    """为所有或指定的配置文件应用随机指纹"""
    client = RoxyAPIClient()
    
    try:
        if dir_ids is None:
            # 如果没有指定配置文件，获取工作区所有配置文件
            response = client.list_profiles(workspace_id)
            if response.get("code") != 0:
                print(f"获取配置文件列表失败: {response}")
                return False
            
            dir_ids = [profile["dirId"] for profile in response["data"]["list"]]

        success_count = 0
        for dir_id in dir_ids:
            response = client.random_fingerprint(workspace_id, dir_id)
            if response and response.get("code") == 0:
                success_count += 1
                print(f"成功为配置文件 {dir_id} 应用随机指纹")
            else:
                print(f"为配置文件 {dir_id} 应用随机指纹失败: {response}")

        return success_count == len(dir_ids)

    except Exception as e:
        print(f"随机指纹过程出错: {str(e)}")
        return False