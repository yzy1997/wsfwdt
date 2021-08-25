import html
from typing import Tuple
from selenium import webdriver
from lxml import etree
import time
from selenium.webdriver import chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import smtplib
from email.mime.text import MIMEText
# from threading import Timer
# from time import sleep
# from msedge.selenium_tools import EdgeOptions
# from msedge.selenium_tools import Edge


# "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222   # 这里修改为你的chrome路径

# class RepeatedTimer(object):
#     def __init__(self, interval, function, *args, **kwargs):
#         self._timer     = None
#         self.interval   = interval
#         self.function   = function
#         self.args       = args
#         self.kwargs     = kwargs
#         self.is_running = False
#         self.start()

#     def _run(self):
#         self.is_running = False
#         self.start()
#         self.function(*self.args, **self.kwargs)

#     def start(self):
#         if not self.is_running:
#             self._timer = Timer(self.interval, self._run)
#             self._timer.start()
#             self.is_running = True

#     def stop(self):
#         self._timer.cancel()
#         self.is_running = False

def initial():
    # driver_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe'
    driver_path = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe' # 这里修改为你的chromedrive.exe路径
    options = Options()
    # options.use_chromium = True
    # options.add_argument('headless')
    options.add_argument('disable-gpu')

    # # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
    # options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--ignore-ssl-errors")
    # options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    # options.add_argument('--user-agent=%s' % user_agent)
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    # print(driver.window_handles)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    # driver.maximize_window()
    clear_brower_data(driver)
    # driver.get('https://eportal.uestc.edu.cn/new/index.html')
    driver.get('https://eportal.uestc.edu.cn/jkdkapp/sys/lwReportEpidemicStu/index.do?t_s=1629700640487&amp_sec_version_=1&gid_=YTR5VlBlZDNHQUh4bkV6bTlKcDVuRFh4S1dnTEZOb1BHK016S1ZraitIWGVtdEY4ZmZIWWFVNXNGU3N0K3Vuc01UWmlEWWFLd0xVWEF6VnEzd2tDOUE9PQ&EMAP_LANG=zh&THEME=indigo#/dailyReport')
    return driver


def parse_page_index(driver):
    WebDriverWait(driver=driver, timeout=20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@id='ampHasNoLogin']"))
    )
    # source = driver.page_source
    login_btn = driver.find_element_by_xpath("//div[@id='ampHasNoLogin']")
    # login_btn.click()
    # print(driver.window_handles)


def parse_page_login(driver, name):
    # url_auth = 'https://idas.uestc.edu.cn/authserver/login?service=https%3A%2F%2Feportal.uestc.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Feportal.uestc.edu.cn%2Fnew%2Findex.html'
    # driver.execute_script('window.open("%s")' % url_auth)
    # driver.switch_to.window(driver.window_handles[1])
    # print(driver.window_handles)
    # source_auth = driver.page_source
    # send_user_pass(driver)
    # clear_brower_data(driver)
    # driver.refresh()
    WebDriverWait(driver=driver, timeout=20).until(
        EC.presence_of_element_located((By.XPATH, "//div[@data-action='add']"))
    )
    actions = ActionChains(driver=driver)
    health_btn = driver.find_element_by_xpath('//div[@data-action="add"]')
    actions.click(health_btn).perform()
    time.sleep(3)
    if (isElementExist(driver, "//div[@data-action='save']")==False) and (isElementExist(driver, "/html/body/div[11]/div[1]/div[1]/div[2]/div[2]/a")==False):
        print("error! 打卡失败!!!")
        send_email("error! %s打卡失败!!!" % name, "error! %s打卡失败!!!" % name)
        return
    try:
        actions = ActionChains(driver=driver)
        save_btn = driver.find_element_by_xpath("//div[@data-action='save']")
        driver.implicitly_wait(10)
        actions.move_to_element(save_btn).click(save_btn).perform()
        time.sleep(3)
        WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[29]/div[1]/div[1]/div[2]/div[2]/a[1]"))
        )
        post_btn = driver.find_element_by_xpath("/html/body/div[29]/div[1]/div[1]/div[2]/div[2]/a[1]")
        ActionChains(driver).move_to_element(post_btn).click(post_btn).perform()
        print("OKK~打卡成功")
        send_email("OKK~%s打卡成功" % name, "OKK~%s打卡成功" % name)
    except:
        time.sleep(3)
        confirm_btn = driver.find_element_by_xpath("/html/body/div[11]/div[1]/div[1]/div[2]/div[2]/a")
        ActionChains(driver).move_to_element(confirm_btn).click(confirm_btn).perform()
        print("害，已经打过卡了")
        send_email("害，%s已经打过卡了" % name, "害，%s已经打过卡了" % name)
    # driver.execute_script("$(arguments[0]).click()", click_btn)


def clear_brower_data(driver):
    # url_clear = 'chrome://settings/clearBrowserData'
    # driver.get(url_clear)
    # driver.switch_to.window(driver.window_handles[1])
    driver.delete_all_cookies()


def isElementExist(driver, element):
    flag = True
    try:
        WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.XPATH, element))
        )
        return flag
    except:
        flag = False
        return flag


def send_email(title, content):
    mail_host = 'smtp.163.com'  # 以163邮箱为例
    mail_user = '' # 163邮箱用户名 
    #密码(部分邮箱为授权码) 
    mail_pass = ''   
    sender = '@163.com'  # 发送邮箱的地址 
    receivers = ['']  # 接收邮箱的地址
    message = MIMEText(content, 'plain', 'utf-8')      
    message['Subject'] = title 
    message['From'] = sender      
    message['To'] = receivers[0]  

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)
        smtpObj.login(mail_user, mail_pass) 
        smtpObj.sendmail(sender, receivers, message.as_string()) 
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) 


def automation(driver, name):
    while True:
        parse_page_login(driver=driver, name=name)
        i = 0
        while True:
            time.sleep(5*60)
            driver.refresh()
            i = i + 1
            if i >= 287:
                break
        time.sleep(5*60)


# def send_user_pass(driver):
    # username = driver.find_element_by_id('username')
    # password = driver.find_element_by_id('password')
    # click_btn = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[6]/div/form/p[4]/button')
    # actions = ActionChains(driver=driver)
    # actions.move_to_element(username)
    # actions.send_keys('username')
    # actions.move_to_element(password)
    # actions.send_keys_to_element(password, 'password')
    # actions.move_to_element(click_btn)
    # actions.click()
    # actions.perform()
    # username.send_keys('username')
    # password.send_keys('password')
    # time.sleep(1)
    # driver.delete_all_cookies()
    # click_btn.click()
    # submit = driver.find_element_by_tag_name('form')
    # submit.submit()
    # js = """
    # document.getElementById('username').value='username';
    # document.getElementById('password').value='password';
    # document.getElementsByTagName('button')[0].click();
    # """
    # driver.execute_script(js)
    # health_btn.click()

# def keep_login(driver):
#     driver.refresh()



if __name__ == '__main__':
    name = ''  # 这里填你的名字
    driver = initial()
    # parse_page_index(driver=driver)
    automation(driver=driver, name=name)

