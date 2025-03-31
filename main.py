import argparse
from utils import get_logger
from tasks import (
    create_multiple_profiles,
    modify_profile_proxies,  # 之前是 modify_proxies
    run_login_task,         # 之前是 run_login
    random_fingerprints
)
from config.settings import DEFAULT_WORKSPACE_ID

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser(description="RoxyBrowser 自动化工具")
    parser.add_argument("--task", required=True, choices=[
        "create", "modify_proxy", "login", "random_fp"
    ], help="要执行的任务")
    
    # 通用参数
    parser.add_argument("--workspace-id", type=int, default=DEFAULT_WORKSPACE_ID, help="工作区ID")
    parser.add_argument("--dir-id", help="配置文件ID")
    
    # 创建配置文件的参数
    parser.add_argument("--num", type=int, default=1, help="要创建的配置文件数量")
    parser.add_argument("--base-name", default="AutoProfile", help="配置文件名称前缀")
    
    # 代理设置参数
    parser.add_argument("--proxy-method", choices=["custom", "auth", "noproxy"], help="代理方法")
    parser.add_argument("--proxy-host", help="代理主机地址")
    parser.add_argument("--proxy-port", type=int, help="代理端口")
    parser.add_argument("--proxy-username", help="代理用户名")
    parser.add_argument("--proxy-password", help="代理密码")
    
    # 登录任务参数
    parser.add_argument("--url", help="登录页面URL")
    parser.add_argument("--username", help="登录用户名")
    parser.add_argument("--password", help="登录密码")
    parser.add_argument("--username-selector", help="用户名输入框的CSS选择器")
    parser.add_argument("--password-selector", help="密码输入框的CSS选择器")
    parser.add_argument("--submit-selector", help="提交按钮的CSS选择器")
    parser.add_argument("--success-selector", help="登录成功标志的CSS选择器")

    args = parser.parse_args()
    
    # 验证工作区ID
    if args.workspace_id <= 0:
        logger.error("工作区ID必须大于0")
        return 1

    try:
        if args.task == "create":
            if args.num <= 0:
                raise ValueError("创建数量必须大于0")
            
            logger.info(f"开始创建 {args.num} 个配置文件")
            created_ids = create_multiple_profiles(
                args.num,
                args.workspace_id,
                args.base_name
            )
            if not created_ids:
                logger.warning("没有成功创建任何配置文件")
                return 1
            logger.info(f"成功创建配置文件: {created_ids}")

        elif args.task == "modify_proxy":
            if not args.dir_id:
                raise ValueError("修改代理任务需要指定 --dir-id")
            
            if args.proxy_method in ["custom", "auth"] and not all([args.proxy_host, args.proxy_port]):
                raise ValueError("自定义代理需要指定主机地址和端口")
            
            proxy_info = {
                "proxyMethod": args.proxy_method or "noproxy"
            }
            if args.proxy_method in ["custom", "auth"]:
                proxy_info.update({
                    "proxyHost": args.proxy_host,
                    "proxyPort": args.proxy_port
                })
                if args.proxy_method == "auth":
                    proxy_info.update({
                        "username": args.proxy_username,
                        "password": args.proxy_password
                    })
            
            success = modify_profile_proxies(args.dir_id, proxy_info, args.workspace_id)
            logger.info("代理修改成功" if success else "代理修改失败")

        elif args.task == "login":
            if not all([args.dir_id, args.url, args.username, args.password,
                       args.username_selector, args.password_selector,
                       args.submit_selector, args.success_selector]):
                raise ValueError("登录任务缺少必要参数")
            
            success = run_login_task(
                args.dir_id,
                args.url,
                args.username,
                args.password,
                args.username_selector,
                args.password_selector,
                args.submit_selector,
                args.success_selector
            )
            logger.info("登录成功" if success else "登录失败")

        elif args.task == "random_fp":
            success = random_fingerprints(
                args.workspace_id,
                [args.dir_id] if args.dir_id else None
            )
            logger.info("随机指纹应用成功" if success else "随机指纹应用失败")

    except Exception as e:
        logger.error(f"执行任务 {args.task} 时出错: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())