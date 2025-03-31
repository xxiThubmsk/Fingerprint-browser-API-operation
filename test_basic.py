from core import RoxyAPIClient
from utils import get_logger

logger = get_logger("BasicTest")

def test_basic_functions():
    """测试基本功能"""
    client = RoxyAPIClient()
    
    try:
        # 1. 测试健康检查
        logger.info("测试健康检查...")
        health = client.health_check()
        if health.get("code") == 0:
            logger.info("健康检查通过")
        else:
            logger.error(f"健康检查失败: {health}")
            return False

        # 2. 获取工作区列表
        logger.info("获取工作区列表...")
        workspaces = client.get_workspaces()
        if workspaces.get("code") == 0:
            workspace_id = workspaces["data"][0]["id"]  # 使用第一个工作区
            logger.info(f"获取到工作区ID: {workspace_id}")
        else:
            logger.error(f"获取工作区失败: {workspaces}")
            return False

        # 3. 创建一个测试配置文件
        logger.info("创建测试配置文件...")
        create_data = {
            "workspaceId": workspace_id,
            "windowName": "TestProfile",
            "os": "Windows",
            "proxyInfo": {"proxyMethod": "noproxy"},
            "fingerInfo": {"randomFingerprint": True}
        }
        create_result = client.create_profile(create_data)
        if create_result.get("code") == 0:
            dir_id = create_result["data"]["dirId"]
            logger.info(f"成功创建配置文件，ID: {dir_id}")
        else:
            logger.error(f"创建配置文件失败: {create_result}")
            return False

        # 4. 打开配置文件
        logger.info("尝试打开配置文件...")
        open_result = client.open_profile(dir_id)
        if open_result.get("code") == 0:
            logger.info("成功打开配置文件")
        else:
            logger.error(f"打开配置文件失败: {open_result}")
            return False

        # 5. 获取连接信息
        logger.info("获取连接信息...")
        conn_info = client.get_connection_info([dir_id])
        if conn_info.get("code") == 0:
            logger.info(f"成功获取连接信息: {conn_info['data']}")
        else:
            logger.error(f"获取连接信息失败: {conn_info}")
            return False

        # 6. 关闭配置文件
        logger.info("关闭配置文件...")
        close_result = client.close_profile(dir_id)
        if close_result.get("code") == 0:
            logger.info("成功关闭配置文件")
        else:
            logger.error(f"关闭配置文件失败: {close_result}")
            return False

        # 7. 删除测试配置文件
        logger.info("清理测试配置文件...")
        delete_result = client.delete_profile(workspace_id, [dir_id])
        if delete_result.get("code") == 0:
            logger.info("成功删除测试配置文件")
        else:
            logger.error(f"删除配置文件失败: {delete_result}")
            return False

        return True

    except Exception as e:
        logger.error(f"测试过程出错: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_basic_functions()
    if success:
        logger.info("所有基本功能测试通过！")
    else:
        logger.error("测试失败！")