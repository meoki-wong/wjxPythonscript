#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第16题的显示格式
"""

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_q16_format():
    """测试第16题的显示格式"""
    print("正在测试第16题的显示格式...")
    
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
        
        # 先处理前面的题目直到第6题
        print("\n=== 处理前面的题目 ===")
        
        # 第1题：出生年份
        print("处理第1题...")
        years = [2001, 2002, 2003] * 12 + [2004, 2005, 2006, 2007] * 70 + [2008, 2009, 2010] * 18
        year = random.choice(years)
        driver.find_element(By.CSS_SELECTOR, "#q1").send_keys(str(year))
        time.sleep(0.5)
        
        # 第2题：性别
        print("处理第2题...")
        genders = ["男"] * 40 + ["女"] * 60  # 女生60%，男生40%
        gender = random.choice(genders)
        if gender == "男":
            driver.find_element(By.CSS_SELECTOR, "#div2 > div.ui-controlgroup > div:nth-child(2)").click()
        else:
            driver.find_element(By.CSS_SELECTOR, "#div2 > div.ui-controlgroup > div:nth-child(1)").click()
        time.sleep(0.5)
        
        # 第3题：省份（简化处理）
        print("处理第3题...")
        provinces = ["北京", "上海", "广东", "江苏", "浙江", "山东", "河南", "四川", "湖北", "湖南"]
        province = random.choice(provinces)
        driver.find_element(By.CSS_SELECTOR, "#q3").send_keys(province)
        time.sleep(0.5)
        
        # 第4题：高考成绩
        print("处理第4题...")
        scores = ["A"] * 5 + ["B"] * 30 + ["C"] * 35 + ["D"] * 30
        score = random.choice(scores)
        if score == "A":
            driver.find_element(By.CSS_SELECTOR, "#div4 > div.ui-controlgroup > div:nth-child(1)").click()
        elif score == "B":
            driver.find_element(By.CSS_SELECTOR, "#div4 > div.ui-controlgroup > div:nth-child(2)").click()
        elif score == "C":
            driver.find_element(By.CSS_SELECTOR, "#div4 > div.ui-controlgroup > div:nth-child(3)").click()
        else:
            driver.find_element(By.CSS_SELECTOR, "#div4 > div.ui-controlgroup > div:nth-child(4)").click()
        time.sleep(0.5)
        
        # 第5题：高校类型
        print("处理第5题...")
        types = ["A"] * 4 + ["B"] * 16 + ["C"] * 65 + ["D"] * 15
        school_type = random.choice(types)
        if school_type == "A":
            driver.find_element(By.CSS_SELECTOR, "#div5 > div.ui-controlgroup > div:nth-child(1)").click()
        elif school_type == "B":
            driver.find_element(By.CSS_SELECTOR, "#div5 > div.ui-controlgroup > div:nth-child(2)").click()
        elif school_type == "C":
            driver.find_element(By.CSS_SELECTOR, "#div5 > div.ui-controlgroup > div:nth-child(3)").click()
        else:
            driver.find_element(By.CSS_SELECTOR, "#div5 > div.ui-controlgroup > div:nth-child(4)").click()
        time.sleep(0.5)
        
        # 第6题：专业类型（选择一个用于测试）
        print("处理第6题...")
        majors = ["文史类", "理工类", "艺术类", "医学类"]
        major = random.choice(majors)
        
        if major == "文史类":
            driver.find_element(By.CSS_SELECTOR, "#div6 > div.ui-controlgroup > div:nth-child(1)").click()
        elif major == "理工类":
            driver.find_element(By.CSS_SELECTOR, "#div6 > div.ui-controlgroup > div:nth-child(2)").click()
        elif major == "艺术类":
            driver.find_element(By.CSS_SELECTOR, "#div6 > div.ui-controlgroup > div:nth-child(3)").click()
        else:
            driver.find_element(By.CSS_SELECTOR, "#div6 > div.ui-controlgroup > div:nth-child(4)").click()
        time.sleep(0.5)
        
        print(f"选择的第6题专业: {major}")
        
        # 现在测试第16题
        print("\n=== 测试第16题格式 ===")
        
        # 滚动到第16题
        q16_element = driver.find_element(By.CSS_SELECTOR, "#div16")
        driver.execute_script("arguments[0].scrollIntoView(true);", q16_element)
        time.sleep(1)
        
        # 获取所有子问题
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
                print(f"找到子问题{i}: input={q_elem.get_attribute('id')}")
                
                # 显示当前的span内容
                current_span_text = span_elem.text.strip()
                print(f"  当前span.textCont内容: '{current_span_text}'")
                
                i += 1
            except Exception as e:
                break
        
        print(f"\n共找到{len(sub_questions)}个子问题")
        
        # 根据专业类型确定学费范围
        def get_tuition_range(major_type):
            """根据专业类型返回学费范围"""
            if major_type == "文史类":
                return (4000, 6000)
            elif major_type == "理工类":
                return (5000, 8000)
            elif major_type == "艺术类":
                return (8000, 15000)
            elif major_type == "医学类":
                return (6000, 10000)
            else:
                return (4000, 6000)  # 默认
        
        min_fee, max_fee = get_tuition_range(major)
        print(f"专业'{major}'对应的学费范围：{min_fee}-{max_fee}元/年")
        
        # 为每个子问题设置学费值
        for i, sub_q in enumerate(sub_questions):
            # 生成随机学费（整数，整百数）
            tuition_fee = random.randint(min_fee // 100, max_fee // 100) * 100
            
            # 生成显示文本
            display_text = f"学费：{tuition_fee}元/年"
            
            print(f"\n子问题{i+1}:")
            print(f"  设置span.textCont: '{display_text}'")
            print(f"  设置input值: {tuition_fee}")
            
            # 设置span.textCont的值（显示给用户看）
            driver.execute_script("arguments[0].textContent = arguments[1];", sub_q['span_elem'], display_text)
            
            # 设置input框的值（实际提交的值）
            driver.execute_script("arguments[0].value = arguments[1];", sub_q['input_elem'], str(tuition_fee))
            
            # 触发input框的事件
            driver.execute_script("""
                var input = arguments[0];
                input.dispatchEvent(new Event('input', {bubbles: true}));
                input.dispatchEvent(new Event('change', {bubbles: true}));
            """, sub_q['input_elem'])
            
            time.sleep(0.5)
            
            # 验证设置结果
            new_span_text = sub_q['span_elem'].text.strip()
            new_input_value = sub_q['input_elem'].get_attribute('value')
            print(f"  验证结果 - span.textCont: '{new_span_text}', input值: '{new_input_value}'")
        
        print("\n✅ 第16题格式测试完成")
        
        # 保持浏览器打开一段时间供观察
        print("\n浏览器将保持打开30秒供您检查...")
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        
    finally:
        driver.quit()
        print("测试完成！")

if __name__ == "__main__":
    test_q16_format()