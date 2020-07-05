from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import os
import unittest


# Edith has heard about a cool new online to-do app She goes
# to check out its homepage

#browser.get('http://localhost:8000')

# She notices the page title and header mention to-do lists
#assert 'To-Do' in browser.title, "Browser title was " + browser.title
MAX_WAIT = 10  


#browser.quit()

class FunctionalTest(StaticLiveServerTestCase):

   
    
    def wait_for_now_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        
    def tearDown(self):
        self.browser.quit()
