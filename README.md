# Fingerprint Browser API 操作工具

这是一个用于操作指纹浏览器API的Python工具包，提供了完整的API客户端封装，可以方便地进行浏览器指纹管理和自动化操作。本工具支持多工作区管理、多账号管理、自动化任务执行等高级功能。

## 功能特性

### 完整的API客户端封装
- **健康检查**：实时监控API服务状态
- **工作区管理**：多工作区创建、查询和管理
- **账号管理**：支持多平台账号配置和管理
- **标签管理**：浏览器标签页的创建、切换和关闭
- **浏览器窗口管理**：窗口的创建、修改、打开、关闭等操作
- **指纹管理**：浏览器指纹的随机化和自定义配置
- **缓存管理**：本地和服务器缓存的清理和维护

### 自动化任务脚本
- **批量创建浏览器配置**：快速部署多个定制化的浏览器环境
- **批量修改代理设置**：灵活配置和更新代理服务器
- **批量随机指纹**：自动化更新浏览器指纹特征
- **自动化登录**：支持多平台的自动化登录流程

## 项目架构

```
├── config/          # 配置文件目录
│   ├── .env        # 环境变量配置
│   └── settings.py # 全局设置
├── core/           # 核心功能模块
│   └── roxy_client.py # API客户端实现
├── tasks/          # 自动化任务脚本
│   ├── create_profiles.py # 批量创建配置
│   ├── modify_proxies.py  # 代理设置
│   ├── random_all_fp.py   # 随机指纹
│   └── run_login.py       # 自动登录
├── tests/          # 单元测试
│   ├── test_roxy_client.py # API测试
│   └── test_tasks.py       # 任务测试
├── utils/          # 工具函数
│   ├── helpers.py # 辅助函数
│   └── logger.py  # 日志工具
└── main.py        # 主程序入口
```

### 核心模块说明

#### 1. API客户端(core/roxy_client.py)
- 封装所有API接口调用
- 处理请求认证和错误处理
- 提供友好的接口调用方式

#### 2. 自动化任务(tasks/)
- 实现常用自动化操作
- 支持批量处理和定时任务
- 提供可扩展的任务框架

#### 3. 工具类(utils/)
- 提供通用辅助函数
- 统一的日志记录机制
- 错误处理和异常管理

## 快速开始

### 1. 环境准备

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 配置说明
在config/.env文件中配置以下参数：

```ini
# API服务配置
API_PORT=40004      # API服务端口
API_TOKEN=your_token # API访问令牌

# 日志配置
LOG_LEVEL=INFO     # 日志级别(DEBUG/INFO/WARNING/ERROR)
LOG_FORMAT=default # 日志格式(default/json)
LOG_PATH=./logs    # 日志保存路径

# 代理配置
PROXY_HOST=        # 代理服务器地址
PROXY_PORT=        # 代理服务器端口
PROXY_USER=        # 代理认证用户名
PROXY_PASS=        # 代理认证密码
```

### 2. 使用示例
```python
from core.roxy_client import RoxyClient

# 初始化客户端
client = RoxyClient(port=40004, token="your_token")

# 健康检查
print(client.health())

# 获取工作区列表
print(client.workspace_project())

# 创建浏览器窗口
data = {
    "workspaceId": 10,
    "windowName": "测试窗口",
    "coreVersion": "117",
    "os": "Windows",
    "osVersion": "11",
    "fingerInfo": {
        "randomFingerprint": True
    }
}
print(client.browser_create(data))
```

## API文档

### 核心API

#### 健康检查
```python
health() -> dict
```
检查API服务是否正常运行
- 返回值：{'status': 'ok'} 表示服务正常

#### 工作区管理
```python
workspace_project() -> list
```
获取工作区和项目列表
- 返回值：工作区和项目信息列表

#### 账号管理
```python
account(workspaceId: int, accountId: int = 0) -> dict
```
获取已配置的平台账号
- 参数：
  - workspaceId: 工作区ID
  - accountId: 账号ID，默认为0获取所有账号
- 返回值：账号配置信息

#### 浏览器窗口管理
```python
# 创建窗口
browser_create(data: dict) -> dict
'''
参数示例：
{
    "workspaceId": 10,
    "windowName": "测试窗口",
    "coreVersion": "117",
    "os": "Windows",
    "osVersion": "11",
    "fingerInfo": {
        "randomFingerprint": True,
        "webgl": "noise",
        "canvas": "noise",
        "clientRects": "noise"
    }
}
'''

# 修改窗口
browser_mdf(data: dict) -> dict

# 删除窗口
browser_delete(workspaceId: int, dirIds: list) -> dict

# 打开窗口
browser_open(dirId: str) -> dict

# 关闭窗口
browser_close(dirId: str) -> dict
```

#### 指纹管理
```python
# 随机指纹
browser_random_env(workspaceId: int, dirId: str) -> dict
```
- 参数：
  - workspaceId: 工作区ID
  - dirId: 浏览器窗口ID
- 返回值：新的指纹配置信息

#### 缓存管理
```python
# 清空本地缓存
browser_local_cache(dirIds: list) -> dict

# 清空服务器缓存
browser_server_cache(workspaceId: int, dirIds: list) -> dict
```

## 自动化任务使用说明

### 批量创建浏览器配置(create_profiles.py)
```python
from tasks.create_profiles import create_profiles

# 创建10个浏览器配置
configs = {
    "workspaceId": 1,
    "count": 10,
    "baseConfig": {
        "os": "Windows",
        "osVersion": "11",
        "coreVersion": "117"
    }
}
create_profiles(configs)
```

### 批量修改代理设置(modify_proxies.py)
```python
from tasks.modify_proxies import modify_proxies

# 更新指定窗口的代理设置
proxy_data = {
    "workspaceId": 1,
    "dirIds": ["dir1", "dir2"],
    "proxy": {
        "host": "proxy.example.com",
        "port": 8080,
        "username": "user",
        "password": "pass"
    }
}
modify_proxies(proxy_data)
```

### 批量随机指纹(random_all_fp.py)
```python
from tasks.random_all_fp import random_fingerprints

# 为工作区内所有窗口随机化指纹
random_fingerprints(workspaceId=1)
```

### 自动化登录(run_login.py)
```python
from tasks.run_login import auto_login

# 执行自动登录
login_data = {
    "platform": "example.com",
    "username": "user@example.com",
    "password": "password"
}
auto_login(login_data)
```

## 测试用例说明

### 运行测试
```bash
# 运行所有测试
python -m unittest discover tests

# 运行特定测试文件
python -m unittest tests/test_roxy_client.py
```

### 测试覆盖范围

#### API客户端测试(test_roxy_client.py)
- 健康检查接口测试
- 工作区管理接口测试
- 账号管理接口测试
- 浏览器窗口操作测试
- 指纹管理功能测试
- 错误处理和异常测试

#### 自动化任务测试(test_tasks.py)
- 批量配置创建测试
- 代理设置修改测试
- 指纹随机化测试
- 自动登录流程测试

## 日志配置

### 日志文件
- 位置：logs目录
- 命名格式：roxy_YYYY-MM-DD.log
- 日志级别：可在.env中配置(DEBUG/INFO/WARNING/ERROR)

### 日志格式
```python
# 默认格式
2024-03-31 10:00:00 [INFO] message

# JSON格式
{"timestamp": "2024-03-31 10:00:00", "level": "INFO", "message": "content"}
```

## 许可证

本项目基于MIT许可证开源。详细信息请参阅LICENSE文件。

