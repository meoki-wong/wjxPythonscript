#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第19题的处理逻辑
"""

import random

def generate_q19_values():
    """生成第19题的2个值，第二个值有80%概率大于第一个值"""
    print(f"   第19题特殊处理：第二个值有80%概率大于第一个值")
    # 生成第一个值
    first_value = random.randint(1, 80)  # 第一个值在1-80之间
    # 生成第二个值
    if random.random() < 0.8:  # 80%概率
        # 第二个值大于第一个值
        second_value = random.randint(first_value + 1, 100)
        print(f"   第二个值大于第一个值: {second_value} > {first_value}")
    else:  # 20%概率
        # 第二个值可以小于或等于第一个值
        second_value = random.randint(1, first_value)
        print(f"   第二个值不大于第一个值: {second_value} <= {first_value}")
    
    values = [first_value, second_value]
    print(f"   生成的值: {values}")
    return values

def test_q19_logic():
    """测试第19题的处理逻辑"""
    print("=" * 50)
    print("测试第19题的处理逻辑（第二个值有80%概率大于第一个值）")
    print("=" * 50)
    
    # 测试20次
    greater_count = 0
    total_tests = 20
    
    for test_num in range(total_tests):
        print(f"\n测试用例 {test_num + 1}:")
        
        values = generate_q19_values()
        first_value, second_value = values
        
        print(f"   第一个值: {first_value}")
        print(f"   第二个值: {second_value}")
        
        # 验证条件
        if second_value > first_value:
            greater_count += 1
            print("   ✅ 第二个值大于第一个值")
        else:
            print("   ⚠️ 第二个值不大于第一个值")
        
        # 验证值范围
        assert 1 <= first_value <= 80, f"第一个值{first_value}不在1-80范围内"
        assert 1 <= second_value <= 100, f"第二个值{second_value}不在1-100范围内"
        assert len(values) == 2, f"值数量{len(values)}不等于2"
    
    # 统计结果
    greater_percentage = (greater_count / total_tests) * 100
    print("\n" + "=" * 50)
    print(f"测试结果统计:")
    print(f"总测试次数: {total_tests}")
    print(f"第二个值大于第一个值的次数: {greater_count}")
    print(f"第二个值大于第一个值的百分比: {greater_percentage:.1f}%")
    print(f"期望百分比: 80%")
    
    # 验证百分比是否接近80%（允许±15%的误差）
    if 65 <= greater_percentage <= 95:
        print("✅ 百分比在合理范围内，验证通过！")
    else:
        print("❌ 百分比超出合理范围，可能需要调整！")
    
    print("=" * 50)

if __name__ == "__main__":
    test_q19_logic()