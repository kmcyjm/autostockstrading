
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


CONFIG_FILE = './data/config.json'

with open(CONFIG_FILE, 'r') as f:
    cred = json.load(f)

username = cred['username']
password = cred['password']
SNSEmailARN = cred['SNSEmailARN']
twilioAccountId = cred['twilioAccountId']
twilioAuthToken = cred['twilioAuthToken']
twilioFromPhoneNumber = cred['twilioFromPhoneNumber']
twilioToPhoneNumber = cred['twilioToPhoneNumber']

####################################
# Initialize Selenium + Chromedriver
####################################

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=options)

# start Chrome in normal mode
# driver = webdriver.Chrome()

driver.implicitly_wait(5)

driver.get("https://trader.degiro.nl/login/ie?_ga=2.155780798.424581382.1545820572-1247114947.1542379073#/login")
driver.find_element_by_id("username").click()
driver.find_element_by_id("username").clear()

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").clear()
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_id("loginForm").submit()

time.sleep(5)
