#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试第17题的处理逻辑
"""

import random

def test_q17_logic():
    """测试第17题的处理逻辑"""
    print("=" * 50)
    print("测试第17题的处理逻辑（5个值和为100，第一个值不低于55）")
    print("=" * 50)
    
    # 测试10次
    for test_num in range(10):
        print(f"\n测试用例 {test_num + 1}:")
        
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
        
        print(f"   生成的值: {values}")
        print(f"   第一个值: {values[0]} (要求: >=55)")
        print(f"   总和: {sum(values)} (要求: =100)")
        
        # 验证条件
        assert values[0] >= 55, f"第一个值{values[0]}小于55"
        assert sum(values) == 100, f"总和{sum(values)}不等于100"
        assert len(values) == 5, f"值数量{len(values)}不等于5"
        
        print("   ✅ 验证通过")
    
    print("\n" + "=" * 50)
    print("所有测试用例验证通过！")
    print("=" * 50)

if __name__ == "__main__":
    test_q17_logic()