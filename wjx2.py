import logging
import random
import re
import threading
import traceback
from threading import Thread
import time
from typing import List

import numpy
import requests
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

# 导入滑块处理函数
from slider_handler import handle_slider_question


"""
任何疑问，请加qq群咨询：774326264 || 427847187 || 850281779 || 931614446
代码简洁版：https://github.com/Zemelee/wjx/blob/master/wjx.py  ---  视频教程： https://www.bilibili.com/video/BV1qc411T7CG/
除了python，作者还发布了js版脚本在scriptcat和greasyfork上，名字就叫“问卷星脚本”，不带任何前后缀，比py更方便且支持跳题逻辑：
    scriptcat地址：https://scriptcat.org/zh-CN/script-show-page/2833
    greasyfork地址：https://greasyfork.org/zh-CN/scripts/466722-%E9%97%AE%E5%8D%B7%E6%98%9F%E8%84%9A%E6%9C%AC
    相关系列教程：https://space.bilibili.com/29109990/channel/collectiondetail?sid=1340503&ctype=0

代码使用规则：
    你需要提前安装python环境，且已具备上述的所有安装包
    还需要下载好chrome的chromeDriver自动化工具（chrome版本号需要和chromedriver匹配，具体参考教程）
    并将chromeDriver放在python安装目录下，以便和selenium配套使用，准备工作做好即可直接运行
    按要求填写比例值并替换成自己的问卷链接即可运行你的问卷。
    虽然但是！！！即使正确填写概率值，不保证100%成功运行，因为代码再强大也强大不过问卷星的灵活性，别问我怎么知道的，都是泪
    如果有疑问可以进群提问，或者直接通过代刷网 http://sugarblack.top 直接刷问卷
"""

"""
获取代理ip，这里要使用到一个叫“品赞ip”的第三方服务: https://www.ipzan.com?pid=ggj6roo98
注册，需要实名认证（这是为了防止你用代理干违法的事，相当于网站的免责声明，属于正常步骤，所有代理网站都会有这一步）
将自己电脑的公网ip添加到网站的白名单中，然后选择地区，时长为1分钟，数据格式为txt，提取数量选1
然后点击生成api，将链接复制到放在zanip函数里
设置完成后，不要问为什么和视频教程有点不一样，因为与时俱进！(其实是因为懒，毕竟代码改起来容易，视频录起来不容易嘿嘿2023.10.29)
如果不需要ip可不设置，只是所有问卷的ip都会是同一个（悄悄提醒，品赞ip每周可以领3块钱）
"""


def zanip():
    # 这里放你的ip链接，选择你想要的地区，1分钟，ip池无所谓，数据格式txt，提取数量1，数量一定是1!其余默认即可
    api = "https://service.ipzan.com/core-extract?num=1&no=???&minute=1&area=all&pool=quality&secret=???"
    ip = requests.get(api).text
    return ip


# 示例问卷,试运行结束后,需要改成你的问卷地址
# 一个可以代刷问卷星的网站： http://sugarblack.top
url = "https://v.wjx.cn/vm/h9RwweO.aspx#"

"""
30题问卷结构：
1. 填空题（出生年份）
2. 单选题（性别）
3. 填空题（生源地省份）- 按发达程度分布，与第19、21题支付能力正相关
4-15. 单选题
16. 暂时不处理（跳过）
17. 滑块题（5个值需和为100）
18. 单选题
19. 滑块题（2个子滑块）- 与第3题生源地发达程度正相关
20-21. 矩阵题
22. 单选题
23. 多选排序题（最多选三个）
24-26. 矩阵题
27. 单选题
28-30. 填空题
"""

# 填空题参数 (第1题 + 第3题 + 第28-30题，共5个填空题)
# 第1题：出生年份 - 按在校大学生年龄分布优化
# 第3题：生源地省份 - 按经济发达程度分布，与第19、21题支付能力正相关
texts = {
    "1": ["2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010"],  # 出生年份范围
    "3": ["北京", "上海", "江苏", "浙江", "广东", "天津", "山东", "福建", "湖北", "湖南", "河南", "河北", "四川", "重庆", "陕西", "安徽", "江西", "辽宁", "吉林", "黑龙江", "山西", "云南", "贵州", "广西", "海南", "甘肃", "宁夏", "青海", "新疆", "西藏", "内蒙古"],  # 有大学的省份，按发达程度排序
    "28": ["内容A", "内容B", "内容C"],
    "29": ["信息X", "信息Y", "信息Z"],
    "30": ["数据1", "数据2", "数据3"],
}
# 第1题概率：2004-2007占70%，2001-2003占12%，2008-2010占18%
# 第3题概率：按省份经济发达程度设置权重，发达地区概率高，与第19、21题支付能力正相关
texts_prob = {
    "1": [4, 4, 4, 17.5, 17.5, 17.5, 17.5, 6, 6, 6],  # 精确到每个年份的概率权重：2001-2003(12%)，2004-2007(70%)，2008-2010(18%)
    "3": [25, 20, 18, 16, 14, 12, 10, 9, 8, 7, 6, 5, 5, 4, 4, 3, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 省份概率权重：发达程度高到低
    "28": [1, 1, 1],
    "29": [1, 1, 1],
    "30": [1, 1, 1],
}

# 单选题参数 (第2题 + 第4-15题 + 第18题 + 第22题 + 第27题，共16个单选题)
single_prob = {
    "0": [3.8, 6.2],  # 第2题性别：女生62%，男生38%（符合55-64% vs 37-45%要求，近几年女生超60%）
    "1": [1, 6, 7, 6],  # 第4题高考成绩：A:5%, B:30%, C:35%, D:30%
    "2": [2, 8, 33, 8],  # 第5题高校类型：A:4%, B:16%, C:65%, D:15%
    "3": [35, 25, 15, 12, 8, 6, 5, 4, 3, 2, 1, 1, 1],  # 第6题专业大类：13个选项，按收入排序工学＞经济学＞理学＞管理学＞农学＞文学＞艺术学＞法学＞医学＞历史学＞教育学+其他2个
    "4": [1, 1, 1, 1],  # 第7题年级：随机分布（大一、大二、大三、大四均匀分布）
    "5": [55, 35, 7, 2, 1],  # 第8题兄弟姐妹数量：1个55%，2个35%，3个7%，4个2%，5个及以上1%（3个及以上共10%，符合<10%要求）
    "6": [1, 1, 1, 1],  # 第9题家庭常住地：4个选项随机分布
    "8": -1,      # 第10题 (第8个单选题)
    "9": -1,      # 第11题 (第9个单选题)
    "10": -1,     # 第12题 (第10个单选题)
    "11": -1,     # 第13题 (第11个单选题)
    "12": -1,     # 第14题 (第12个单选题)
    "13": -1,     # 第15题 (第13个单选题)
    "14": -1,     # 第18题 (第14个单选题)
    "15": -1,     # 第22题 (第15个单选题)
    "16": -1,     # 第27题 (第16个单选题)
}

# 下拉框参数 (本问卷中第3题已改为填空题，此处留空)
droplist_prob = {
    # 第3题已改为填空题，省份数据在texts中定义
}

# 多选题参数 (第23题，多选排序，最多选三个)
multiple_prob = {
    "1": [50, 50, 50, 50, 50],  # 第23题，5个选项，每个选项50%概率被选中，但会限制最多选3个
}

# 矩阵题参数 (第20-21题 + 第24-26题，共5个矩阵题)
matrix_prob = {
    "1": -1,      # 第20题矩阵
    "2": -1,      # 第21题矩阵
    "3": -1,      # 第24题矩阵：实际只有2个选项（是/否），使用随机选择
    "4": -1,      # 第25题矩阵
    "5": -1,      # 第26题矩阵
}

# 量表题参数 (本问卷中没有量表题，留空)
scale_prob = {}

# 排序题不支持设置参数，如果有排序题程序会自动处理
# 滑块题没支持参数，程序能自动处理部分滑块题

# --------------到此为止，参数设置完毕，可以直接运行啦！-------------------
# 如果需要设置浏览器窗口数量，请转到最后一个函数(main函数)，注意看里面的注释喔！


# 参数归一化，把概率值按比例缩放到概率值和为1，比如某个单选题[1,2,3,4]会被转化成[0.1,0.2,0.3,0.4],[1,1]会转化成[0.5,0.5]
for prob in [single_prob, matrix_prob, droplist_prob, scale_prob, texts_prob]:
    for key in prob:
        if isinstance(prob[key], list):
            prob_sum = sum(prob[key])
            prob[key] = [x / prob_sum for x in prob[key]]

# 转化为列表,去除题号
single_prob = list(single_prob.values())
droplist_prob = list(droplist_prob.values())
multiple_prob = list(multiple_prob.values())
matrix_prob = list(matrix_prob.values())
scale_prob = list(scale_prob.values())
texts_prob = list(texts_prob.values())
texts = list(texts.values())
print("="*50)



# 校验IP地址合法性
def validate(ip):
    pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(\d{1,5})$"
    if re.match(pattern, ip):
        return True
    return False


# 检测题量
def detect(driver: WebDriver) -> List[int]:
    q_list: List[int] = []
    page_num = len(driver.find_elements(By.XPATH, '//*[@id="divQuestion"]/fieldset'))
    for i in range(1, page_num + 1):
        questions = driver.find_elements(By.XPATH, f'//*[@id="fieldset{i}"]/div')
        valid_count = sum(
            1 for question in questions if question.get_attribute("topic").isdigit()
        )
        q_list.append(valid_count)
    return q_list


# 填空题处理函数（增强版，支持动态问题28-30）
def vacant(driver: WebDriver, current, index):
    # 检查元素是否存在
    elements = driver.find_elements(By.CSS_SELECTOR, f"#q{current}")
    if len(elements) == 0:
        print(f"[调试] 第{current}题元素不存在，跳过")
        return False
    
    # 检查元素是否可见和可交互
    element = elements[0]
    if not element.is_displayed() or not element.is_enabled():
        print(f"[调试] 第{current}题元素不可见或不可交互，跳过")
        return False
    
    # 对于动态问题28-30，需要根据标题判断内容
    if current >= 28:
        try:
            # 获取问题标题
            title_element = driver.find_element(By.CSS_SELECTOR, f"#div{current} .field-label")
            title_text = title_element.text
            print(f"[调试] 第{current}题标题: {title_text}")
            
            # 根据标题关键词判断问题类型
            if "助学贷款" in title_text:
                # 助学贷款金额：16000-20000元（整百数）
                amount = random.randint(160, 200) * 100  # 16000-20000元，整百
                answer = str(amount)
                print(f"[调试] 识别为助学贷款题，填写金额: {answer}元")
                
            elif "奖学金" in title_text:
                # 奖学金金额：5000-8000元占90%，8000-10000元占10%（整百数）
                if random.random() < 0.9:
                    amount = random.randint(50, 80) * 100  # 5000-8000元
                else:
                    amount = random.randint(80, 100) * 100  # 8000-10000元
                answer = str(amount)
                print(f"[调试] 识别为奖学金题，填写金额: {answer}元")
                
            elif "助学金" in title_text:
                # 助学金金额：
                # 一档（特别困难）：4000-5000元，占30%
                # 二档（一般困难）：3000-3900元，占50%  
                # 三档（较低困难）：2500-2800元，占20%
                rand = random.random()
                if rand < 0.3:  # 30% 一档
                    amount = random.randint(40, 50) * 100  # 4000-5000元
                elif rand < 0.8:  # 50% 二档  
                    amount = random.randint(30, 39) * 100  # 3000-3900元
                else:  # 20% 三档
                    amount = random.randint(25, 28) * 100  # 2500-2800元
                answer = str(amount)
                print(f"[调试] 识别为助学金题，填写金额: {answer}元")
                
            else:
                # 其他情况使用默认逻辑 - 对于动态问题28-30，提供合理的默认值
                if 0 <= index <= 2:  # 对应问题28-30
                    # 提供合理的默认金额范围
                    amount = random.randint(1000, 20000)  # 1000-20000元范围
                    answer = str(amount)
                    print(f"[调试] 未识别特定类型，使用默认金额: {answer}元")
                else:
                    answer = "未知"
                    print(f"[调试] 未识别特定类型，使用默认值: {answer}")
                
        except Exception as e:
            print(f"[调试] 获取标题失败，使用默认逻辑: {str(e)}")
            # 对于动态问题28-30，提供合理的默认值
            if 0 <= index <= 2:  # 对应问题28-30
                amount = random.randint(1000, 20000)  # 1000-20000元范围
                answer = str(amount)
                print(f"[调试] 异常处理，使用默认金额: {answer}元")
            else:
                answer = "未知"
                print(f"[调试] 异常处理，使用默认值: {answer}")
    else:
        # 非动态问题使用原有逻辑
        content = texts[index]
        p = texts_prob[index]
        text_index = numpy.random.choice(a=numpy.arange(0, len(p)), p=p)
        answer = content[text_index]
    
    # 使用JavaScript设置值，更可靠
    try:
        driver.execute_script("arguments[0].value = arguments[1];", element, answer)
        driver.execute_script("arguments[0].dispatchEvent(new Event('input', {bubbles: true}));", element)
        driver.execute_script("arguments[0].dispatchEvent(new Event('change', {bubbles: true}));", element)
        print(f"[调试] 成功设置值: {answer}")
    except Exception as e:
        print(f"[调试] JavaScript设置值失败，尝试直接输入: {str(e)}")
        try:
            element.clear()
            element.send_keys(answer)
        except Exception as e2:
            print(f"[调试] 直接输入也失败: {str(e2)}")
            return False
    
    return True


# 单选题处理函数
def single(driver: WebDriver, current, index):
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    a = driver.find_elements(By.XPATH, xpath)
    p = single_prob[index]
    if p == -1:
        r = random.randint(1, len(a))
    else:
        assert len(p) == len(
            a
        ), f"第{current}题参数长度：{len(p)},选项长度{len(a)},不一致！"
        r = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)
    driver.find_element(
        By.CSS_SELECTOR, f"#div{current} > div.ui-controlgroup > div:nth-child({r})"
    ).click()


# 下拉框处理函数
def droplist(driver: WebDriver, current, index):
    # 先点击“请选择”
    driver.find_element(By.CSS_SELECTOR, f"#select2-q{current}-container").click()
    time.sleep(0.5)
    # 选项数量
    options = driver.find_elements(
        By.XPATH, f"//*[@id='select2-q{current}-results']/li"
    )
    p = droplist_prob[index]  # 对应概率
    r = numpy.random.choice(a=numpy.arange(1, len(options)), p=p)
    driver.find_element(
        By.XPATH, f"//*[@id='select2-q{current}-results']/li[{r + 1}]"
    ).click()


def multiple(driver: WebDriver, current, index):
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    options = driver.find_elements(By.XPATH, xpath)
    mul_list = []
    p = multiple_prob[index]
    assert len(options) == len(p), f"第{current}题概率值和选项值不一致"
    # 生成序列,同时保证至少有一个1
    while sum(mul_list) <= 1:
        mul_list = []
        for item in p:
            a = numpy.random.choice(
                a=numpy.arange(0, 2), p=[1 - (item / 100), item / 100]
            )
            mul_list.append(a)
    # 依次点击
    for index, item in enumerate(mul_list):
        if item == 1:
            css = f"#div{current} > div.ui-controlgroup > div:nth-child({index + 1})"
            driver.find_element(By.CSS_SELECTOR, css).click()


# 第16题特殊矩阵处理函数（同级结构）
def matrix_q16(driver: WebDriver):
    """
    处理第16题的特殊矩阵结构
    结构：#q16_1 label 和 #q16_2 label 同级
    每个label下有span.textCont，对应的input框q16_1和q16_2
    """
    print(f"[调试] 处理第16题特殊矩阵结构...")
    
    try:
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
            return False
        
        # 为每个子问题设置值
        for i, sub_q in enumerate(sub_questions):
            # 生成随机文本（可以根据需要修改）
            random_text = f"选项{i+1}_{random.randint(1, 100)}"
            random_value = str(random.randint(1, 5))  # 假设是1-5的值
            
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
            
            time.sleep(0.2)  # 小延迟
        
        print("✅ 第16题特殊矩阵处理完成")
        return True
        
    except Exception as e:
        print(f"❌ 第16题特殊矩阵处理失败: {str(e)}")
        return False


# 特殊处理第24题矩阵（是/否类型）
def matrix_yesno(driver: WebDriver, current, probabilities):
    """
    处理"是/否"类型的矩阵题（如第24题）
    Args:
        driver: WebDriver实例
        current: 当前题号
        probabilities: 每个子问题选择"是"的概率列表
    """
    print(f"[调试] 第{current}题是/否矩阵题特殊处理")
    
    xpath1 = f'//*[@id="divRefTab{current}"]/tbody/tr'
    a = driver.find_elements(By.XPATH, xpath1)
    q_num = 0  # 矩阵的题数量
    for tr in a:
        if tr.get_attribute("rowindex") is not None:
            q_num += 1
    
    print(f"[调试] 第{current}题矩阵有{q_num}个子问题")
    
    # 验证概率数组长度
    if len(probabilities) != q_num:
        print(f"❌ [错误] 概率数组长度({len(probabilities)})与子问题数量({q_num})不匹配！")
        return False
    
    # 遍历每一道小题
    for i in range(1, q_num + 1):
        # 根据概率选择"是"或"否"
        # "是"对应第2列，"否"对应第3列
        yes_prob = probabilities[i-1] / 100.0  # 转换为0-1之间的概率
        
        if random.random() < yes_prob:
            opt = 2  # 选择"是"
            choice_text = "是"
        else:
            opt = 3  # 选择"否"  
            choice_text = "否"
        
        print(f"[调试] 子问题{i}选择{choice_text}（概率{probabilities[i-1]}%）")
        
        try:
            driver.find_element(
                By.CSS_SELECTOR, f"#drv{current}_{i} > td:nth-child({opt})"
            ).click()
            time.sleep(0.2)  # 添加小延迟
        except Exception as e:
            print(f"❌ 子问题{i}点击失败: {str(e)}")
            return False
    
    return True

# 矩阵题处理函数
def matrix(driver: WebDriver, current, matrix_question_index):
    """
    处理矩阵题
    Args:
        driver: WebDriver实例
        current: 当前题号
        matrix_question_index: 矩阵题的序号（从0开始）
    """
    # 特殊处理第24题
    if current == 24:
        print(f"[调试] 第24题使用特殊是/否矩阵处理")
        # 第24题的概率要求：
        # [1]"我的家庭完全能够支付我上学所需的各项费用": 60-75% "是"
        # [2]"如有需要，我的父母愿意为我上大学而向亲友借贷": 30-50% "是"  
        # [3]"我的家庭曾为我上大学而有计划地进行储蓄": 60-65% "是"
        # [4]"本学年我曾申请过贷款": 15-20% "是"
        # [5]"其他情况": ~5% "是"
        q24_probabilities = [70, 40, 62, 17, 5]  # 取中间值
        if matrix_yesno(driver, current, q24_probabilities):
            return matrix_question_index + 1
        else:
            return matrix_question_index + 1  # 即使失败也继续
    
    xpath1 = f'//*[@id="divRefTab{current}"]/tbody/tr'
    a = driver.find_elements(By.XPATH, xpath1)
    q_num = 0  # 矩阵的题数量
    for tr in a:
        if tr.get_attribute("rowindex") is not None:
            q_num += 1
    
    print(f"[调试] 第{current}题矩阵有{q_num}个子问题")
    
    # 选项数量
    xpath2 = f'//*[@id="drv{current}_1"]/td'
    b = driver.find_elements(By.XPATH, xpath2)  # 题的选项数量+1 = 6
    option_count = len(b)  # 实际选项数量（包括表头）
    actual_options = option_count - 1  # 减去表头后的实际选项数量
    
    print(f"[调试] 第{current}题矩阵选项检测：总td数={option_count}, 实际选项数={actual_options}")
    print(f"[调试] 选项范围: 2到{option_count}（包含表头）")
    
    # 获取当前矩阵题的概率参数
    # matrix_prob 现在是列表，matrix_question_index 是索引
    if matrix_question_index < len(matrix_prob):
        p = matrix_prob[matrix_question_index]
    else:
        p = -1  # 如果没有找到，使用-1（随机选择）
    
    print(f"[调试] 使用概率参数: {p}")
    
    # 验证概率数组大小是否匹配
    if p != -1 and isinstance(p, list):
        expected_options = len(p) + 1  # 概率数组长度 + 1（因为选项从2开始）
        if expected_options != option_count:
            print(f"❌ [错误] 概率数组长度({len(p)})与选项数量({actual_options})不匹配！")
            print(f"❌ [错误] 期望td数={expected_options}, 实际td数={option_count}")
            return matrix_question_index + 1  # 跳过此题，返回下一个索引
    
    # 遍历每一道小题
    for i in range(1, q_num + 1):
        if p == -1:
            opt = random.randint(2, len(b))
        else:
            opt = numpy.random.choice(a=numpy.arange(2, len(b) + 1), p=p)
        
        print(f"[调试] 子问题{i}选择选项{opt}")
        
        try:
            driver.find_element(
                By.CSS_SELECTOR, f"#drv{current}_{i} > td:nth-child({opt})"
            ).click()
            time.sleep(0.2)  # 添加小延迟
        except Exception as e:
            print(f"❌ 子问题{i}点击失败: {str(e)}")
            raise
    
    return matrix_question_index + 1  # 返回下一个矩阵题的索引


# 排序题处理函数，排序暂时只能随机
def reorder(driver: WebDriver, current):
    xpath = f'//*[@id="div{current}"]/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    for j in range(1, len(a) + 1):
        b = random.randint(j, len(a))
        driver.find_element(
            By.CSS_SELECTOR, f"#div{current} > ul > li:nth-child({b})"
        ).click()
        time.sleep(0.4)


# 量表题处理函数
def scale(driver: WebDriver, current, index):
    xpath = f'//*[@id="div{current}"]/div[2]/div/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    p = scale_prob[index]
    if p == -1:
        b = random.randint(1, len(a))
    else:
        b = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)
    driver.find_element(
        By.CSS_SELECTOR, f"#div{current} > div.scale-div > div > ul > li:nth-child({b})"
    ).click()


# 多选排序题处理函数（最多选三个）
def multiple_reorder(driver: WebDriver, current, index):
    xpath = f'//*[@id="div{current}"]/ul/li'
    options = driver.find_elements(By.XPATH, xpath)
    p = multiple_prob[index]
    
    # 生成选择序列，最多选3个
    selected_indices = []
    for i, prob in enumerate(p):
        if numpy.random.choice([0, 1], p=[1 - prob/100, prob/100]) == 1:
            selected_indices.append(i)
    
    # 如果选择的超过3个，随机减少到3个
    if len(selected_indices) > 3:
        selected_indices = random.sample(selected_indices, 3)
    
    # 如果选择的少于1个，至少选1个
    if len(selected_indices) == 0:
        selected_indices = [random.randint(0, len(options) - 1)]
    
    # 对选中的选项进行排序
    for i, option_index in enumerate(selected_indices):
        driver.find_element(
            By.CSS_SELECTOR, f"#div{current} > ul > li:nth-child({option_index + 1})"
        ).click()
        time.sleep(0.3)


# 刷题逻辑函数（30题结构）
def brush(driver: WebDriver):
    print("[调试] 开始检测问卷结构...")
    q_list = detect(driver)  # 检测页数和每一页的题量
    print(f"[调试] 检测到问卷结构: {q_list} 页，每页题目数量")
    
    single_num = 0  # 第num个单选题
    vacant_num = 0  # 第num个填空题
    droplist_num = 0  # 第num个下拉框题
    multiple_num = 0  # 第num个多选题
    matrix_num = 0  # 第num个矩阵小题
    scale_num = 0  # 第num个量表题
    current = 0  # 题号
    
    for page_idx, j in enumerate(q_list, 1):  # 遍历每一页
        print(f"\n[调试] 处理第{page_idx}页，共{j}道题")
        
        for k in range(1, j + 1):  # 遍历该页的每一题
            current += 1
            print(f"\n[调试] 开始处理第{current}题...")
            
            try:
                # 根据题号判断题型（30题结构）
                if current == 1:  # 第1题：填空题
                    print(f"[调试] 第{current}题：填空题")
                    vacant(driver, current, vacant_num)
                    vacant_num += 1
                    print(f"✅ 第{current}题填写完成")
                    
                elif current == 2:  # 第2题：单选题
                    print(f"[调试] 第{current}题：单选题")
                    single(driver, current, single_num)
                    single_num += 1
                    print(f"✅ 第{current}题选择完成")
                    
                elif current == 3:  # 第3题：填空题（生源地省份）
                    print(f"[调试] 第{current}题：填空题（生源地省份）")
                    vacant(driver, current, vacant_num)
                    vacant_num += 1
                    print(f"✅ 第{current}题省份填写完成")
                    
                elif 4 <= current <= 15:  # 第4-15题：单选题
                    print(f"[调试] 第{current}题：单选题")
                    single(driver, current, single_num)
                    single_num += 1
                    print(f"✅ 第{current}题选择完成")
                    
                elif current == 16:  # 第16题：特殊矩阵题
                    print(f"[调试] 第{current}题：特殊矩阵题（同级结构）")
                    if not matrix_q16(driver):
                        raise Exception(f"第{current}题特殊矩阵处理失败")
                    print(f"✅ 第{current}题特殊矩阵处理完成")
                    
                elif current == 17:  # 第17题：滑块题（有5个子滑块）
                    print(f"[调试] 第{current}题：滑块题（5个子滑块）")
                    if not handle_slider_question(driver, current, 5):
                        raise Exception(f"第{current}题滑块处理失败")
                    print(f"✅ 第{current}题滑块设置完成")
                    
                elif current == 18:  # 第18题：单选题
                    print(f"[调试] 第{current}题：单选题")
                    single(driver, current, single_num)
                    single_num += 1
                    print(f"✅ 第{current}题选择完成")
                    
                elif current == 19:  # 第19题：滑块题（有2个子滑块）
                    print(f"[调试] 第{current}题：滑块题（2个子滑块）")
                    if not handle_slider_question(driver, current, 2):
                        raise Exception(f"第{current}题滑块处理失败")
                    print(f"✅ 第{current}题滑块设置完成")
                    
                elif 20 <= current <= 21:  # 第20-21题：矩阵题
                    print(f"[调试] 第{current}题：矩阵题")
                    matrix_num = matrix(driver, current, matrix_num)
                    print(f"✅ 第{current}题矩阵填写完成")
                    
                elif current == 22:  # 第22题：单选题
                    print(f"[调试] 第{current}题：单选题")
                    single(driver, current, single_num)
                    single_num += 1
                    print(f"✅ 第{current}题选择完成")
                    
                elif current == 23:  # 第23题：多选排序题（最多选三个）
                    print(f"[调试] 第{current}题：多选排序题")
                    multiple_reorder(driver, current, multiple_num)
                    multiple_num += 1
                    print(f"✅ 第{current}题多选排序完成")
                    
                elif 24 <= current <= 26:  # 第24-26题：矩阵题
                    print(f"[调试] 第{current}题：矩阵题")
                    matrix_num = matrix(driver, current, matrix_num)
                    print(f"✅ 第{current}题矩阵填写完成")
                    
                elif current == 27:  # 第27题：单选题
                    print(f"[调试] 第{current}题：单选题")
                    single(driver, current, single_num)
                    single_num += 1
                    print(f"✅ 第{current}题选择完成")
                    
                elif 28 <= current <= 30:  # 第28-30题：填空题（条件性显示）
                    print(f"[调试] 第{current}题：填空题（条件性显示）")
                    # 对于动态问题28-30，使用特殊的索引处理
                    dynamic_index = current - 28  # 0, 1, 2 对应 28, 29, 30题
                    if vacant(driver, current, dynamic_index):
                        vacant_num += 1
                        print(f"✅ 第{current}题填写完成")
                    else:
                        print(f"⚠️ 第{current}题元素不存在，跳过")
                    
                else:
                    print(f"⚠️ 第{current}题为不支持题型！")
                    
            except Exception as e:
                print(f"❌ [错误] 第{current}题处理失败: {str(e)}")
                # 显示当前页面信息
                try:
                    print(f"[调试] 当前页面标题: {driver.title}")
                    print(f"[调试] 当前URL: {driver.current_url}")
                    # 检查是否存在预期的元素
                    element_exists = len(driver.find_elements(By.CSS_SELECTOR, f"#q{current}")) > 0
                    print(f"[调试] 元素#q{current}是否存在: {element_exists}")
                except:
                    pass
                raise  # 重新抛出异常
                
        print(f"\n[调试] 第{page_idx}页处理完成")
        
        time.sleep(0.5)
        # 一页结束过后要么点击下一页，要么点击提交
        try:
            print("[调试] 尝试点击下一页...")
            driver.find_element(By.CSS_SELECTOR, "#divNext").click()  # 点击下一页
            time.sleep(0.5)
            print("✅ 成功点击下一页")
        except:
            print("[调试] 无法找到下一页按钮，尝试点击提交...")
            # 点击提交
            driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
            print("✅ 成功点击提交")
            
    print("[调试] 问卷填写完成，准备提交...")
    submit(driver)


# 提交函数
def submit(driver: WebDriver):
    time.sleep(1)
    # 点击对话框的确认按钮
    try:
        driver.find_element(By.XPATH, '//*[@id="layui-layer1"]/div[3]/a').click()
        time.sleep(1)
    except:
        pass
    # 点击智能检测按钮，因为可能点击提交过后直接提交成功的情况，所以智能检测也要try
    try:
        driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
        time.sleep(3)
    except:
        pass
    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        sliderButton = driver.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get("width")
            ActionChains(driver).drag_and_drop_by_offset(
                sliderButton, width, 0
            ).perform()
    except:
        pass


def run(xx, yy):
    option = webdriver.ChromeOptions()
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option("useAutomationExtension", False)
    global cur_num, cur_fail
    driver = None  # 初始化driver变量
    
    while cur_num < target_num:
        if driver is None:  # 只有在需要新浏览器时才创建
            if use_ip:
                ip = zanip()
                option.add_argument(f"--proxy-server={ip}")
            driver = webdriver.Chrome(options=option)
            driver.set_window_size(1200, 800)  # 增大窗口便于调试
            driver.set_window_position(x=xx, y=yy)
            # 有学过 vue2 的吗, Object.defineProperty 这个 api 是不是很眼熟啊哈哈哈
            driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                },
            )
        
        try:
            print(f"\n[调试] 正在打开问卷页面: {url}")
            driver.get(url)
            print(f"[调试] 页面标题: {driver.title}")
            print(f"[调试] 当前URL: {driver.current_url}")
            
            # 等待页面加载
            time.sleep(3)
            
            url1 = driver.current_url  # 表示问卷链接
            print(f"[调试] 开始填写问卷，初始URL: {url1}")
            
            brush(driver)
            
            # 刷完后给一定时间让页面跳转
            time.sleep(4)
            url2 = driver.current_url
            print(f"[调试] 填写完成后的URL: {url2}")
            
            if url1 != url2:
                cur_num += 1
                print(
                    f"✅ 成功填写第{cur_num}份 - 失败{cur_fail}次 - {time.strftime('%H:%M:%S', time.localtime(time.time()))} "
                )
                print("[调试] 问卷填写成功！浏览器将保持打开状态30秒供您查看...")
                time.sleep(30)  # 保持浏览器打开30秒
                driver.quit()
                driver = None  # 重置driver变量
            else:
                print("[调试] URL未变化，可能填写失败。浏览器保持打开状态供您检查...")
                print("[提示] 您可以手动检查页面，按Ctrl+C停止脚本")
                while True:  # 保持浏览器打开，直到用户手动停止
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            print("\n[用户中断] 用户手动停止脚本")
            if driver:
                print("[提示] 浏览器保持打开状态，您可以检查页面")
            break
            
        except Exception as e:
            print(f"\n❌ [错误] 发生异常: {str(e)}")
            traceback.print_exc()
            
            # 获取页面信息用于调试
            try:
                print(f"[调试] 异常发生时页面标题: {driver.title}")
                print(f"[调试] 异常发生时URL: {driver.current_url}")
                # 尝试获取页面源码的一部分
                page_source = driver.page_source[:500]  # 获取前500字符
                print(f"[调试] 页面源码前500字符:\n{page_source}...")
            except:
                pass
            
            lock.acquire()
            cur_fail += 1
            lock.release()
            
            print(
                f"\n⚠️ 已失败{cur_fail}次, 失败超过{int(fail_threshold)}次将强制停止",
            )
            
            if cur_fail >= fail_threshold:
                logging.critical(
                    "失败次数过多，程序将停止。浏览器保持打开状态供您调试..."
                )
                print("\n🔍 [调试模式] 浏览器保持打开状态，您可以：")
                print("   1. 检查页面元素和结构")
                print("   2. 使用开发者工具(F12)查看HTML")
                print("   3. 手动尝试填写问卷")
                print("   4. 按Ctrl+C停止脚本")
                
                # 保持浏览器打开，直到用户手动停止
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n用户选择停止脚本")
                break
            else:
                print(f"\n🔍 [调试模式] 浏览器保持打开状态，供您检查第{cur_fail}次失败原因...")
                print("[提示] 您可以检查页面后按Ctrl+C继续下一个尝试")
                try:
                    input("按回车键继续下一个尝试，或按Ctrl+C停止脚本...")
                except KeyboardInterrupt:
                    print("\n用户选择停止脚本")
                    break
                
                # 关闭当前浏览器，创建新的浏览器实例
                if driver:
                    driver.quit()
                    driver = None
                continue


# 多线程执行run函数
if __name__ == "__main__":
    # 一个可以代刷问卷星的网站： http://sugarblack.top
    target_num = 1  # 目标份数
    # 失败阈值，数值可自行修改为固定整数
    fail_threshold = target_num / 4 + 1
    cur_num = 0  # 已提交份数
    cur_fail = 0  # 已失败次数
    lock = threading.Lock()
    use_ip = False
    stop = False
    if validate(zanip()):
        print("IP设置成功, 将使用代理ip填写")
        use_ip = True
    else:
        print("IP设置失败, 将使用本机ip填写")
    num_threads = 1  # 窗口数量
    threads: list[Thread] = []
    # 创建并启动线程
    for i in range(num_threads):
        x = 50 + i * 60  # 浏览器弹窗左上角的横坐标
        y = 50  # 纵坐标
        thread = Thread(target=run, args=(x, y))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

"""
    总结,你需要修改的有: 1 每个题的比例参数(必改)  2 问卷链接(必改)  3 ip链接(可选)  4 浏览器窗口数量(可选)
    有疑问可以加qq群喔: 774326264 || 427847187 || 850281779 || 931614446; 
    虽然我不一定回hhh, 但是群友们不一定不回
    Presented by 鐘
"""
