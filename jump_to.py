# -*- coding: UTF-8 -*-
from appium import webdriver
from appium.webdriver.common.touch_action import  TouchAction
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image, ImageEnhance, ImageDraw
import time
import math

screenshot_path = 'D:/temp.png'

desired_caps = {
    'platformName': 'Android',
    'deviceName': '127.0.0.1:21503',
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
                return (x, y + 50)
            else:
                pass


def find_board(im, rect):
    width = rect['width']
    height = rect['height']

    #增强背景对比度
    enh_color = ImageEnhance.Color(im)
    em_im = enh_color.enhance(100)
    em_im.convert('L')

    back_color = em_im.getpixel((50, 50))

    for y in range(310, height):
        for x in range(0, width):

            pixel = em_im.getpixel((x, y + 5))
            color_range = 80

            if (abs(pixel[0] - back_color[0]) + abs(pixel[1] - back_color[1]) + abs(pixel[2] - back_color[2]) > color_range):
                return (x, y + 80)


def jump(driver, distance):
    magic_num = 1.781

    if distance < 340:
        magic_num = 1.721
    elif distance < 150:
        magic_num = 1.55

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
    try:
        # 等待chess动画结束
        time.sleep(3)
        print '等待动画结束'
        driver.get_screenshot_as_file(screenshot_path)
        im = Image.open(screenshot_path)
        print '开始捕获位置'
        chess_position = find_chess(im, rect)
        board_position = find_board(im, rect)
        if chess_position == None:
            print 'not found board'
            break
        distance = math.sqrt(
            abs(chess_position[0] - board_position[0]) ** 2 + abs(chess_position[0] - board_position[1]) ** 2)

        print '跳跃距离:' + str(distance)

        jump(driver, distance)

    except Exception as e:
        draw = ImageDraw.Draw(im)
        draw.rectangle((chess_position[0], chess_position[1], chess_position[0] + 10, chess_position[1] + 10), fill=128)
        draw.rectangle((board_position[0], board_position[1], board_position[0] + 10, board_position[1] + 10), fill=128)
        im.show()

