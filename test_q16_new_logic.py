#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第16题的处理逻辑
"""

import random

def get_accommodation_fee(q5_selection):
    """根据第5题选择计算住宿金额"""
    if q5_selection is None:
        q5_selection = 1  # 默认值
    
    q5_selection = int(q5_selection)
    # 基础500元 + 500元 * 选项数
    base_fee = 500 + 500 * q5_selection
    
    # 确保不超过3000元
    if base_fee > 3000:
        base_fee = 3000
    
    # 生成1000-3000之间的随机值，以500为步长
    possible_values = [1000, 1500, 2000, 2500, 3000]
    # 偏向于计算出的值，但有一定随机性
    if base_fee in possible_values:
        # 60%概率选择计算出的值，40%概率选择其他值
        if random.random() < 0.6:
            return base_fee
        else:
            other_values = [v for v in possible_values if v != base_fee]
            return random.choice(other_values)
    else:
        # 如果计算出的值不在标准值中，选择最接近的
        closest = min(possible_values, key=lambda x: abs(x - base_fee))
        return closest

def get_tuition_range(major_type):
    """根据专业类型返回学费范围"""
    if major_type is None:
        # 默认范围（文史类）
        return (4000, 6000)
    
    major_type = str(major_type).strip()
    
    # 文史类：4000-6000元/年
    if any(keyword in major_type for keyword in ["文史", "文学", "历史", "哲学", "法学", "教育", "经济", "管理"]):
        return (4000, 6000)
    # 理工类：5000-8000元/年  
    elif any(keyword in major_type for keyword in ["理工", "工学", "理学", "工程", "计算机", "数学", "物理", "化学", "生物"]):
        return (5000, 8000)
    # 艺术类：8000-15000元/年
    elif any(keyword in major_type for keyword in ["艺术", "美术", "音乐", "舞蹈", "戏剧", "设计", "传媒"]):
        return (8000, 15000)
    # 医学类（特殊处理，通常较高）
    elif any(keyword in major_type for keyword in ["医学", "临床", "护理", "药学"]):
        return (6000, 10000)
    else:
        # 默认文史类范围
        return (4000, 6000)

def test_q16_logic():
    """测试第16题的处理逻辑"""
    print("=" * 50)
    print("测试第16题的处理逻辑")
    print("=" * 50)
    
    # 测试不同的第5题选择
    for q5_selection in range(1, 5):
        accommodation_fee = get_accommodation_fee(q5_selection)
        print(f"\n第5题选择选项{q5_selection} -> 住宿费: {accommodation_fee}元/年")
    
    # 测试不同的专业类型
    test_majors = ["文史", "理工", "艺术", "医学", "其他"]
    for major in test_majors:
        min_fee, max_fee = get_tuition_range(major)
        print(f"\n专业类型: {major}")
        print(f"学费范围: {min_fee}-{max_fee}元/年")
        
        # 模拟生成3个学费值
        for i in range(3):
            tuition_fee = random.randint(min_fee // 100, max_fee // 100) * 100
            print(f"  学费{i+1}: {tuition_fee}元/年")
    
    # 综合测试
    print("\n" + "=" * 50)
    print("综合测试（第16题完整处理）")
    print("=" * 50)
    
    test_cases = [
        (1, "文史", "第5题选1，专业为文史类"),
        (2, "理工", "第5题选2，专业为理工类"),
        (3, "艺术", "第5题选3，专业为艺术类"),
        (4, "医学", "第5题选4，专业为医学类"),
    ]
    
    for q5_selection, major_type, description in test_cases:
        print(f"\n测试用例: {description}")
        
        # 获取住宿费
        accommodation_fee = get_accommodation_fee(q5_selection)
        
        # 获取学费范围
        min_fee, max_fee = get_tuition_range(major_type)
        
        # 生成学费值
        tuition_fee1 = random.randint(min_fee // 100, max_fee // 100) * 100
        tuition_fee2 = random.randint(min_fee // 100, max_fee // 100) * 100
        
        print(f"  q16_1 (学费): {tuition_fee1}元/年")
        print(f"  q16_2 (住宿费): {accommodation_fee}元/年")
        print(f"  q16_3 (学费): {tuition_fee2}元/年")

if __name__ == "__main__":
    test_q16_logic()