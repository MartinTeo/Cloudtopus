# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from sys import platform
import os
import chromedriver_binary

import unittest, time, re

class SeleniumTableau(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.binary_location = "/usr/bin/google-chrome-stable"

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_selenium_tableau(self):
        driver = self.driver
        driver.get("https://public.tableau.com/profile/martin.teo#!/vizhome/FYP1_0/Dashboard1?publish=yes")
        driver.find_element_by_class_name("login-link").click()
        driver.find_element_by_id("login-email").clear()
        driver.find_element_by_id("login-email").send_keys("martin.teo.2016@sis.smu.edu.sg")
        driver.find_element_by_id("login-password").clear()
        driver.find_element_by_id("login-password").send_keys("thunderheadmonkeys2018!")
        driver.find_element_by_id("signin-submit").click()
        for i in range(60):
            try:
                if driver.find_element_by_class_name("viz-refresh-extract").is_displayed(): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_class_name("viz-refresh-extract").click()

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
        print("done tableaurefresh")

    # def run(self):
    #     try:
    #         self.setUp()
    #         self.test_selenium_tableau()
    #         if self.is_element_present() and self.is_alert_present():
    #             self.close_alert_and_get_its_text()
    #         else: self.tearDown()
    #     except Exception as exc:
    #         self.retry(countdown=backoff(self.request.retries), exc=exc)

if __name__ == "__main__":
    unittest.main()
