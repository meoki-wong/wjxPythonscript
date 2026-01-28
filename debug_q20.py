#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试第20题的结构 - 检查为什么少填了一个选项
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def debug_q20_structure():
    """调试第20题的结构"""
    print("正在调试第20题的结构...")
    
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    
    try:
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(1200, 800)
        
        url = "https://v.wjx.cn/vm/h9RwweO.aspx#"
        print(f"打开问卷: {url}")
        driver.get(url)
        time.sleep(5)
        
        print(f"页面标题: {driver.title}")
        
        # 查找第20题
        print("\n=== 调试第20题结构 ===")
        
        # 检查第20题的整体结构
        q20_div = driver.find_element(By.CSS_SELECTOR, "#div20")
        print(f"找到第20题div元素")
        
        # 查找所有子问题
        sub_questions = driver.find_elements(By.CSS_SELECTOR, "#div20 tr")
        print(f"找到 {len(sub_questions)} 行(tr)元素")
        
        for i, row in enumerate(sub_questions, 1):
            print(f"\n第{i}行内容:")
            row_text = row.text.strip()
            print(f"  文本内容: {row_text}")
            
            # 查找这一行的选项
            options = row.find_elements(By.CSS_SELECTOR, "td")
            print(f"  找到 {len(options)} 个td选项")
            
            for j, option in enumerate(options, 1):
                option_text = option.text.strip()
                print(f"    选项{j}: '{option_text}'")
                
                # 检查是否有单选按钮
                radios = option.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                if radios:
                    print(f"      找到 {len(radios)} 个单选按钮")
                    for radio in radios:
                        print(f"        radio id: {radio.get_attribute('id')}, name: {radio.get_attribute('name')}")
        
        # 保持浏览器打开供检查
        print("\n浏览器将保持打开30秒供您手动检查...")
        time.sleep(30)
        
        driver.quit()
        print("调试完成！")
        
    except Exception as e:
        print(f"调试出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_q20_structure()