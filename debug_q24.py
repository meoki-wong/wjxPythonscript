#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 启动浏览器
driver = webdriver.Chrome()
driver.get("https://v.wjx.cn/vm/h9RwweO.aspx")
time.sleep(3)

# 检测第24题结构
print("=== 检测第24题矩阵结构 ===")

# 检测子问题数量
xpath1 = '//*[@id="divRefTab24"]/tbody/tr'
a = driver.find_elements(By.XPATH, xpath1)
q_num = 0
for tr in a:
    if tr.get_attribute("rowindex") is not None:
        q_num += 1

print(f"子问题数量: {q_num}")

# 检测选项数量
xpath2 = '//*[@id="drv24_1"]/td'
b = driver.find_elements(By.XPATH, xpath2)
option_count = len(b)
actual_options = option_count - 1

print(f"总td数（含表头）: {option_count}")
print(f"实际选项数: {actual_options}")
print(f"选项范围: 2到{option_count}")

# 显示每个子问题的结构
for i in range(1, min(q_num+1, 6)):  # 显示前5个子问题
    print(f"\n子问题{i}:")
    try:
        # 检测每个子问题的选项
        sub_xpath = f'//*[@id="drv24_{i}"]/td'
        sub_tds = driver.find_elements(By.XPATH, sub_xpath)
        print(f"  选项td数量: {len(sub_tds)}")
        
        # 显示每个td的内容
        for j, td in enumerate(sub_tds, 1):
            text = td.text.strip()
            if text:
                print(f"  td{j}: '{text}'")
            else:
                # 检查是否有input或其他元素
                inputs = td.find_elements(By.TAG_NAME, "input")
                if inputs:
                    print(f"  td{j}: [可点击选项]")
                else:
                    print(f"  td{j}: [空]")
                    
    except Exception as e:
        print(f"  检测失败: {e}")

print("\n=== 分析完成 ===")
input("按回车键退出...")
driver.quit()