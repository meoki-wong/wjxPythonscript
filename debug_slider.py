#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试滑块题交互方式的专用脚本
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置浏览器选项
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=chrome_options)
except Exception as e:
    print(f"❌ 无法连接到浏览器: {str(e)}")
    print("请确保浏览器已打开并连接到调试端口")
    exit(1)
    print("✅ 成功连接到已打开的浏览器")
    print(f"📄 当前页面标题: {driver.title}")
    print(f"🔗 当前URL: {driver.current_url}")
    
    # 等待页面加载
    time.sleep(2)
    
    # 分析第17题的滑块结构
    print("\n" + "="*60)
    print("🔍 分析第17题滑块结构:")
    print("="*60)
    
    # 查找第17题容器
    q17_container = driver.find_element(By.ID, "div17")
    print(f"✅ 找到第17题容器: div17")
    
    # 查找所有相关的滑块元素
    slider_inputs = q17_container.find_elements(By.CSS_SELECTOR, "input[type='text'].ui-slider-input")
    print(f"📊 找到 {len(slider_inputs)} 个滑块输入框:")
    
    for i, input_elem in enumerate(slider_inputs):
        input_id = input_elem.get_attribute("id")
        input_value = input_elem.get_attribute("value")
        print(f"   {i+1}. 输入框 ID: {input_id}, 当前值: {input_value}")
        
        # 查找对应的rangeslider元素
        rangeslider = q17_container.find_element(By.ID, f"jsrs_{input_id}")
        print(f"      对应滑块: {rangeslider.tag_name}, 类名: {rangeslider.get_attribute('class')}")
        
        # 查找滑块手柄
        handle = rangeslider.find_element(By.CLASS_NAME, "rangeslider__handle")
        print(f"      滑块手柄: 位置信息 - {handle.location}")
        
        # 查找滑块填充条
        fill = rangeslider.find_element(By.CLASS_NAME, "rangeslider__fill")
        print(f"      滑块填充: 宽度 - {fill.size['width']}px")
        
        print()
    
    # 测试不同的交互方式
    print("🧪 测试交互方式:")
    
    # 方法1: 直接设置输入框值（使用JavaScript）
    print("\n方法1: 使用JavaScript设置输入框值")
    for i, input_elem in enumerate(slider_inputs):
        input_id = input_elem.get_attribute("id")
        test_value = str((i + 1) * 20)  # 20, 40, 60, 80, 100
        
        print(f"   设置 {input_id} = {test_value}")
        driver.execute_script(f"document.getElementById('{input_id}').value = '{test_value}';")
        
        # 触发change事件
        driver.execute_script(f"document.getElementById('{input_id}').dispatchEvent(new Event('change'));")
        time.sleep(0.5)
    
    # 方法2: 使用ActionChains拖拽滑块
    print("\n方法2: 使用ActionChains拖拽滑块")
    for i, input_elem in enumerate(slider_inputs):
        input_id = input_elem.get_attribute("id")
        
        # 获取对应的rangeslider和handle
        rangeslider = q17_container.find_element(By.ID, f"jsrs_{input_id}")
        handle = rangeslider.find_element(By.CLASS_NAME, "rangeslider__handle")
        
        # 计算目标位置（假设滑块宽度为200px，范围1-100）
        target_value = (i + 1) * 20
        offset = int((target_value - 1) * 2)  # 粗略计算
        
        print(f"   拖拽 {input_id} 到位置 {target_value} (偏移: {offset}px)")
        
        try:
            actions = ActionChains(driver)
            actions.drag_and_drop_by_offset(handle, offset, 0).perform()
            time.sleep(0.5)
            print(f"   ✅ 拖拽成功")
        except Exception as e:
            print(f"   ❌ 拖拽失败: {str(e)}")
    
    # 分析第19题
    print("\n" + "="*60)
    print("🔍 分析第19题滑块结构:")
    print("="*60)
    
    q19_container = driver.find_element(By.ID, "div19")
    print(f"✅ 找到第19题容器: div19")
    
    q19_inputs = q19_container.find_elements(By.CSS_SELECTOR, "input[type='text'].ui-slider-input")
    print(f"📊 找到 {len(q19_inputs)} 个滑块输入框:")
    
    for i, input_elem in enumerate(q19_inputs):
        input_id = input_elem.get_attribute("id")
        print(f"   {i+1}. 输入框 ID: {input_id}")
    
    print("\n✅ 调试完成！浏览器保持打开状态供您检查...")
    print("💡 提示：按F12打开开发者工具，手动测试滑块交互")
    
    # 保持浏览器打开
    input("\n按回车键关闭浏览器...")
    
except Exception as e:
    print(f"❌ 发生错误: {str(e)}")
    import traceback
    traceback.print_exc()
    
    # 保持浏览器打开以便调试
    input("\n按回车键关闭浏览器...")
finally:
    try:
        driver.quit()
    except:
        pass
        pass