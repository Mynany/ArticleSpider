__author__ = "Pixel"

from selenium import webdriver
from scrapy.selector import Selector
import time
# browser = webdriver.Chrome(executable_path="/Users/yangym/tools/chromedriver")

# login weibo

# browser.get("https://www.weibo.com")
# time.sleep(10)
# browser.find_element_by_css_selector("#loginname").send_keys("425708797@qq.com")
# browser.find_element_by_css_selector(".info_list.password input[node-type='password']").send_keys("Yym13572428745")
# browser.find_element_by_css_selector(".info_list.login_btn a[node-type='submitBtn']").click()

#test scroll

# browser.get("https://www.oschina.net/blog")
# import time
# time.sleep(2)
# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)
# t_selector = Selector(text=browser.page_source)
# print (t_selector.css(".tm-promo-price .tm-price::text").extract())

# set chromedriver do not load images to
# dosent work!!!!!!!!!!!!!!!!!!

# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
# browser.get("https://www.taobao.com")

# phantomjs

browser = webdriver.PhantomJS(executable_path="/Users/yangym/tools/phantomjs-2.1.1-macosx/bin/phantomjs")
browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")

print (browser.page_source)
browser.quit()