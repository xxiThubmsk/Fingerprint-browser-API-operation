from typing import Union
from core import RoxyAPIClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_login_task(
    dir_id: Union[str, int],
    url: str,
    username: str,
    password: str,
    username_selector: str,
    password_selector: str,
    submit_selector: str,
    success_selector: str
) -> bool:
    """使用指定配置文件登录特定网站"""
    client = RoxyAPIClient()
    
    try:
        # 打开浏览器配置文件
        response = client.open_profile(dir_id)
        if response.get("code") != 0:
            print(f"打开配置文件失败: {response}")
            return False

        # 获取连接信息
        conn_info = client.get_connection_info([dir_id])
        if conn_info.get("code") != 0:
            print(f"获取连接信息失败: {conn_info}")
            return False

        profile_info = conn_info["data"][str(dir_id)]
        debugger_address = f"{profile_info['http']}"

        # 配置 Chrome 选项
        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = debugger_address

        # 创建 driver
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)

        # 执行登录流程
        driver.get(url)
        
        username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, username_selector)))
        username_input.send_keys(username)
        
        password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, password_selector)))
        password_input.send_keys(password)
        
        submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, submit_selector)))
        submit_button.click()
        
        # 等待登录成功标志
        success_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, success_selector)))
        
        print(f"配置文件 {dir_id} 成功登录到 {url}")
        return True

    except Exception as e:
        print(f"登录过程出错: {str(e)}")
        return False

    finally:
        try:
            client.close_profile(dir_id)
        except:
            pass