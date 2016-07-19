#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-07-16 19:42:57
# @Author  : liu yangyang (yangliucs07@163.com)
# @Link    : https://github.com/FlyingHorse
# @Version : $Id$

import time,random,logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level= logging.INFO,
                    filename= 'test_sele.log',
                    filemode='w')

FILES = ['/html/body/div/div[2]/div[1]/div[2]/div/div[4]/ul/li[42]',
'/html/body/div/div[2]/div[1]/div[2]/div/div[4]/ul/li[38]',
'/html/body/div/div[2]/div[1]/div[2]/div/div[4]/ul/li[28]',
'/html/body/div/div[2]/div[1]/div[2]/div/div[4]/ul/li[35]',
'/html/body/div/div[2]/div[1]/div[2]/div/div[4]/ul/li[41]',
'/html/body/div/div[2]/div[1]/div[2]/div/div[4]/ul/li[32]',
]

def simu_pvw(url):

    try:
        brw = webdriver.Firefox()

        start = time.time()
        brw.get(url)
        WebDriverWait(brw, 60, 0.5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[1]/span[2]')))
        end = time.time()
        print( '%s use time % s' % (url, end - start))

        brw.set_window_size(1800,800)

        first = random.randint(0,5)
        #点击file
        brw.find_element_by_xpath('/html/body/div/div[1]/div[1]/span[2]').click()

        #点击ParaviewData 4.1
        brw.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div/div[2]/ul/li[2]').click()
        #点击Data
        brw.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div/div[2]/ul/li[2]').click()
        #点击shuttle-surf.vtm
        brw.find_element_by_xpath(FILES[first]).click()
        time.sleep(1)

        sec = random.randint(0,5)
        while sec == first:
            sec = random.randint(0,5)
        print sec

        #another data file
            #点击file
        brw.find_element_by_xpath('/html/body/div/div[1]/div[1]/span[2]').click()

        #点击ParaviewData 4.1
        #brw.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div/div[2]/ul/li[2]').click()
        #点击Data
        #brw.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[2]/div/div[2]/ul/li[2]').click()
        brw.find_element_by_xpath(FILES[sec]).click()

        time.sleep(5)


        #点击设置
        brw.find_element_by_xpath('/html/body/div/div[1]/div[1]/span[8]').click()
        #设置local
        brw.find_element_by_xpath('/html/body/div/div[2]/div[1]/div[5]/div[1]/div[1]/div/select/option[2]').click()

        time.sleep(5)
        #关闭菜单键
        brw.find_element_by_xpath('/html/body/div/div[1]/div[1]/i').click()


        #ActionChains里边有一个_actions数组，每一个命令都会append进去，perform()时会把每一个命令执行一遍。
        #这里每一个命令都需要重新new一个ActionChains
        #注意offset是相对于当前位置的， xoffset>0为右，yoffset>0为下
        ActionChains(brw).move_by_offset(900,350).perform()
        time.sleep(1)

        xoffset = random.randint(0,200)
        yoffset = random.randint(0,50)
        for i in range(0,300):
            if xoffset > 0:
                xoffset = 0 - random.randint(0,200)
            else:
                xoffset = random.randint(0,200)
            if yoffset >0:
                yoffset = 0 - random.randint(0,50)
            else:
                yoffset = random.randint(0,50)
            print( '%s,  count: %d, xoff:%d, yoff:%d' % (url, i, xoffset, yoffset))
            ActionChains(brw).click_and_hold().move_by_offset(xoffset, yoffset).release().perform()
            time.sleep(random.uniform(0,1.5))

        brw.close()

    except:

        logging.exception('error when selenium, url:%s' % url)


if __name__ == '__main__':
    simu_pvw('http://10.0.0.24:9000/apps/Visualizer/')
