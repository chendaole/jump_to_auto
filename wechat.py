# -*- coding: UTF-8 -*-
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from elementXpath import wechatXpath

def getSize(driver):
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return { 'width': x, 'height': y }

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'emulator-5554',
    'platformVersion': '4.4',
    'appPackage': 'com.tencent.mm',
    'appActivity': 'com.tencent.mm.ui.LauncherUI',
    'noReset': 'true'
}

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, wechatXpath['friendTab']))
element.click()

element = WebDriverWait(driver, 5).until(lambda d: d.find_element(By.XPATH, wechatXpath['friendItem']))
element.click()

time.sleep(5)
rect = getSize(driver)
driver.swipe(rect['width'] / 2, 100, rect['width'] / 2, rect['height'] - 20)

driver.swipe(rect['width'] / 2, 500, rect['width'] / 2, 100)

time.sleep(5)
listView = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, '//android.widget.ListView'))
listItems = listView.find_elements_by_xpath('//android.widget.ListView/android.widget.FrameLayout')
for ele in listItems:
    try:
        elementName = ele.find_element_by_xpath('//android.widget.TextView')
    except Exception as e:
            print "error"
    print elementName.text
print driver.page_source

