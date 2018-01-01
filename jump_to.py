# -*- coding: UTF-8 -*-
from appium import webdriver
from appium.webdriver.common.touch_action import  TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
import time

screenshot_path = 'D:/temp.png'

desired_caps = {
    'platformName': 'Android',
    'deviceName': '127.0.0.1:21513',
    'platformVersion': '5.1',
    'appPackage': 'com.tencent.mm',
    'appActivity': 'com.tencent.mm.ui.LauncherUI',
    'noReset': 'true',
    'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
}


def find_chess(im, rect):
    width = rect['width']
    height = rect['height']
    for y in range(310, height):
        for x in range(width):
            pixel = im.getpixel((x, y))
            if (pixel[0]==64) and(pixel[1]==50) and (pixel[2]==87):
                return x
            else:
                pass


def find_board(im, chess_x, rect):
    width = rect['width']
    height = rect['height']
    back_color = im.getpixel((300, 250))

    for y in range(310, height):
        for x in range(0, width):

            pixel = im.getpixel((x, y + 5))
            color_range = 20

            print abs(pixel[0] - back_color[0]) + abs(pixel[1] - back_color[1]) + abs(pixel[2] - back_color[2])

            if (abs(pixel[0] - back_color[0]) + abs(pixel[1] - back_color[1]) + abs(pixel[2] - back_color[2]) > color_range):
                return x

def jump(driver, distance):
    magic_num = 2.3

    press_time = distance * magic_num
    press_time = int(press_time)

    TouchAction(driver).press(x=100, y=100).wait(press_time).release().perform()


driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)

element = WebDriverWait(driver, 30).until(lambda d: d.find_element(By.XPATH, './/android.widget.TextView[@text=\'发现\']'))
element.click()


element = WebDriverWait(driver, 30).until(lambda d: d.find_element(By.XPATH, './/android.widget.TextView[@text=\'小程序\']'))
element.click()

element = WebDriverWait(driver, 30).until(lambda d: d.find_element(By.XPATH, './/android.widget.TextView[@text=\'跳一跳\']'))
element.click()

time.sleep(15)
rect = driver.get_window_size()
TouchAction(driver).tap(x=rect['width'] / 2, y= rect['height'] - 250).perform()

time.sleep(5)

while 1:
    driver.get_screenshot_as_file(screenshot_path)
    time.sleep(2)
    im = Image.open(screenshot_path)
    chess_x = find_chess(im, rect)
    board_x = find_board(im, chess_x, rect)
    if chess_x == None:
        print 'not found board'
        break
    distance = abs(chess_x - board_x)
    jump(driver, distance)

