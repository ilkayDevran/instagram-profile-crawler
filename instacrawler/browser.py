#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @author: Ilkay Tevfik Devran
# @updatedDate: 22.04.2019
# @version: 1.0 


import os
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


class Browser:
    def __init__(self, run_locally=False):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        chrome_options = Options()
        
        if run_locally:
            print "RUN LOCALLY"
            driver_path = '%s/bin/chromedriver' % dir_path
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
        else:
            print "RUN LAMBDA"
            driver_path = drvr_path or '%s/bin/chromedriver-linux' % dir_path
            chrome_options.binary_location = '%s/bin/headless-chromium-linux' % dir_path
            chrome_options.add_argument("--headless")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
        self.driver.implicitly_wait(5)

    @property
    def page_height(self):
        return self.driver.execute_script('return document.body.scrollHeight')

    @property
    def current_url(self):
        return self.driver.current_url

    def go(self, url):
        self.driver.get(url)

    def implicitly_wait(self, t):
        self.driver.implicitly_wait(t)
    
    def find_one(self, css_selector, elem=None, waittime=0, x_path=None):
        "example to find posts on profile 263px .v1Nh3 div .KL4Bh"
        ".v1Nh3 a -> 470px"
        obj = elem or self.driver
        if x_path == None:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )

            try:
                #return self.driver.find_element(By.CSS_SELECTOR, css_selector)
                return obj.find_element_by_css_selector(css_selector)
            except NoSuchElementException:
                return None
        else:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.xpath, x_path))
                )

            try:
                return obj.find_element_by_xpath(x_path)
            except NoSuchElementException:
                return None
    
    def find(self, css_selector, elem=None, waittime=0, x_path=None):
        obj = elem or self.driver
        if x_path == None:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))
                )

            try:
                return obj.find_elements_by_css_selector(css_selector)
            except NoSuchElementException:
                return None
        else:
            if waittime:
                WebDriverWait(obj, waittime).until(
                    EC.presence_of_element_located((By.xpath, x_path))
                )

            try:
                return obj.find_elements_by_xpath(x_path)
            except NoSuchElementException:
                return None


    def js_click(self, elem):
        self.driver.execute_script("arguments[0].click();", elem)

    def scroll_down(self, wait=0.3):
        self.driver.execute_script(
            'window.scrollTo(0, document.body.scrollHeight)')
        self.randmized_sleep(wait)

    def scroll_up(self, offset=-1, wait=2):
        if (offset == -1):
            self.driver.execute_script('window.scrollTo(0, 0)')
        else:
            self.driver.execute_script('window.scrollBy(0, -%s)' % offset)
        self.randmized_sleep(wait)

    def randmized_sleep(self, average = 1):
        _min, _max = average * 1/2, average * 3/2
        sleep(random.uniform(_min, _max))

    def __del__(self):
        print "QUIT"
        try:
            self.driver.quit()
        except Exception:
            pass


