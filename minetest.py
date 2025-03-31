import requests
import json
import time

class RoxyClient:
    '''
    :param port: api服务的端口号
    :param token: api服务的token
    '''
    def __init__(self,port:int,token:str) -> None:
        self.port = port 
        self.host = "127.0.0.1"
        self.token = token
        self.url = f"http://{self.host}:{self.port}"

    def _build_headers(self):
        return {"Content-Type": "application/json","token":self.token}
    
    def _post(self,path,data = None):
        return requests.post(self.url + path,json=data,headers=self._build_headers())
    
    def _get(self,path,data = None):
        return requests.get(self.url + path,params=data,headers=self._build_headers())

    '''
    健康检查,用于检查API服务是否正常运行,文档地址:https://roxybrowser.com/api/v2/#/api_health
    '''
    def health(self):
        return self._get("/health").json()
    
    '''
    获取工作空间项目列表,用于获取已拥有的空间和项目列表,文档地址:https://roxybrowser.com/api/v2/#/api_workspace
    :param page_index,page_size 分页参数
    '''
    def workspace_project(self):
        return self._get("/browser/workspace").json()

    '''
    获取账号列表,用于获取已配置的平台账号,文档地址:https://roxybrowser.com/api/v2/#/api_account
    :param workspaceId: 工作空间id, 必填，指定要获取哪个空间下的平台账号，通过workspace_project方法获取
    :param accountId: 账号库id, 选填
    :param page_index,page_size 分页参数
    '''
    def account(self,workspaceId:int,accountId:int = 0,page_index:int = 1,page_size:int = 15):
        return self._get("/browser/account",{"workspaceId":workspaceId,"accountId":accountId,"page_index":page_index,"page_size":page_size}).json()
    '''
    获取标签列表,用于获取已配置的标签信息,文档地址:https://roxybrowser.com/api/v2/#/api_label
    :param workspaceId: 工作空间id, 必填，指定要获取哪个空间下的标签，通过workspace_project方法获取
    '''
    def label(self,workspaceId:int):
        return self._get("/browser/label",{"workspaceId":workspaceId}).json()
    '''
    获取窗口列表,文档地址: https://roxybrowser.com/api/v2/#/api_list
    :param workspaceId: 工作空间id, 必填，指定要获取哪个空间下的窗口列表，通过workspace_project方法获取
    :param dirId: 窗口id, 选填；如果填了就只查询这个窗口的信息
    :param page_index,page_size 分页参数
    :res 返回值参考文档
    '''
    def browser_list(self,workspaceId:int,sortNums:str = "",page_index:int = 1,page_size:int = 15):
        return self._get("/browser/list_v2",{"workspaceId":workspaceId,"sortNums":sortNums,"page_index":page_index,"page_size":page_size}).json()
    

    '''
    创建窗口,文档地址: https://roxybrowser.com/api/v2/#/api_create
    :param data: 创建窗口需要传的参数,参考文档说明，其中workspaceId为必传，通过workspace_project方法获取
    :res 返回值参考文档
    '''
    def browser_create(self,data:dict = None):
        return self._post("/browser/create",data).json()

    '''
    修改窗口，文档地址: https://roxybrowser.com/api/v2/#/api_mdf
    :param data: 修改窗口需要传的参数,参考文档说明，其中workspaceId和dirId为必传，workspaceId通过workspace_project方法获取
    :res 返回值参考文档
    '''
    def browser_mdf(self,data:dict):
        return self._post("/browser/mdf",data).json()
    
    '''
    删除窗口,文档地址:https://roxybrowser.com/api/v2/#/api_delete
    :param workspaceId: 工作空间id, 必填，指定窗口所在的空间，通过workspace_project方法获取
    :param dirIds: 窗口id列表, 必填，指定要删除的浏览器窗口列表
    :res 返回值参考文档
    '''
    def browser_delete(self,workspaceId:int,dirIds:list):
        return self._post("/browser/delete",{"workspaceId":workspaceId,"dirIds": dirIds}).json()
    
    '''
    打开窗口,文档地址：https://roxybrowser.com/api/v2/#/api_open
    :param dirId: 需要打开的窗口ID，必填
    :param args: 指定浏览器启动参数，选填
    :res 返回值参考文档
    '''
    def browser_open(self,dirId:str,args=[]):
        return self._post("/browser/open",{"dirId":dirId,"args": args}).json()
        
    '''
    关闭窗口,文档地址:https://roxybrowser.com/api/v2/#/api_close
    :param dirId: 需要关闭的窗口ID，必填
    :res 返回值参考文档
    '''
    def browser_close(self,dirId:str):
        return self._post("/browser/close",{"dirId":dirId}).json()

    '''
    窗口随机指纹,文档地址：https://roxybrowser.com/api/v2/#/api_random_env
    :param workspaceId: 工作空间id, 必填，指定窗口所在的空间，通过workspace_project方法获取
    :param dirId: 窗口id, 必填，指定需要随机指纹的窗口
    :res 返回值参考文档
    '''
    def browser_random_env(self,workspaceId:int,dirId:str):
        return self._post("/browser/random_env",{"workspaceId": workspaceId,"dirId":dirId}).json()
    
    '''
    清空窗口本地缓存,文档地址:https://roxybrowser.com/api/v2/#/api_local_cache
    :param dirIds: 窗口id列表, 必填，指定要清空缓存的窗口列表
    :res 返回值参考文档
    '''
    def browser_local_cache(self,dirIds:list):
        return self._post("/browser/clear_local_cache",{"dirIds":dirIds}).json()
    
    '''
    清空窗口服务器缓存,文档地址:https://roxybrowser.com/api/v2/#/api_server_cache
    :param workspaceId: 工作空间id, 必填，指定窗口所在的空间，通过workspace_project方法获取
    :param dirIds: 窗口id列表, 必填，指定要清空缓存的窗口列表
    :res 返回值参考文档
    '''
    def browser_server_cache(self,workspaceId:int,dirIds:list):
        return self._post("/browser/clear_server_cache",{"workspaceId": workspaceId,"dirIds":dirIds}).json()
    
    '''
    获取已打开的浏览器信息,文档地址:https://roxybrowser.com/api/v2/#/api_pid
    :param dirIds: 需要查询的窗口ID，选填
    :res 返回值参考文档
    '''
    def browser_connection_info(self,dirIds=[]):
        return self._get("/browser/connection_info",{"dirIds":dirIds}).json()

if __name__ == "__main__":
    client = RoxyClient(port=40004,token="a24a6b81e4ecde903b98c09b42ec64a8")
    print(client.health())
    print(client.workspace_project())
    #print(client.account(workspaceId=10))
    #print(client.browser_list(workspaceId=10,sortNums="1,2"))
    '''
    data = {
        "workspaceId": 10,
        "windowName":"启动时随机指纹",
        "coreVersion":"117",
        "os":"Windows",
        "osVersion": "11",
        "windowRemark":"备注",
        "proxyInfo":{
            "proxyMethod":"custom",
            "proxyCategory":"SOCKS5",
            "ipType":"IPV4",
            "protocol":"SOCKS5",
            "host":"xxx",
            "port":"1200",
            "proxyUserName":"xxx",
            "proxyPassword":"xxx"
        },
        "fingerInfo":{
            "randomFingerprint":False,
            "portScanProtect":False
        }
    }
    print(client.browser_create(data))
    
    data = {
        "workspaceId": 10,
        "dirId":"ac4bd731074a6ef3bbe1e8f4f6667749",
        "windowName":"修改窗口",
        "coreVersion":"109",
        "os":"macOS",
        "proxyInfo":{
            "port":"1000"
        }
    }
    print(client.browser_mdf(data))
    
    '''
    #print(client.browser_delete(workspaceId=10,dirIds=["ac4bd731074a6ef3bbe1e8f4f6667749"]))
    # print(client.browser_open(dirId="ac4bd731074a6ef3bbe1e8f4f6667749"))
    #print(client.browser_close(dirId="ac4bd731074a6ef3bbe1e8f4f6667749"))
    #print(client.browser_random_env(workspaceId=10,dirId="ac4bd731074a6ef3bbe1e8f4f6667749"))
    #print(client.browser_local_cache(dirIds=["ac4bd731074a6ef3bbe1e8f4f6667749"]))
    #print(client.browser_server_cache(workspaceId=10,dirIds=["ac4bd731074a6ef3bbe1e8f4f6667749"]))
    # print(client.browser_connection_info())