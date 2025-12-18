import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

class WJXAutoFill:
    def __init__(self):
        # 初始化浏览器
        self.driver = webdriver.Chrome()  # 使用Chrome浏览器，确保已安装ChromeDriver
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.ccc = 0  # 题块计数器
        self.xiala_index = 0  # 下拉框计数器
        
    def clear_cookie(self):
        """清除浏览器Cookie"""
        self.driver.delete_all_cookies()
        print("Cookie已清除")
    
    def open_questionnaire(self, url):
        """打开问卷URL"""
        self.driver.get(url)
        time.sleep(2)  # 等待页面加载
    
    def check_url(self, wenjuan_url):
        """检查当前URL，处理完成页面跳转"""
        current_url = self.driver.current_url
        if "https://www.wjx.cn/wjx/join/complete.aspx" in current_url:
            self.driver.get(wenjuan_url)
            time.sleep(2)
    
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
    
    def danxuan(self, bili):
        """根据比例随机选择选项"""
        rand = random.random() * 100
        total = 0
        for i, percent in enumerate(bili):
            total += percent
            if rand < total:
                return i
        return len(bili) - 1
    
    def xiala_click(self, element):
        """点击下拉框"""
        ActionChains(self.driver).click(element).perform()
        time.sleep(1)
    
    def xialaElement_click(self, element):
        """点击下拉框选项"""
        ActionChains(self.driver).click(element).perform()
        time.sleep(1)
    
    def random_bili(self, count):
        """生成随机比例"""
        if count <= 0:
            return [100]
        
        bili = [random.randint(1, 100) for _ in range(count)]
        total = sum(bili)
        return [round((b / total) * 100) for b in bili]
    
    def get_birth_year(self):
        """获取出生年份"""
        rand = random.random() * 100
        if rand < 70:
            return str(random.randint(2004, 2007))
        elif rand < 82:
            return str(random.randint(2001, 2003))
        else:
            return str(random.randint(2008, 2010))
    
    def get_tuition_fee(self):
        """获取学费"""
        rand = random.random()
        if rand < 0.3:
            return str(random.randint(40, 60) * 100)
        elif rand < 0.6:
            return str(random.randint(50, 80) * 100)
        elif rand < 0.8:
            return str(random.randint(80, 150) * 100)
        elif rand < 0.9:
            return str(random.randint(55, 70) * 100)
        else:
            return str(random.randint(35, 50) * 100)
    
    def get_accommodation_fee(self):
        """获取住宿费"""
        if random.random() < 0.9:
            return str(random.randint(8, 15) * 100)
        else:
            return str(random.randint(15, 20) * 100)
    
    def get_living_expenses(self):
        """获取生活费"""
        rand = random.random() * 100
        if rand < 15:
            return str(random.randint(1301, 1500))
        elif rand < 60:
            return str(random.randint(1500, 2000))
        elif rand < 90:
            return str(random.randint(2000, 3000))
        elif rand < 95:
            return str(random.randint(3000, 4000))
        else:
            return str(random.randint(800, 1300))
    
    def fill_questionnaire(self):
        """填写问卷"""
        try:
            # 1. 出生年份
            birth_year = self.get_birth_year()
            q1_input = self.driver.find_element(By.ID, "q1")
            q1_input.clear()
            q1_input.send_keys(birth_year)
            print(f"已填写出生年份: {birth_year}")
            
            # 获取题块列表
            lists = self.driver.find_elements(By.CLASS_NAME, "ui-controlgroup")
            
            # 2. 性别 - 男生41%，女生59%
            ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
            self.ccc += 1
            bili = [41, 59]
            ops[self.danxuan(bili)].click()
            print("已填写性别")
            
            # 3. 下拉框题
            select2_elements = self.driver.find_elements(By.CLASS_NAME, "select2-selection.select2-selection--single")
            if len(select2_elements) > self.xiala_index:
                self.xiala_click(select2_elements[self.xiala_index])
                self.xiala_index += 1
                
                # 获取下拉选项
                ops = self.driver.find_elements(By.CSS_SELECTOR, "#select2-q3-results li")
                ops = ops[1:]  # 跳过第一个空选项
                bili = self.random_bili(len(ops) - 1)
                if ops:
                    self.xialaElement_click(ops[self.danxuan(bili)])
                    print("已填写下拉框题")
            
            # 4. 高考成绩 - A:5%, B:30%, C:35%, D:30%
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [5, 30, 35, 30]
                ops[self.danxuan(bili)].click()
                print("已填写高考成绩")
            
            # 5. 高校类型 - A:4%, B:16%, C:65%, D:15%
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [4, 16, 65, 15]
                ops[self.danxuan(bili)].click()
                print("已填写高校类型")
            
            # 6-8 单选题 (3个单选题)
            for i in range(6, 9):
                if self.ccc < len(lists):
                    ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                    self.ccc += 1
                    bili = self.random_bili(len(ops))
                    ops[self.danxuan(bili)].click()
                    print(f"已填写单选题 {i}")
            
            # 9 兄弟姐妹数量 - 1个60%，2个30%，3个8%，4个及以上2%
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [60, 30, 8, 2]
                if len(ops) > 0:
                    ops[self.danxuan(bili)].click()
                    print("已填写兄弟姐妹数量")
            
            # 10-11 单选题 (2个单选题 - 父母学历)
            for i in range(10, 12):
                if self.ccc < len(lists):
                    ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                    self.ccc += 1
                    bili = self.random_bili(len(ops))
                    ops[self.danxuan(bili)].click()
                    print(f"已填写单选题 {i}")
            
            # 12 父亲工作单位性质 - A:15%, B:25%, C:35%, D:25%
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [15, 25, 35, 25]
                ops[self.danxuan(bili)].click()
                print("已填写父亲工作单位性质")
            
            # 13 母亲工作单位性质 - A:15%, B:25%, C:35%, D:25%
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [15, 25, 35, 25]
                ops[self.danxuan(bili)].click()
                print("已填写母亲工作单位性质")
            
            # 14 家庭年总收入分布
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                # ①3万及以下7%，②3.1-6万18%，③④共30%，⑤⑥⑦共30%，⑧30.1-50万10%，⑨50万以上5%
                bili = [7, 18, 15, 15, 10, 10, 10, 10, 5]
                ops[self.danxuan(bili)].click()
                print("已填写家庭年总收入分布")
            
            # 15 家庭经济负担 - 随机分布
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = self.random_bili(len(ops))
                ops[self.danxuan(bili)].click()
                print("已填写家庭经济负担")
            
            # 16 填空题 - 学费、住宿费、生活费赋值
            try:
                # 等待元素加载
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "q16_1"))
                )
                
                # 学费赋值
                tuition = self.get_tuition_fee()
                q16_1_inputs = self.driver.find_element(By.ID, "q16_1")
                q16_1_inputs.clear()
                q16_1_inputs.send_keys(str(tuition))
                print(f"已填写学费: {tuition}")
                
                # 住宿费赋值
                accommodation = self.get_accommodation_fee()
                q16_2_inputs = self.driver.find_element(By.ID, "q16_2")
                q16_2_inputs.clear()
                q16_2_inputs.send_keys(str(accommodation))
                print(f"已填写住宿费: {accommodation}")
                
                # 生活费赋值
                living = self.get_living_expenses()
                q16_3_inputs = self.driver.find_element(By.ID, "q16_3")
                q16_3_inputs.clear()
                q16_3_inputs.send_keys(str(living))
                print(f"已填写生活费: {living}")
                
            except Exception as e:
                print(f"第16题填写失败: {e}")
            
            self.ccc += 1
            
            # 17 资金来源比例 - 家庭供给64%，奖学金7%，助学金13%，助学贷款13%，勤工助学3%
            try:
                # 等待元素加载
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='drv17_']"))
                )
                
                # 资金分配比例，确保总和为100%
                # 基于现实情况的资金来源分配
                base_allocation = {
                    "家庭供给": 65,      # 主要来源
                    "奖学金": 10,       # 优秀学生
                    "助学金": 10,       # 贫困生资助  
                    "助学贷款": 10,     # 贷款补充
                    "勤工助学": 5       # 兼职收入
                }
                
                fund_names = ["家庭供给", "奖学金", "助学金", "助学贷款", "勤工助学"]
                fund_values = [base_allocation[name] for name in fund_names]
                
                # 验证总和是否为100%
                total = sum(fund_values)
                if total != 100:
                    # 调整家庭供给比例使其总和为100%
                    adjustment = 100 - total
                    fund_values[0] += adjustment
                
                for i in range(1, 6):
                    try:
                        # 等待元素可交互
                        container = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.ID, f"drv17_{i}"))
                        )
                        input_element = container.find_element(By.TAG_NAME, "input")
                        
                        # 确保元素可见并可交互
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", input_element)
                        time.sleep(0.3)  # 短暂等待滚动完成
                        
                        # 强制清空输入框
                        self.driver.execute_script("arguments[0].value = '';", input_element)
                        input_element.clear()  # 再次清空确保
                        
                        # 发送新值
                        input_element.send_keys(str(fund_values[i-1]))
                        
                        # 验证值是否正确填入
                        actual_value = input_element.get_attribute('value')
                        print(f"已填写{fund_names[i-1]}: {fund_values[i-1]}% (实际值: {actual_value})")
                        
                        # 如果是最后一个输入框，额外验证
                        if i == 5:
                            print(f"最后一个输入框({fund_names[i-1]})填写完成: {fund_values[i-1]}%")
                            
                    except Exception as e:
                        print(f"第{i}个资金来源({fund_names[i-1] if i <= len(fund_names) else '未知'})填写失败: {e}")
                        
                # 输出总和验证
                final_total = sum(fund_values)
                print(f"资金分配总和: {final_total}%")
                        
            except Exception as e:
                print(f"第17题填写失败: {e}")
            
            print("已填写资金来源比例")
            
            # 18 单选题 - 改为单选模式
            try:
                # 等待元素加载
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[id^='q18_']"))
                )
                
                # 查找第18题的所有选项
                q18_options = self.driver.find_elements(By.CSS_SELECTOR, "[name='q18']")
                if q18_options:
                    # 随机选择一个选项
                    random_index = random.randint(0, len(q18_options) - 1)
                    q18_options[random_index].click()
                    print(f"已填写第18题单选题，选择第{random_index + 1}个选项")
                else:
                    # 如果没找到radio按钮，尝试其他选择器
                    q18_div = self.driver.find_element(By.ID, "div18")
                    if q18_div:
                        ops = q18_div.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                        if ops:
                            random_index = random.randint(0, len(ops) - 1)
                            ops[random_index].click()
                            print(f"已填写第18题单选题，选择第{random_index + 1}个选项")
                            
            except Exception as e:
                print(f"第18题填写失败: {e}")
            
            self.ccc += 1
            
            # 20 单选题 - 学费上涨承受能力
            divRefTab20 = self.driver.find_element(By.ID, "divRefTab20") if self.driver.find_elements(By.ID, "divRefTab20") else None
            if divRefTab20:
                for i in range(1, 7):
                    tr_element = divRefTab20.find_element(By.ID, f"drv20_{i}") if divRefTab20.find_elements(By.ID, f"drv20_{i}") else None
                    if tr_element:
                        a_elements = tr_element.find_elements(By.TAG_NAME, "a")
                        if a_elements:
                            random_index = random.randint(0, len(a_elements) - 1)
                            a_elements[random_index].click()
                            time.sleep(0.5)
                print("已填写学费上涨承受能力")
            
            # 21 单选题 - 学费上涨接受程度
            divRefTab21 = self.driver.find_element(By.ID, "divRefTab21") if self.driver.find_elements(By.ID, "divRefTab21") else None
            if divRefTab21:
                for i in range(1, 13):
                    tr_element = divRefTab21.find_element(By.ID, f"drv21_{i}") if divRefTab21.find_elements(By.ID, f"drv21_{i}") else None
                    if tr_element:
                        a_elements = tr_element.find_elements(By.TAG_NAME, "a")
                        if a_elements:
                            if i <= 6:
                                # 当前学校：接受程度较低
                                random_index = random.randint(0, max(0, len(a_elements) // 2))
                            else:
                                # 国内前十：接受程度较高
                                random_index = random.randint(max(0, len(a_elements) // 2), len(a_elements) - 1)
                            a_elements[random_index].click()
                            time.sleep(0.5)
                print("已填写学费上涨接受程度")
            
            # 22 单选题 - 学费用途了解程度
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [35, 32, 18, 8, 7]
                ops[self.danxuan(bili)].click()
                print("已填写学费用途了解程度")
            
            # 23 多选题 - 学费上涨接受原因（最多选三项）
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                option_probs = [4, 15, 20, 23, 13, 10, 3, 12]
                selected_count = 0
                max_selections = 3
                
                for i, op in enumerate(ops):
                    if selected_count < max_selections:
                        if random.random() * 100 < option_probs[i]:
                            op.click()
                            selected_count += 1
                            time.sleep(0.5)
                
                # 确保至少选一项
                if selected_count == 0 and ops:
                    ops[random.randint(0, len(ops) - 1)].click()
                
                print("已填写多选题23")
            
            # 24 单选题 - 实际情况调查
            divRefTab24 = self.driver.find_element(By.ID, "divRefTab24") if self.driver.find_elements(By.ID, "divRefTab24") else None
            if divRefTab24:
                for i in range(1, 7):
                    q24 = divRefTab24.find_element(By.ID, f"drv24_{i}") if divRefTab24.find_elements(By.ID, f"drv24_{i}") else None
                    if q24:
                        a_elements = q24.find_elements(By.TAG_NAME, "a")
                        if a_elements:
                            # 根据不同选项设置不同的选择概率
                            if i == 1:  # 选项1: "是"占60%-75%
                                is_selected = random.random() < 0.675
                            elif i == 2:  # 选项2: "是"占30%-50%
                                is_selected = random.random() < 0.4
                            elif i == 3:  # 选项3: "是"占60%-65%
                                is_selected = random.random() < 0.625
                            elif i == 4:  # 选项4: "是"占15%-20%
                                is_selected = random.random() < 0.175
                            elif i == 5:  # 选项5: "是"占10%-15%
                                is_selected = random.random() < 0.125
                            else:  # 选项6: "是"占20%-25%
                                is_selected = random.random() < 0.225
                            
                            index = 0 if is_selected else random.randint(1, len(a_elements) - 1)
                            a_elements[index].click()
                            time.sleep(0.5)
                print("已填写实际情况调查")
            
            # 25 单选题 - 上大学的原因
            divRefTab25 = self.driver.find_element(By.ID, "divRefTab25") if self.driver.find_elements(By.ID, "divRefTab25") else None
            if divRefTab25:
                very_important_probs = [20, 13, 15, 12, 10, 9, 9, 3, 9]
                for i in range(1, 11):
                    tr_element = divRefTab25.find_element(By.ID, f"drv25_{i}") if divRefTab25.find_elements(By.ID, f"drv25_{i}") else None
                    if tr_element:
                        a_elements = tr_element.find_elements(By.TAG_NAME, "a")
                        if a_elements and i-1 < len(very_important_probs):
                            if random.random() * 100 < very_important_probs[i-1]:
                                random_index = 0  # 选择"很重要"
                            else:
                                random_index = random.randint(1, len(a_elements) - 1)
                            a_elements[random_index].click()
                            time.sleep(0.5)
                print("已填写上大学的原因")
            
            # 26 单选题 - 起薪水平
            divRefTab26 = self.driver.find_element(By.ID, "divRefTab26") if self.driver.find_elements(By.ID, "divRefTab26") else None
            if divRefTab26:
                for i in range(1, 9):
                    tr_element = divRefTab26.find_element(By.ID, f"drv26_{i}") if divRefTab26.find_elements(By.ID, f"drv26_{i}") else None
                    if tr_element:
                        a_elements = tr_element.find_elements(By.TAG_NAME, "a")
                        if a_elements:
                            random_index = random.randint(0, len(a_elements) - 1)
                            a_elements[random_index].click()
                            time.sleep(0.5)
                print("已填写起薪水平")
            
            # 27 单选题 - 期望就业部门
            if self.ccc < len(lists):
                ops = lists[self.ccc].find_elements(By.TAG_NAME, "div")
                self.ccc += 1
                bili = [15, 20, 25, 20, 15, 5]  # 政府、事业单位、国企、外资、私企、其他
                ops[self.danxuan(bili)].click()
                print("已填写期望就业部门")
            
            # 28 填空题
            q28_input = self.driver.find_element(By.ID, "q28") if self.driver.find_elements(By.ID, "q28") else None
            if q28_input:
                tiankong_list = ['3800', '5800', '10000']
                bili = [33, 33, 34]
                q28_input.clear()
                q28_input.send_keys(tiankong_list[self.danxuan(bili)])
                print("已填写填空题28")
            
            # 29 填空题
            q29_input = self.driver.find_element(By.ID, "q29") if self.driver.find_elements(By.ID, "q29") else None
            if q29_input:
                tiankong_list = ['3800', '5800', '10000']
                bili = [33, 33, 34]
                q29_input.clear()
                q29_input.send_keys(tiankong_list[self.danxuan(bili)])
                print("已填写填空题29")
            
            # 30 填空题
            q30_input = self.driver.find_element(By.ID, "q30") if self.driver.find_elements(By.ID, "q30") else None
            if q30_input:
                tiankong_list = ['3800', '5800', '10000']
                bili = [33, 33, 34]
                q30_input.clear()
                q30_input.send_keys(tiankong_list[self.danxuan(bili)])
                print("已填写填空题30")
            
        except Exception as e:
            print(f"填写问卷时出错: {e}")
    
    def submit_questionnaire(self):
        """提交问卷"""
        try:
            # 第一步：点击提交按钮
            submit_button = self.driver.find_element(By.ID, "ctlNext")
            submit_button.click()
            print("点击提交按钮")
            time.sleep(2)
            
            # 第二步：处理安全校验弹窗
            self.handle_security_popup()
            
        except Exception as e:
            print(f"提交问卷时出错: {e}")
    
    def handle_security_popup(self):
        """处理安全校验弹窗"""
        print("处理安全校验弹窗...")
        
        # 尝试多种方式查找弹窗确认按钮
        confirm_selectors = [
            "#layui-layer1 .layui-layer-btn0",  # 标准的layui弹窗确认按钮
            ".layui-layer-btn0",                  # 通用确认按钮类
            ".layui-layer-page .layui-layer-btn",  # 页面弹窗按钮
            "#layui-layer1 .layui-layer-btn"      # 特定层弹窗按钮
        ]
        
        popup_found = False
        
        for selector in confirm_selectors:
            try:
                confirm_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                confirm_button.click()
                print(f"找到并点击确认按钮: {selector}")
                popup_found = True
                time.sleep(2)
                break
            except:
                continue
        
        if not popup_found:
            # 尝试通用方式查找可见的确认按钮
            try:
                all_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, a")
                for btn in all_buttons:
                    if ("确认" in btn.text or "重新提交" in btn.text) and btn.is_displayed():
                        btn.click()
                        print("找到通用确认按钮并点击")
                        popup_found = True
                        time.sleep(2)
                        break
            except:
                pass
        
        # 处理可能的验证
        self.handle_verification()
    
    def handle_verification(self):
        """处理各种验证"""
        print("处理安全验证...")
        
        # 检查是否有阿里云验证码弹窗
        try:
            aliyun_popup = self.wait.until(EC.presence_of_element_located((By.ID, "aliyunCaptcha-window-popup")))
            if aliyun_popup and aliyun_popup.is_displayed():
                print("检测到阿里云验证码弹窗")
                # 这里可以添加更复杂的验证码处理逻辑
                time.sleep(3)  # 等待用户手动处理
        except:
            pass
        
        # 检查是否有其他验证元素
        try:
            verification_elements = self.driver.find_elements(By.CSS_SELECTOR, "[class*='verify'], [class*='captcha'], [class*='check']")
            if verification_elements:
                for elem in verification_elements:
                    if elem.is_displayed():
                        try:
                            elem.click()
                            print("点击验证元素")
                            time.sleep(2)
                            break
                        except:
                            continue
        except:
            pass
    
    def run(self, wenjuan_url):
        """运行整个流程"""
        try:
            self.open_questionnaire(wenjuan_url)
            self.check_url(wenjuan_url)
            self.clear_cookie()
            self.scroll_to_bottom()
            self.fill_questionnaire()
            self.submit_questionnaire()
            print("问卷填写完成")
            
            # 保持浏览器打开，以便查看结果
            time.sleep(10)
            
        except Exception as e:
            print(f"运行时出错: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    # 填写问卷的网址
    wenjuan_url = 'https://v.wjx.cn/vm/h9RwweO.aspx'
    
    # 创建并运行自动填写实例
    wjx_auto_fill = WJXAutoFill()
    wjx_auto_fill.run(wenjuan_url)
