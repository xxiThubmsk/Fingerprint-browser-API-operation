from typing import List, Dict, Optional
from core import RoxyAPIClient
from config.settings import DEFAULT_WORKSPACE_ID
import random

def create_multiple_profiles(
    num_profiles: int,
    workspace_id: int = DEFAULT_WORKSPACE_ID,
    base_name: str = "AutoProfile",
    proxy_info: Optional[Dict] = None,
    finger_info: Optional[Dict] = None
) -> List[str]:
    """批量创建配置文件"""
    client = RoxyAPIClient()
    created_ids = []

    default_proxy = proxy_info or {"proxyMethod": "noproxy"}
    default_finger = finger_info or {"randomFingerprint": True}

    for i in range(num_profiles):
        profile_name = f"{base_name}_{i+1}"
        create_data = {
            "workspaceId": workspace_id,
            "windowName": profile_name,
            "os": random.choice(["Windows", "macOS"]),
            "proxyInfo": default_proxy,
            "fingerInfo": default_finger
        }

        response = client.create_profile(create_data)
        if response and response.get("code") == 0:
            dir_id = response["data"]["dirId"]
            created_ids.append(dir_id)
            print(f"成功创建窗口: {profile_name} (ID: {dir_id})")
        else:
            print(f"创建窗口 {profile_name} 失败: {response}")

    return created_ids