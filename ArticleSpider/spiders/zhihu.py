# -*- coding: utf-8 -*-
import scrapy
import pyautogui
import time
import datetime
import re
import json
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem
from urllib import parse


class ZhihuSpider(scrapy.Spider):
    # terminal Google\ Chrome --remote-debugging-port=9222
    # make sure all the chrome u open is closed now!!!!!!
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']
    handle_httpstatus_list = [400]

    # question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def start_requests(self):
        return [scrapy.Request("https://www.zhihu.com/signin", headers=self.headers, callback=self.login)]

    def login(self, resoponse):

        chrome_option = Options()
        chrome_option.add_argument("--disable-extensions")
        chrome_option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        broswer = webdriver.Chrome(executable_path="/Users/yangym/tools/chromedriver", chrome_options=chrome_option)
        try:
            broswer.maximize_window()
        except:
            pass

        broswer.get("https://www.zhihu.com/signin")
        login_success = True
        try:
            notify_ele = broswer.find_element_by_class_name(".PushNotifications-count")
        except:
            login_success = False
        print(login_success)
        if login_success == False:
            broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("425708797@qq.com")
            # broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.COMMAND, "a")
            # broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("425708797@qq.com")
            # broswer.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.COMMAND + "a")
            broswer.find_element_by_css_selector(".SignFlow-password input").send_keys("13572428745")
            broswer.find_element_by_css_selector(".SignFlow-submitButton").click()
            time.sleep(1)
        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, headers=self.headers)

        # while not login_success:
        #     print("false")
        #     try:
        #         notify_ele = broswer.find_element_by_class_name("Popover PushNotifications AppHeader-notifications")
        #         login_success = True
        #     except:
        #         pass
        #
        #     try:
        #         english_captcha_element = broswer.find_element_by_class_name("Captcha-englishImg")
        #     except:
        #         english_captcha_element = None
        #
        #     try:
        #         chinese_captcha_element = broswer.find_element_by_class_name("Captcha-chineseImg")
        #     except:
        #         chinese_captcha_element = None
        #
        #     if chinese_captcha_element:
        #         print("chinese")
        #         ele_position = chinese_captcha_element.location
        #         x_relative = ele_position["x"]
        #         y_relative = ele_position["y"]
        #
        #         broswer_navigation_panel_height = broswer.execute_script(
        #             'return window.outerHeight - window.innerHeight;')
        #
        #         base64_text = chinese_captcha_element.get_attribute("src")
        #         import base64
        #         code = base64_text.replace("data:image/jpg;base64,", "").replace("%0A", "")
        #         fh = open("yzm_cn.jpeg", "wb")
        #         fh.write(base64.b64decode(code))
        #         fh.close()
        #
        #         from zheye import zheye
        #
        #         z = zheye()
        #         positions = z.Recognize('yzm_cn.jpeg')
        #         last_postion = []
        #         if len(positions) == 2:
        #             if positions[0][1] > positions[1][1]:
        #                 last_postion.append([positions[1][1], positions[1][0]])
        #                 last_postion.append([positions[0][1], positions[0][0]])
        #             else:
        #                 last_postion.append([positions[0][1], positions[0][0]])
        #                 last_postion.append([positions[1][1], positions[1][0]])
        #             first_position = [int(last_postion[0][0] / 2), int(last_postion[0][1] / 2)]
        #             second_position = [int(last_postion[1][0] / 2), int(last_postion[1][1] / 2)]
        #
        #             first_x = x_relative + first_position[0]
        #             first_y = y_relative + broswer_navigation_panel_height + first_position[1]
        #             pyautogui.click(x=first_x, y=first_y)
        #             time.sleep(3)
        #
        #             second_x = x_relative + second_position[0]
        #             second_y = y_relative + broswer_navigation_panel_height + second_position[1]
        #             pyautogui.click(x=second_x, y=second_y)
        #
        #
        #         else:
        #             last_postion.append([positions[0][1], positions[0][0]])
        #             first_position = [int(last_postion[0][0] / 2), int(last_postion[0][1] / 2)]
        #             first_x = x_relative + first_position[0]
        #             first_y = y_relative + broswer_navigation_panel_height + first_position[1]
        #             pyautogui.click(x=first_x, y=first_y)
        #
        #         broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.COMMAND + Keys.DELETE)
        #         broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("425708797@qq.com")
        #         broswer.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.COMMAND + Keys.DELETE)
        #         broswer.find_element_by_css_selector(".SignFlow-password input").send_keys("13572428745")
        #         broswer.find_element_by_css_selector(".SignFlow-submitButton").click()
        #
        #         login_success = True
        #
        #     if english_captcha_element:
        #         print("english")
        #         base64_text = english_captcha_element.get_attribute("src")
        #         import base64
        #         code = base64_text.replace('data:image/jpg;base64,', '').replace("%0A", "")
        #         fh = open("yzm_en.jpeg", "wb")
        #         fh.write(base64.b64decode(code))
        #         fh.close()
        #
        #         from tools.yundama_requests import YDMHttp
        #         yundama = YDMHttp("xxx", "xxx", 3129, "xxx")
        #         code = yundama.decode("yzm_en.jpeg", 5000, 60)
        #         while True:
        #             if code == "":
        #                 code = yundama.decode("yzm_en.jpeg", 5000, 60)
        #             else:
        #                 break
        #
        #         broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys(Keys.COMMAND + Keys.COMMAND)
        #         broswer.find_element_by_css_selector(".SignFlow-accountInput input").send_keys("425708797@qq.com")
        #         broswer.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.COMMAND + Keys.COMMAND)
        #         broswer.find_element_by_css_selector(".SignFlow-password input").send_keys("13572428745")
        #         broswer.find_element_by_css_selector(".SignFlow-submitButton").click()
        #         login_success = True

    # def check_login(self):
    #
    #     for url in self.start_urls:
    #         yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    def parse(self, response):
        print("test parse")
        """
        提取出html页面中的所有url 并跟踪这些url进行一步爬取
        如果提取的url中格式为 /question/xxx 就下载之后直接进入解析函数
        """
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [parse.urljoin(response.url, url) for url in all_urls]
        all_urls = filter(lambda x:True if x.startswith("https") else False, all_urls)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", url)
            if match_obj:
                # print("test parse question")
                #如果提取到question相关的页面则下载后交由提取函数进行提取
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
                break
            else:
                # print("test parse not question")
                #如果不是question页面则直接进一步跟踪
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)
                # pass

    def parse_question(self, response):
        print("test parse question")
        # 处理question页面， 从页面中提取出具体的question item
        if "QuestionHeader-title" in response.text:
            print("new version")
            # 处理新版本
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_css("title", "h1.QuestionHeader-title::text")
            item_loader.add_css("content", ".QuestionHeader-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", ".List-headerText span::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            # item_loader.add_xpath("watch_user_num", "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".QuestionHeader-topics .Popover div::text")

            question_item = item_loader.load_item()
        else:
            # 处理老版本页面的item提取
            print("old version")
            match_obj = re.match("(.*zhihu.com/question/(\d+))(/|$).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title", "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", ".QuestionHeader-Comment button::text")
            item_loader.add_css("watch_user_num", ".NumberBoard-itemValue::text")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()


        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        # yield question_item

    def parse_answer(self, reponse):
        print("test parse answer")
        # 处理question的answer
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        next_url = ans_json["paging"]["next"]

        # 提取answer的具体字段
        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)
