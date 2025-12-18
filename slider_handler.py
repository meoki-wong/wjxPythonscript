#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
滑块题处理函数 - 基于JavaScript的解决方案
"""

import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def handle_slider_question(driver, question_num, sub_count):
    """
    处理滑块题的统一函数
    
    Args:
        driver: WebDriver实例
        question_num: 题号（17或19）
        sub_count: 子滑块数量
    """
    print(f"[调试] 处理第{question_num}题滑块（{sub_count}个子滑块）")
    
    try:
        # 获取题目容器
        container = driver.find_element(By.ID, f"div{question_num}")
        print(f"✅ 找到题目容器: div{question_num}")
        
        # 方法1: 查找独立的滑块输入框（适用于第19题）
        slider_inputs = container.find_elements(By.CSS_SELECTOR, "input[type='text'].ui-slider-input")
        print(f"📊 方法1: 找到 {len(slider_inputs)} 个独立滑块输入框")
        
        # 方法2: 查找q17_0, q17_1, q17_2, q17_3, q17_4等结构的输入框（适用于第17题）
        if len(slider_inputs) == 0:
            print("🔍 方法2: 查找q17_x结构的滑块输入框...")
            
            # 查找q17_0, q17_1, q17_2, q17_3, q17_4等结构
            q_inputs = []
            for i in range(sub_count):
                try:
                    input_id = f"q{question_num}_{i}"
                    print(f"   正在查找: {input_id}")
                    input_elem = container.find_element(By.ID, input_id)
                    print(f"   ✅ 找到输入框: {input_id}")
                    q_inputs.append(input_elem)
                    
                except Exception as e:
                    print(f"   ❌ 第{i}个未找到: {str(e)}")
            
            if q_inputs:
                slider_inputs = q_inputs
                print(f"✅ 使用q结构输入框: {len(slider_inputs)} 个")
            else:
                print("❌ 未找到q结构输入框")
        
        # 方法3: 通过rangeslider反向查找（备用方案）
        if len(slider_inputs) == 0:
            print("🔍 方法3: 通过rangeslider反向查找...")
            
            # 查找所有rangeslider元素
            rangesliders = container.find_elements(By.CLASS_NAME, "rangeslider")
            print(f"📊 找到 {len(rangesliders)} 个rangeslider元素")
            
            # 通过rangeslider ID推断输入框ID
            inferred_inputs = []
            for slider in rangesliders:
                slider_id = slider.get_attribute("id")
                if slider_id and slider_id.startswith("jsrs_"):
                    # 移除jsrs_前缀得到输入框ID
                    input_id = slider_id.replace("jsrs_", "")
                    try:
                        input_elem = driver.find_element(By.ID, input_id)
                        inferred_inputs.append(input_elem)
                        print(f"   ✅ 找到输入框: {input_id}")
                    except:
                        print(f"   ❌ 未找到输入框: {input_id}")
            
            # 如果找到了推断的输入框，使用它们
            if inferred_inputs:
                slider_inputs = inferred_inputs
                print(f"✅ 使用推断的输入框: {len(slider_inputs)} 个")
            else:
                # 最后尝试：查找容器内的所有文本输入框
                all_text_inputs = container.find_elements(By.CSS_SELECTOR, "input[type='text']")
                slider_inputs = [inp for inp in all_text_inputs if inp.is_displayed() or inp.get_attribute("class") and "slider" in inp.get_attribute("class")]
                print(f"✅ 使用所有文本输入框: {len(slider_inputs)} 个")
        
        if len(slider_inputs) != sub_count:
            print(f"⚠️  警告：预期{sub_count}个滑块，实际找到{len(slider_inputs)}个")
        
        # 为每个滑块设置值
        # 特殊处理第17题：5个值加起来必须是100
        if question_num == 17 and sub_count == 5:
            print(f"   第17题特殊处理：生成5个和为100的随机值")
            # 生成5个正整数，和为100
            values = []
            remaining = 100
            for i in range(4):  # 前4个值
                # 确保剩下的值足够分配给剩余的输入框（每个至少1）
                max_val = remaining - (4 - i)
                val = random.randint(1, max_val)
                values.append(val)
                remaining -= val
            values.append(remaining)  # 最后一个值
            
            # 打乱顺序，让分布更随机
            random.shuffle(values)
            print(f"   生成的值: {values}")
        else:
            # 其他题目正常随机生成
            values = [random.randint(1, 100) for _ in range(sub_count)]
            
        # 为每个滑块设置值
        for i, input_elem in enumerate(slider_inputs[:sub_count]):
            target_value = values[i]  # 使用预生成的值
            
            # 获取输入框的ID（如果存在）
            input_id = input_elem.get_attribute("id") if input_elem else None
            
            try:
                if input_id and input_id.strip() != "":
                    print(f"   设置滑块 {input_id} = {target_value}")
                    # 使用ID的JavaScript方法
                    script = f"""
                        var input = document.getElementById('{input_id}');
                        if (input) {{
                            input.value = '{target_value}';
                            // 触发change事件
                            var event = new Event('change', {{ bubbles: true }});
                            input.dispatchEvent(event);
                            
                            // 触发input事件
                            var inputEvent = new Event('input', {{ bubbles: true }});
                            input.dispatchEvent(inputEvent);
                            
                            console.log('设置值成功: ' + '{target_value}');
                            return true;
                        }}
                        return false;
                    """
                    result = driver.execute_script(script)
                else:
                    print(f"   设置第{i+1}个滑块 (无ID) = {target_value}")
                    # 使用元素引用的JavaScript方法
                    script = """
                        arguments[0].value = arguments[1];
                        // 触发change事件
                        var event = new Event('change', { bubbles: true });
                        arguments[0].dispatchEvent(event);
                        
                        // 触发input事件
                        var inputEvent = new Event('input', { bubbles: true });
                        arguments[0].dispatchEvent(inputEvent);
                        
                        console.log('设置值成功: ' + arguments[1]);
                        return true;
                    """
                    result = driver.execute_script(script, input_elem, str(target_value))
                
                if result:
                    # 等待一下让UI更新
                    time.sleep(0.3)
                    
                    # 验证设置是否成功
                    if input_id and input_id.strip() != "":
                        actual_value = driver.execute_script(f"return document.getElementById('{input_id}').value;")
                    else:
                        actual_value = driver.execute_script("return arguments[0].value;", input_elem)
                    print(f"   ✅ 设置成功，当前值: {actual_value}")
                else:
                    print(f"   ❌ 未找到输入元素")
                    
            except Exception as e:
                print(f"   ❌ JavaScript设置失败: {str(e)}")
                
                # 方法2: 尝试使用ActionChains拖拽滑块（仅当输入ID有效时）
                try:
                    # 查找对应的rangeslider元素
                    rangeslider_id = f"jsrs_{input_id}"
                    rangeslider = container.find_element(By.ID, rangeslider_id)
                    handle = rangeslider.find_element(By.CLASS_NAME, "rangeslider__handle")
                    
                    # 计算拖拽距离（假设滑块总宽度对应0-100的范围）
                    slider_width = rangeslider.size['width']
                    offset = int((target_value / 100.0) * slider_width - (slider_width / 2))
                    
                    print(f"   尝试拖拽滑块到位置: {offset}px")
                    
                    actions = ActionChains(driver)
                    actions.drag_and_drop_by_offset(handle, offset, 0).perform()
                    
                    time.sleep(0.3)
                    print(f"   ✅ 拖拽成功")
                    
                except Exception as e2:
                    print(f"   ❌ 拖拽也失败: {str(e2)}")
                    # 最后尝试直接点击滑条
                    try:
                        if 'rangeslider' in locals():
                            rangeslider.click()
                            print(f"   ✅ 点击滑条成功")
                        else:
                            print(f"   ❌ 无法获取滑条元素")
                    except:
                        print(f"   ❌ 所有方法都失败")
        
        print(f"✅ 第{question_num}题滑块设置完成")
        return True
        
    except Exception as e:
        print(f"❌ 处理第{question_num}题滑块失败: {str(e)}")
        return False

# 测试函数
def test_slider_handling():
    """测试滑块处理函数"""
    print("🧪 滑块处理函数已加载")
    print("💡 使用方式:")
    print("   handle_slider_question(driver, 17, 5)  # 处理第17题，5个子滑块")
    print("   handle_slider_question(driver, 19, 2)  # 处理第19题，2个子滑块")

if __name__ == "__main__":
    test_slider_handling()