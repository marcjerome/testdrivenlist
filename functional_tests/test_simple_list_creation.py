from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):      
    def test_can_start_a_list_for_one_user(self):
        # Edith has heard about a cool new online to-do app She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)
            
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start a new To-Do list', header_text)
        
        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # She types "Buy peacock feathers" into a text box (Edith's hobby)
        # is tying fly-fishing lures
        inputbox.send_keys('Buy peacock feathers')
        
        # When she hits enter, the page updates and now the page lsits 
        # "1. Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table('1: Buy peacock feathers')
        #time.sleep(3)
        
        #self.check_for_row_in_list_table('1: Buy peacock #feathers')
              
        
        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)
               
        # The page updates again, and now shows both items on her list
        self.wait_for_now_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_now_in_list_table('1: Buy peacock feathers')

        
        # Edith wonders wether the site will remember her list. The she sees 
        # that the site has generated a unique URL for her -- there is some 
        # explanatory text to that effect. 
        #self.fail('Finish the test')
        #She visits that URL - her to-do list is still there

        # Satisfied, she goes back to sleep
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table('1: Buy peacock feathers')
        
        #She notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        
        #Now a new user, Francis, comes along to the site. 
        ##We use a new browser session to make sure that no 
        ##information of Edith's is coming through from coockies etc. 
        
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        #Francis visits the homepage. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
        #Francis starts a new list by entering a new item. He
        #is less interesting than Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table('1: Buy milk')
        
        #Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)
        
        #Again there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)  
        
        #She starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_now_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
            )