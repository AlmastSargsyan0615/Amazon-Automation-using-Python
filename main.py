from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, csv
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.relative_locator import locate_with

from twocaptcha import TwoCaptcha
from amazoncaptcha import AmazonCaptcha
from selenium import webdriver
import requests
import random
import time
import re
from typing import Optional

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
# A package to have a chromedriver always up-to-date.
from webdriver_manager.chrome import ChromeDriverManager

import json

# Load configuration from config.json
with open('config.json', 'r') as file:
    config = json.load(file)

# Access values as needed
site_signin = config["site_signin"]
music_url_all = config["music_url_all"]
user_informations = config["USERINFOMATIONS"]

def chrome_proxy(user: str, password: str, endpoint: str) -> dict:
    wire_options = {
        "proxy": {
            "http": f"http://{user}:{password}@{endpoint}",
            "https": f"http://{user}:{password}@{endpoint}",
        }
    }

    return wire_options

for userinfo in user_informations:
    print(userinfo["EMAIL"],userinfo["PWD"],userinfo["USERNAME"],userinfo["PASSWORD"],userinfo["ENDPOINT"])

    #proxy setting
    proxies = chrome_proxy(userinfo["USERNAME"], userinfo["PASSWORD"], userinfo["ENDPOINT"])

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    # Set options for window size
    options.add_argument("--window-size=1920,1200")
    # Initialize the webdriver
    # driver = webdriver.Chrome(options=options, seleniumwire_options=proxies)
      # Initialize the webdriver
    driver = webdriver.Chrome(options=options)

    # Go to page url
    driver.get("https://www.amazon.com/errors/validateCaptcha")

    while(True):
        try:
        # Check if the input field with id "charactercaptcha" is present
            captcha_input = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "captchacharacters")))
            # If found, print a message and wait for a moment before checking again
            print("Captcha input field found. Waiting...")
            time.sleep(1)
            captcha = AmazonCaptcha.fromdriver(driver)
            solution = captcha.solve()
            print(solution)
            captcha_input.clear()
            # Enter your desired solution
            captcha_input.send_keys(solution)
            captcha_input.send_keys(Keys.RETURN)
        except:
            # If not found, exit the loop
            print("Captcha input field not found. Exiting.")
            break
        
    driver.get(site_signin)
    email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "ap_email")))

    # Clear the existing value in the input field
    email_input.clear()

    # Enter your desired email
    email_input.send_keys(userinfo["EMAIL"])

    # Simulate pressing the Enter key
    email_input.send_keys(Keys.RETURN)

    # Wait for the password input field to be present (adjust the timeout as needed)
    password_input = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "ap_password")))

    # Clear the existing value in the input field
    password_input.clear()

    # Enter your desired password
    password_input.send_keys(userinfo["PWD"])

    # Simulate pressing the Enter key
    password_input.send_keys(Keys.RETURN)

    time.sleep(10)

    driver.get("https://music.amazon.com")
    time.sleep(10)

    random.shuffle(music_url_all)
    for music_url in music_url_all:
        driver.get(music_url)
        driver.maximize_window()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(30)

    time.sleep(30)
