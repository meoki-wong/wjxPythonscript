#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门调试第17题滑块结构的脚本
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 设置浏览器选项
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

try:
    driver = webdriver.Chrome(options=chrome_options)
    print("✅ 成功连接到已打开的浏览器")
    
    # 等待页面加载
    time.sleep(1)
    
    print("\n" + "="*60)
    print("🔍 专门分析第17题滑块结构:")
    print("="*60)
    
    # 查找第17题容器
    q17_container = driver.find_element(By.ID, "div17")
    print(f"✅ 找到第17题容器")
    
    # 获取容器的完整HTML内容
    html_content = q17_container.get_attribute("outerHTML")
    print(f"📄 容器HTML内容:\n{html_content[:1000]}")
    
    print("\n" + "-"*50)
    print("🔍 查找所有输入元素:")
    
    # 查找所有输入元素
    all_inputs = q17_container.find_elements(By.TAG_NAME, "input")
    print(f"📊 找到 {len(all_inputs)} 个输入元素:")
    
    for i, input_elem in enumerate(all_inputs):
        input_id = input_elem.get_attribute("id")
        input_type = input_elem.get_attribute("type")
        input_class = input_elem.get_attribute("class")
        input_name = input_elem.get_attribute("name")
        input_value = input_elem.get_attribute("value")
        
        print(f"\n   {i+1}. 输入元素详细信息:")
        print(f"      ID: '{input_id}'")
        print(f"      类型: '{input_type}'")
        print(f"      类名: '{input_class}'")
        print(f"      名称: '{input_name}'")
        print(f"      当前值: '{input_value}'")
        print(f"      是否可见: {input_elem.is_displayed()}")
        print(f"      是否可用: {input_elem.is_enabled()}")
        
        # 尝试使用JavaScript获取更多信息
        try:
            js_info = driver.execute_script("""
                var elem = arguments[0];
                return {
                    tagName: elem.tagName,
                    attributes: elem.attributes.length,
                    parentId: elem.parentElement ? elem.parentElement.id : '无',
                    parentClass: elem.parentElement ? elem.parentElement.className : '无'
                };
            """, input_elem)
            print(f"      标签名: {js_info['tagName']}")
            print(f"      属性数量: {js_info['attributes']}")
            print(f"      父元素ID: '{js_info['parentId']}'")
            print(f"      父元素类名: '{js_info['parentClass']}'")
        except Exception as e:
            print(f"      JavaScript信息获取失败: {e}")
    
    print("\n" + "-"*50)
    print("🔍 查找滑块相关元素:")
    
    # 查找所有rangeslider元素
    rangesliders = q17_container.find_elements(By.CLASS_NAME, "rangeslider")
    print(f"📊 找到 {len(rangesliders)} 个rangeslider元素:")
    
    for i, slider in enumerate(rangesliders):
        slider_id = slider.get_attribute("id")
        print(f"   {i+1}. rangeslider ID: '{slider_id}'")
        
        # 查找相关的输入框
        if slider_id:
            related_input = slider_id.replace("jsrs_", "")
            try:
                input_elem = driver.find_element(By.ID, related_input)
                print(f"      关联输入框: '{related_input}' - 找到")
            except:
                print(f"      关联输入框: '{related_input}' - 未找到")
    
    print("\n" + "-"*50)
    print("🔍 尝试不同的交互方式:")
    
    # 尝试通过父元素查找输入框
    for i, rangeslider in enumerate(rangesliders):
        slider_id = rangeslider.get_attribute("id")
        if slider_id and slider_id.startswith("jsrs_"):
            expected_input_id = slider_id.replace("jsrs_", "")
            print(f"\n   尝试rangeslider {i+1}: {slider_id}")
            
            # 方法1: 直接查找输入框
            try:
                input_elem = driver.find_element(By.ID, expected_input_id)
                print(f"   ✅ 方法1成功: 找到输入框 '{expected_input_id}'")
                
                # 尝试设置值
                test_value = str((i + 1) * 20)
                driver.execute_script(f"""
                    document.getElementById('{expected_input_id}').value = '{test_value}';
                    document.getElementById('{expected_input_id}').dispatchEvent(new Event('change'));
                """)
                print(f"   ✅ 设置值成功: {test_value}")
                
            except Exception as e:
                print(f"   ❌ 方法1失败: {e}")
                
                # 方法2: 通过rangeslider的父元素查找输入框
                try:
                    parent = rangeslider.find_element(By.XPATH, "..")  # 父元素
                    inputs_in_parent = parent.find_elements(By.TAG_NAME, "input")
                    print(f"   父元素中找到 {len(inputs_in_parent)} 个输入框")
                    
                    for j, input_in_parent in enumerate(inputs_in_parent):
                        input_id = input_in_parent.get_attribute("id")
                        input_type = input_in_parent.get_attribute("type")
                        print(f"      输入框{j+1}: ID='{input_id}', 类型='{input_type}'")
                        
                        if input_type == "text":
                            test_value = str((i + 1) * 20)
                            driver.execute_script(f"""
                                arguments[0].value = '{test_value}';
                                arguments[0].dispatchEvent(new Event('change'));
                            """, input_in_parent)
                            print(f"      ✅ 设置输入框{j+1}值成功: {test_value}")
                            break
                            
                except Exception as e2:
                    print(f"   ❌ 方法2也失败: {e2}")
    
    print("\n✅ 调试完成！浏览器保持打开状态供您检查...")
    input("\n按回车键关闭浏览器...")
    
except Exception as e:
    print(f"❌ 发生错误: {str(e)}")
    import traceback
    traceback.print_exc()
    input("\n按回车键关闭浏览器...")
finally:
    try:
        driver.quit()
    except:
        pass