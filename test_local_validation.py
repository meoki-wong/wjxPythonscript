#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地验证脚本 - 验证第16题和第17题的逻辑修改
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

def generate_q17_values():
    """生成第17题的5个值，和为100，第一个值不低于55"""
    # 第一个值：55-70之间
    first_value = random.randint(55, 70)
    remaining = 100 - first_value
    
    # 生成剩余4个值
    values = [first_value]
    for i in range(3):  # 中间3个值
        # 确保剩下的值足够分配给剩余的输入框（每个至少1）
        max_val = remaining - (3 - i)
        val = random.randint(1, max_val)
        values.append(val)
        remaining -= val
    values.append(remaining)  # 最后一个值
    
    return values

def test_q16_q17_logic():
    """测试第16题和第17题的逻辑修改"""
    print("=" * 60)
    print("本地验证脚本 - 第16题和第17题的逻辑修改")
    print("=" * 60)
    
    # 测试第16题
    print("\n" + "=" * 30)
    print("测试第16题逻辑")
    print("=" * 30)
    
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
        
        # 验证住宿费范围
        assert 1000 <= accommodation_fee <= 3000, f"住宿费{accommodation_fee}不在1000-3000范围内"
        assert accommodation_fee % 500 == 0, f"住宿费{accommodation_fee}不是500的倍数"
        
        # 验证学费范围
        assert min_fee <= tuition_fee1 <= max_fee, f"学费1{tuition_fee1}不在{min_fee}-{max_fee}范围内"
        assert min_fee <= tuition_fee2 <= max_fee, f"学费2{tuition_fee2}不在{min_fee}-{max_fee}范围内"
        
        print("  ✅ 验证通过")
    
    # 测试第17题
    print("\n" + "=" * 30)
    print("测试第17题逻辑")
    print("=" * 30)
    
    for test_num in range(5):
        print(f"\n测试用例 {test_num + 1}:")
        
        values = generate_q17_values()
        
        print(f"   生成的值: {values}")
        print(f"   第一个值: {values[0]} (要求: >=55)")
        print(f"   总和: {sum(values)} (要求: =100)")
        
        # 验证条件
        assert values[0] >= 55, f"第一个值{values[0]}小于55"
        assert sum(values) == 100, f"总和{sum(values)}不等于100"
        assert len(values) == 5, f"值数量{len(values)}不等于5"
        
        print("   ✅ 验证通过")
    
    print("\n" + "=" * 60)
    print("所有测试用例验证通过！")
    print("第16题和第17题的逻辑修改正确")
    print("=" * 60)

if __name__ == "__main__":
    test_q16_q17_logic()