from loguru import logger
import sys
import os

# 创建日志目录（使用绝对路径）
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志格式
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 移除默认的处理器
logger.remove()

# 添加控制台处理器
logger.add(
    sys.stderr,
    format=log_format,
    level="INFO",
    enqueue=True
)

# 添加文件处理器
# 修改文件处理器的路径
logger.add(
    os.path.join(log_dir, "roxy_{time:YYYY-MM-DD}.log"),
    format=log_format,
    level="DEBUG",
    rotation="00:00",
    retention="30 days",
    enqueue=True,
    encoding="utf-8"
)

def get_logger(name="RoxyAutomation"):
    """获取配置好的logger实例"""
    return logger.bind(name=name)