from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get("http://localhost:8000")

assert "Congratulations!" in browser.title
time.sleep(3)
