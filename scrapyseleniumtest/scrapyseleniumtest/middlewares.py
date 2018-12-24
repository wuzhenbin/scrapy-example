# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import logging

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


class SeleniumMiddleware(): 
    def __init__(self, timeout=None, service_args=[]): 
        print(timeout,'init')
        self.logger = logging.getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        self.logger.debug('selenium is Starting') 
        page = request.meta.get('page', 1)
        try:
            self.browser.get(request.url)

            return HtmlResponse(url=request.url, body=self.browser.page_source, request=request, encoding=' utf-8', status=200)

        except TimeoutException as e:
            return HtmlResponse(url=request.url, status=500, request=request)


    @classmethod 
    def from_crawler(cls, crawler): 
        s = cls(timeout = crawler.settings.get('SELENIUM_TIMEOUT'))
        return s


