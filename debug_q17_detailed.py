#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门调试第17题的结构
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置Chrome选项
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# 启动浏览器
print("🚀 启动Chrome浏览器...")
driver = webdriver.Chrome(options=chrome_options)

try:
    # 打开问卷页面
    url = "https://v.wjx.cn/vm/h9RwweO.aspx#"
    print(f"📱 打开问卷页面: {url}")
    driver.get(url)
    time.sleep(3)
    
    # 等待页面加载
    wait = WebDriverWait(driver, 10)
    
    # 先处理前面的题目到达第17题
    print("⏩ 快速处理前16题到达第17题...")
    
    # 第1题 填空题
    try:
        driver.find_element(By.ID, "q1").send_keys("测试答案")
        print("✅ 第1题完成")
    except:
        print("❌ 第1题失败")
    
    # 第2题 单选题（选第一个）
    try:
        driver.find_element(By.CSS_SELECTOR, "#div2 .ui-radio").click()
        print("✅ 第2题完成")
    except:
        print("❌ 第2题失败")
    
    # 第3题 下拉选择
    try:
        driver.find_element(By.ID, "q3").click()
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "#q3 option:nth-child(2)").click()
        print("✅ 第3题完成")
    except:
        print("❌ 第3题失败")
    
    # 第4-15题 单选题（都选第一个）
    for i in range(4, 16):
        try:
            driver.find_element(By.CSS_SELECTOR, f"#div{i} .ui-radio").click()
            print(f"✅ 第{i}题完成")
        except:
            print(f"❌ 第{i}题失败")
    
    # 第16题跳过
    print("⏭️  第16题跳过")
    
    # 现在到达第17题
    print("\n🔍 开始详细检查第17题...")
    
    # 检查第17题容器
    try:
        div17 = driver.find_element(By.ID, "div17")
        print("✅ 找到第17题容器: div17")
        
        # 检查页面结构
        print("\n📋 第17题详细结构分析:")
        
        # 检查所有的子div
        sub_divs = div17.find_elements(By.CSS_SELECTOR, "div[id^='drv17_']")
        print(f"📊 找到 {len(sub_divs)} 个 drv17_x div:")
        
        for i, div in enumerate(sub_divs):
            div_id = div.get_attribute("id")
            print(f"\n🔍 检查 {div_id}:")
            
            # 检查这个div下的所有input元素
            inputs = div.find_elements(By.CSS_SELECTOR, "input")
            print(f"   找到 {len(inputs)} 个input元素:")
            
            for j, input_elem in enumerate(inputs):
                input_id = input_elem.get_attribute("id")
                input_type = input_elem.get_attribute("type")
                input_class = input_elem.get_attribute("class")
                input_value = input_elem.get_attribute("value")
                is_displayed = input_elem.is_displayed()
                is_enabled = input_elem.is_enabled()
                
                print(f"     input[{j}]: id={input_id}, type={input_type}, class={input_class}")
                print(f"               value='{input_value}', displayed={is_displayed}, enabled={is_enabled}")
                
                # 尝试用JavaScript获取更多信息
                js_info = driver.execute_script("""
                    var input = arguments[0];
                    return {
                        outerHTML: input.outerHTML,
                        parentElement: input.parentElement ? input.parentElement.tagName + (input.parentElement.id ? '#' + input.parentElement.id : '') : null,
                        grandParent: input.parentElement && input.parentElement.parentElement ? input.parentElement.parentElement.tagName + (input.parentElement.parentElement.id ? '#' + input.parentElement.parentElement.id : '') : null
                    };
                """, input_elem)
                
                print(f"               outerHTML: {js_info['outerHTML']}")
                print(f"               parent: {js_info['parentElement']}, grandParent: {js_info['grandParent']}")
        
        # 尝试手动输入值进行测试
        print(f"\n🧪 尝试手动输入值进行测试...")
        for i in range(1, 5):  # 假设有4个输入框
            try:
                drv_div = driver.find_element(By.CSS_SELECTOR, f"#drv17_{i}")
                input_elem = drv_div.find_element(By.CSS_SELECTOR, "input[type='text']")
                
                input_id = input_elem.get_attribute("id")
                print(f"\n📝 测试输入到 {input_id}:")
                
                # 方法1: 直接send_keys
                try:
                    input_elem.clear()
                    input_elem.send_keys(str(i * 20))
                    time.sleep(0.5)
                    current_value = input_elem.get_attribute("value")
                    print(f"   ✅ send_keys成功，当前值: {current_value}")
                except Exception as e:
                    print(f"   ❌ send_keys失败: {e}")
                
                # 方法2: JavaScript设置
                try:
                    driver.execute_script(f"""
                        var input = document.getElementById('{input_id}');
                        if (input) {{
                            input.value = '{i * 25}';
                            // 触发事件
                            input.dispatchEvent(new Event('input', {{bubbles: true}}));
                            input.dispatchEvent(new Event('change', {{bubbles: true}}));
                            console.log('JavaScript设置值成功');
                        }}
                    """)
                    time.sleep(0.5)
                    current_value = input_elem.get_attribute("value")
                    print(f"   ✅ JavaScript设置成功，当前值: {current_value}")
                except Exception as e:
                    print(f"   ❌ JavaScript设置失败: {e}")
                
            except Exception as e:
                print(f"   ❌ 第{i}个输入框处理失败: {e}")
        
        # 检查是否有滑块相关元素
        print(f"\n🔍 检查滑块相关元素:")
        rangesliders = div17.find_elements(By.CLASS_NAME, "rangeslider")
        print(f"   找到 {len(rangesliders)} 个rangeslider元素")
        
        for i, rs in enumerate(rangesliders):
            rs_id = rs.get_attribute("id")
            print(f"   rangeslider[{i}]: id={rs_id}")
        
        # 检查是否有其他隐藏输入
        all_inputs = div17.find_elements(By.CSS_SELECTOR, "input[type='text']")
        print(f"\n📊 div17内所有文本输入框: {len(all_inputs)} 个")
        for i, inp in enumerate(all_inputs):
            inp_id = inp.get_attribute("id")
            inp_class = inp.get_attribute("class")
            print(f"   input[{i}]: id={inp_id}, class={inp_class}")
        
    except Exception as e:
        print(f"❌ 检查第17题失败: {e}")
    
    print("\n✅ 调试完成，浏览器保持打开状态供检查...")
    input("按回车键关闭浏览器...")
    
except Exception as e:
    print(f"❌ 发生错误: {e}")
    
finally:
    driver.quit()
    print("浏览器已关闭")