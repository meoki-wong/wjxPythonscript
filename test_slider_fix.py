#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试更新后的滑块处理函数
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from slider_handler import handle_slider_question

# 启动浏览器
print("🚀 启动Chrome浏览器...")
driver = webdriver.Chrome()

try:
    # 打开问卷页面
    url = "https://v.wjx.cn/vm/h9RwweO.aspx#"
    print(f"📱 打开问卷页面: {url}")
    driver.get(url)
    time.sleep(3)
    
    # 快速处理前16题到达第17题
    print("⏩ 快速处理前16题到达第17题...")
    
    # 这里简化处理，只处理必要的题目
    try:
        driver.find_element(By.ID, "q1").send_keys("测试")
        driver.find_element(By.CSS_SELECTOR, "#div2 .ui-radio").click()
        # 简化的其他题目处理...
    except:
        pass
    
    # 现在测试第17题
    print("\n🧪 测试第17题滑块处理...")
    result = handle_slider_question(driver, 17, 5)
    
    if result:
        print("✅ 第17题滑块处理成功！")
        
        # 验证输入的值
        print("\n🔍 验证输入的值:")
        for i in range(5):
            try:
                input_elem = driver.find_element(By.ID, f"q17_{i}")
                value = input_elem.get_attribute("value")
                print(f"   q17_{i}: '{value}'")
            except:
                print(f"   q17_{i}: 无法找到或获取值")
    else:
        print("❌ 第17题滑块处理失败")
    
    print("\n✅ 测试完成，浏览器保持打开状态供检查...")
    input("按回车键关闭浏览器...")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    
finally:
    driver.quit()
    print("浏览器已关闭")