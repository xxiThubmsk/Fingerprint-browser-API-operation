from typing import Dict, List, Union, Optional
import random
import string
from .logger import get_logger

logger = get_logger(__name__)

def generate_random_name(prefix: str = "Profile", length: int = 6) -> str:
    """生成随机名称"""
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    return f"{prefix}_{random_str}"

def validate_proxy_config(proxy_info: Dict) -> bool:
    """验证代理配置的有效性"""
    required_fields = {
        'custom': ['proxyHost', 'proxyPort'],
        'auth': ['proxyHost', 'proxyPort', 'username', 'password'],
        'noproxy': []
    }
    
    try:
        proxy_method = proxy_info.get('proxyMethod')
        if proxy_method not in required_fields:
            logger.error(f"无效的代理方法: {proxy_method}")
            return False
            
        for field in required_fields[proxy_method]:
            if field not in proxy_info:
                logger.error(f"缺少必需的代理配置字段: {field}")
                return False
                
        if proxy_method in ['custom', 'auth']:
            port = proxy_info.get('proxyPort')
            if not isinstance(port, int) or not (0 <= port <= 65535):
                logger.error(f"无效的代理端口: {port}")
                return False
                
        return True
        
    except Exception as e:
        logger.error(f"验证代理配置时出错: {str(e)}")
        return False

def format_browser_args(args: List[str]) -> List[str]:
    """格式化浏览器启动参数"""
    valid_args = []
    for arg in args:
        arg = str(arg).strip()
        if arg.startswith('--'):
            valid_args.append(arg)
        else:
            valid_args.append(f"--{arg}")
    return valid_args

def parse_connection_info(conn_info: Dict) -> Optional[Dict]:
    """解析并验证连接信息"""
    try:
        if not conn_info or conn_info.get('code') != 0:
            logger.error("无效的连接信息响应")
            return None
            
        data = conn_info.get('data', {})
        if not data:
            logger.error("连接信息为空")
            return None
            
        result = {}
        for dir_id, info in data.items():
            if 'http' not in info:
                logger.warning(f"配置文件 {dir_id} 缺少HTTP连接信息")
                continue
            result[dir_id] = {
                'http': info['http'],
                'ws': info.get('ws'),
                'driver': info.get('driver')
            }
        return result
        
    except Exception as e:
        logger.error(f"解析连接信息时出错: {str(e)}")
        return None

def batch_process(func, items: List, *args, **kwargs) -> Dict[str, List]:
    """批量处理工具，返回成功和失败的项目"""
    results = {
        'success': [],
        'failed': []
    }
    
    for item in items:
        try:
            if func(item, *args, **kwargs):
                results['success'].append(item)
            else:
                results['failed'].append(item)
        except Exception as e:
            logger.error(f"处理项目 {item} 时出错: {str(e)}")
            results['failed'].append(item)
            
    return results