from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
from urllib import parse
# keys like command dosen't work on MacOS
# mouse don't support macos, use pyautogui instead
import pyautogui
import time


chrome_option = Options()
chrome_option.add_argument("--disable-extensions")
chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
broswer = webdriver.Chrome(executable_path="/Users/yangym/tools/chromedriver", chrome_options = chrome_option)
try:
    broswer.maximize_window()
except:
    pass

time.sleep(3)

broswer.get("https://www.weibo.com/login.php")
broswer.find_element_by_css_selector("#loginname").send_keys("425708797@qq.com")
broswer.find_element_by_css_selector(".password .input_wrap .W_input").send_keys("Yym13572428745")
# broswer.find_element_by_xpath('//*[@id="Username"]').send_keys("425708797@qq.com")
# broswer.find_element_by_xpath('//*[@id="Username"]').send_keys("425708797@qq.com")
# broswer.find_element_by_xpath('//*[@id="Password"]').send_keys("Yym13572428745")
broswer.find_element_by_css_selector(".W_btn_a").click()
time.sleep(1)