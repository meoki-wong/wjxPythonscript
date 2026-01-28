#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行问卷脚本 - 简化版本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入必要的模块
import random
import time
import numpy
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_simple_run():
    """简化测试运行"""
    print("开始测试问卷自动化脚本...")
    
    # 设置Chrome选项
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    
    try:
        # 创建WebDriver实例
        print("正在启动Chrome浏览器...")
        driver = webdriver.Chrome(options=option)
        driver.set_window_size(1200, 800)
        
        # 设置问卷URL
        url = "https://v.wjx.cn/vm/h9RwweO.aspx#"
        print(f"正在打开问卷页面: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(5)
        
        print(f"页面标题: {driver.title}")
        print(f"当前URL: {driver.current_url}")
        
        # 检查页面是否加载成功
        if "问卷星" in driver.title or "问卷" in driver.title:
            print("✅ 问卷页面加载成功！")
            
            # 简单测试：检查是否存在问题元素
            try:
                # 检查第一题
                q1_elements = driver.find_elements(By.CSS_SELECTOR, "#q1")
                if q1_elements:
                    print("✅ 找到第1题元素")
                else:
                    print("⚠️ 未找到第1题元素")
                
                # 检查页面结构
                page_elements = driver.find_elements(By.XPATH, '//*[@id="divQuestion"]/fieldset')
                print(f"检测到 {len(page_elements)} 页问题")
                
                # 保持浏览器打开一段时间供查看
                print("浏览器将保持打开30秒供您检查...")
                time.sleep(30)
                
            except Exception as e:
                print(f"检查页面元素时出错: {str(e)}")
                
        else:
            print("⚠️ 页面标题不包含问卷相关信息，请检查URL是否正确")
            
        driver.quit()
        print("测试完成！")
        
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple_run()