#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第17题滑块值总和是否为100
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
    print("\n🧪 测试第17题滑块处理（要求总和为100）...")
    result = handle_slider_question(driver, 17, 5)
    
    if result:
        print("✅ 第17题滑块处理成功！")
        
        # 验证总和是否为100
        print("\n🔍 验证5个值的总和:")
        total = 0
        values = []
        
        # 获取所有文本输入框
        container = driver.find_element(By.ID, "div17")
        slider_inputs = container.find_elements(By.CSS_SELECTOR, "input[type='text']")
        
        for i, input_elem in enumerate(slider_inputs[:5]):
            value = input_elem.get_attribute("value")
            if value:
                int_val = int(value)
                values.append(int_val)
                total += int_val
                print(f"   滑块{i+1}: {int_val}")
            else:
                values.append(0)
                print(f"   滑块{i+1}: 无值")
        
        print(f"\n📊 总和: {total}")
        print(f"📋 所有值: {values}")
        
        if total == 100:
            print("✅ 完美！总和正好是100！")
        else:
            print(f"❌ 错误！总和是{total}，不是100")
    else:
        print("❌ 第17题滑块处理失败")
    
    print("\n✅ 测试完成，浏览器保持打开状态供检查...")
    input("按回车键关闭浏览器...")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    
finally:
    driver.quit()
    print("浏览器已关闭")