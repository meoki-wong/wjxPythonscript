#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第16题特殊矩阵结构处理
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By

# 启动浏览器
print("🚀 启动Chrome浏览器...")
driver = webdriver.Chrome()

try:
    # 打开问卷页面
    url = "https://v.wjx.cn/vm/h9RwweO.aspx#"
    print(f"📱 打开问卷页面: {url}")
    driver.get(url)
    time.sleep(3)
    
    # 快速处理前15题到达第16题
    print("⏩ 快速处理前15题到达第16题...")
    
    # 简化处理前15题
    try:
        # 第1题：填空题
        driver.find_element(By.ID, "q1").send_keys("测试")
        
        # 第2题：单选题
        driver.find_element(By.CSS_SELECTOR, "#div2 .ui-radio").click()
        
        # 第3题：下拉框
        driver.find_element(By.CSS_SELECTOR, "#select2-q3-container").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//*[@id='select2-q3-results']/li[2]").click()
        
        # 第4-15题：单选题（简化处理）
        for i in range(4, 16):
            try:
                driver.find_element(By.CSS_SELECTOR, f"#div{i} .ui-radio").click()
                time.sleep(0.2)
            except:
                pass
        
    except Exception as e:
        print(f"前15题处理警告: {str(e)}")
    
    # 现在测试第16题
    print("\n🧪 测试第16题特殊矩阵结构...")
    
    # 手动实现第16题处理逻辑
    try:
        print(f"[调试] 处理第16题特殊矩阵结构...")
        
        # 获取所有子问题（q16_1, q16_2等）
        sub_questions = []
        i = 1
        while True:
            try:
                q_elem = driver.find_element(By.ID, f"q16_{i}")
                label_elem = driver.find_element(By.CSS_SELECTOR, f"#q16_{i} + label")
                span_elem = label_elem.find_element(By.CSS_SELECTOR, "span.textCont")
                
                sub_questions.append({
                    'input_id': f"q16_{i}",
                    'input_elem': q_elem,
                    'label_elem': label_elem,
                    'span_elem': span_elem
                })
                print(f"[调试] 找到子问题{i}: input={q_elem.get_attribute('id')}, span.textCont存在")
                i += 1
            except:
                break
        
        print(f"[调试] 共找到{len(sub_questions)}个子问题")
        
        if len(sub_questions) == 0:
            print("❌ 未找到第16题的子问题")
        else:
            # 为每个子问题设置值
            for i, sub_q in enumerate(sub_questions):
                # 生成随机文本
                random_text = f"选项{i+1}_{random.randint(1, 100)}"
                random_value = str(random.randint(1, 5))
                
                # 设置span.textCont的值
                driver.execute_script("arguments[0].textContent = arguments[1];", sub_q['span_elem'], random_text)
                print(f"[调试] 设置span.textCont: {random_text}")
                
                # 设置input框的值
                driver.execute_script("arguments[0].value = arguments[1];", sub_q['input_elem'], random_value)
                print(f"[调试] 设置input值: {random_value}")
                
                # 触发input框的事件
                driver.execute_script("""
                    var input = arguments[0];
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                    input.dispatchEvent(new Event('change', {bubbles: true}));
                """, sub_q['input_elem'])
                
                time.sleep(0.2)
            
            print("✅ 第16题特殊矩阵处理完成")
            
            # 验证设置结果
            print("\n🔍 验证第16题设置结果:")
            for i, sub_q in enumerate(sub_questions):
                span_text = driver.execute_script("return arguments[0].textContent;", sub_q['span_elem'])
                input_val = driver.execute_script("return arguments[0].value;", sub_q['input_elem'])
                print(f"   子问题{i+1}: span.textCont='{span_text}', input.value='{input_val}'")
        
    except Exception as e:
        print(f"❌ 第16题特殊矩阵处理失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n✅ 测试完成，浏览器保持打开状态供检查...")
    input("按回车键关闭浏览器...")
    
except Exception as e:
    print(f"❌ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
    print("浏览器已关闭")