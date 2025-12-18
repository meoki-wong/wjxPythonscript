#!/usr/bin/env python3
"""
调试脚本 - 用于分析问卷页面结构
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

def analyze_survey_structure():
    """分析问卷页面结构"""
    print("🚀 启动浏览器分析问卷结构...")
    
    # 启动浏览器
    driver = webdriver.Chrome()
    driver.set_window_size(1200, 800)
    
    try:
        # 打开问卷页面
        url = "https://v.wjx.cn/vm/h9RwweO.aspx"
        print(f"📄 打开问卷: {url}")
        driver.get(url)
        
        # 等待页面加载
        time.sleep(3)
        
        print(f"📋 页面标题: {driver.title}")
        print(f"🔗 当前URL: {driver.current_url}")
        
        # 分析页面结构
        print("\n🔍 分析页面元素结构...")
        
        # 查找所有题目相关的元素
        print("\n1️⃣ 查找所有ID包含数字的元素:")
        elements = driver.find_elements(By.XPATH, "//*[contains(@id, 'q') or contains(@id, 'Q')]")
        for elem in elements[:20]:  # 只显示前20个
            print(f"   ID: {elem.get_attribute('id')}, 标签: {elem.tag_name}, 类型: {elem.get_attribute('type')}")
        
        print("\n2️⃣ 查找所有class包含'question'或'topic'的元素:")
        question_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'question') or contains(@class, 'topic') or contains(@class, 'div')]")
        for elem in question_elements[:15]:
            print(f"   Class: {elem.get_attribute('class')}, ID: {elem.get_attribute('id')}, 文本: {elem.text[:50]}...")
        
        print("\n3️⃣ 查找所有输入框元素:")
        input_elements = driver.find_elements(By.TAG_NAME, "input")
        for elem in input_elements:
            print(f"   输入框 - ID: {elem.get_attribute('id')}, 类型: {elem.get_attribute('type')}, 名称: {elem.get_attribute('name')}")
        
        print("\n4️⃣ 查找所有滑块相关元素:")
        slider_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'slider') or contains(@id, 'slide') or @type='range']")
        for elem in slider_elements:
            print(f"   滑块 - ID: {elem.get_attribute('id')}, Class: {elem.get_attribute('class')}, 类型: {elem.get_attribute('type')}")
        
        print("\n5️⃣ 查找第17题附近的元素:")
        # 尝试查找第17题相关的各种可能元素
        for i in range(15, 20):
            # 检查不同的可能ID格式
            possible_ids = [f"q{i}", f"Q{i}", f"question{i}", f"div{i}", f"topic{i}"]
            for pid in possible_ids:
                elements = driver.find_elements(By.ID, pid)
                if elements:
                    print(f"   找到第{i}题元素 - ID: {pid}, 标签: {elements[0].tag_name}")
                    # 查找该元素内的输入框
                    inputs = elements[0].find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        print(f"     └─ 输入框: ID={inp.get_attribute('id')}, 类型={inp.get_attribute('type')}")
        
        print("\n6️⃣ 查找所有数字相关的div:")
        # 查找所有div元素，看看是否有数字相关的
        divs = driver.find_elements(By.TAG_NAME, "div")
        number_divs = []
        for div in divs:
            div_id = div.get_attribute('id')
            if div_id and any(char.isdigit() for char in div_id):
                number_divs.append(div_id)
        
        print(f"   找到{len(number_divs)}个包含数字的div元素，前10个:")
        for div_id in number_divs[:10]:
            print(f"   Div ID: {div_id}")
        
        print("\n✅ 分析完成！浏览器保持打开状态供您检查...")
        print("💡 提示：")
        print("   - 按F12打开开发者工具")
        print("   - 使用元素选择器点击页面上的题目")
        print("   - 查看实际的HTML结构和元素ID")
        print("   - 手动关闭浏览器结束调试")
        
        # 保持浏览器打开
        input("\n按回车键关闭浏览器...")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        input("按回车键关闭浏览器...")
    finally:
        driver.quit()

if __name__ == "__main__":
    analyze_survey_structure()