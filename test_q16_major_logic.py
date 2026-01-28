#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第16题根据专业类型设置学费的逻辑
"""

import random
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tuition_calculation():
    """测试学费计算逻辑"""
    
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
    
    # 测试不同的专业类型
    test_cases = [
        ("文史类", "文史"),
        ("汉语言文学", "文学"),
        ("历史学", "历史"),
        ("哲学", "哲学"),
        ("法学", "法学"),
        ("教育学", "教育"),
        ("经济学", "经济"),
        ("管理学", "管理"),
        ("理工类", "理工"),
        ("计算机科学与技术", "计算机"),
        ("数学与应用数学", "数学"),
        ("物理学", "物理"),
        ("化学工程", "化学"),
        ("生物科学", "生物"),
        ("机械工程", "工程"),
        ("艺术类", "艺术"),
        ("美术学", "美术"),
        ("音乐表演", "音乐"),
        ("舞蹈学", "舞蹈"),
        ("戏剧影视文学", "戏剧"),
        ("设计学", "设计"),
        ("传媒学", "传媒"),
        ("临床医学", "临床"),
        ("护理学", "护理"),
        ("药学", "药学"),
        ("医学影像学", "医学"),
        (None, None),  # 测试None值
        ("未知专业", None),  # 测试未知专业
    ]
    
    print("测试第16题学费计算逻辑：")
    print("=" * 60)
    
    for major_name, expected_keyword in test_cases:
        min_fee, max_fee = get_tuition_range(major_name)
        
        # 生成10个随机学费值进行测试
        tuition_values = []
        for _ in range(10):
            tuition = random.randint(min_fee // 100, max_fee // 100) * 100
            tuition_values.append(tuition)
        
        print(f"专业: {major_name}")
        print(f"学费范围: {min_fee}-{max_fee}元/年")
        print(f"随机生成的学费值: {tuition_values}")
        
        # 验证所有生成的值都在范围内
        all_valid = all(min_fee <= fee <= max_fee for fee in tuition_values)
        print(f"所有值都在范围内: {all_valid}")
        
        # 验证是整百数
        all_rounded = all(fee % 100 == 0 for fee in tuition_values)
        print(f"所有值都是整百数: {all_rounded}")
        
        print("-" * 40)
    
    print("\n测试完成！")

if __name__ == "__main__":
    test_tuition_calculation()