// ==UserScript==
// @name         问卷星(定制比例)模板（2025最新版！！！）
// @namespace    http://tampermonkey.net/
// @version      4.8
// @description  可定制每个选项比例概率，刷问卷前需要改代码，目前模板支持单选,多选,填空,量表，下拉框题，如有其它高级题型可进群定制脚本，使用需要一定js知识，不懂的可以加QQ群交流，QQ1群：865248256 QQ2群：487872111，QQ3群：530327843，本群也提供定制脚本刷问卷服务，服务快捷，价格优惠。https://www.wjx.cn/vj/QvfxoEU.aspx 是测试脚本问卷。如遇问题可加QQ 751947907 B站教程：https://www.bilibili.com/video/BV1Mw411R7yp 推荐一个全自动填问卷平台：https://www.yifengwenjuan.top  超级好用！
// @author       ZYY
// @match        https://www.wjx.cn/vm/*
// @match        https://www.wjx.cn/vj/*
// @match        https://ks.wjx.top/*
// @match        https://ww.wjx.top/*
// @match        https://w.wjx.top/*
// @match        https://*.wjx.top/*
// @match        https://*.wjx.cn/vm/*
// @match        https://*.wjx.cn/vj/*
// @match        https://*.wjx.com/vm/*
// @match        https://*.wjx.com/vj/*
// @match        https://www.wjx.cn/*
// @downloadURL https://update.greasyfork.org/scripts/427090/%E9%97%AE%E5%8D%B7%E6%98%9F%28%E5%AE%9A%E5%88%B6%E6%AF%94%E4%BE%8B%29%E6%A8%A1%E6%9D%BF%EF%BC%882025%E6%9C%80%E6%96%B0%E7%89%88%EF%BC%81%EF%BC%81%EF%BC%81%EF%BC%89.user.js
// @updateURL https://update.greasyfork.org/scripts/427090/%E9%97%AE%E5%8D%B7%E6%98%9F%28%E5%AE%9A%E5%88%B6%E6%AF%94%E4%BE%8B%29%E6%A8%A1%E6%9D%BF%EF%BC%882025%E6%9C%80%E6%96%B0%E7%89%88%EF%BC%81%EF%BC%81%EF%BC%81%EF%BC%89.meta.js
// ==/UserScript==

(function () {
    'use strict';

    //===========================开始==============================
    clearCookie();

    //*************************************************************************************************************************************************************************

    //本脚本为vj版，本作者的vm版脚本可搭配群主做的程序实现切换IP，修改问卷答题时间，支持一键刷问卷（不存在验证过不去的情况），浏览器多开（最多五个）的功能，如果有同学想靠刷问卷兼职的同学可以考虑，联系管理员(qq:751947907)即可咨询
    //实在不会的同学推荐用全自动填问卷平台：https://www.yifengwenjuan.top  超级好用！
    //视频教程链接：https://www.bilibili.com/video/BV135yaYfEBP



    //*************************************************************************************************************************************************************************


    //填写刷问卷的网址  注意，如果问卷中的网址中间是vm,一定要改成vj!!!,像这样 https://www.wjx.cn/vj/QvfxoEU.aspx
    var wenjuan_url = 'https://v.wjx.cn/vm/h9RwweO.aspx';

    //if(wenjuan_url.includes('/vm/')||wenjuan_url.includes('#')){
    //  wenjuan_url=wenjuan_url.replace("/vm/", "/vj/").split('#')[0];
    //}
    let currentUrl = window.location.href;
    //if(currentUrl.includes('/vm/')||currentUrl.includes('#')){
    //  window.location.href=currentUrl.replace("/vm/", "/vj/").split('#')[0];
    // }

    //------------------------------下边的网址不要改！！！！！！！！！！！！！！！！！！！！
    if (window.location.href.indexOf('https://www.wjx.cn/wjx/join/complete.aspx') != -1) {
        window.location.href = wenjuan_url;
    } else if (window.location.href == wenjuan_url) {
    } else {
        return
    }

    //滚动到末尾
    window.scrollTo(0, document.body.scrollHeight)

    //获取题块列表
    var lists = document.querySelectorAll('.ui-controlgroup')
    var ccc = 0;
    var liangbiao_index = 0;
    var xiala_index = 0;
    var ops;
    var bili;
    var temp_flag;
    var tiankong_list;
    var liangbiao_lists;
    var min_options;

    //1 出生年份 - 2004-2007占70%；2001-2003占12%；2008-2010占18%
    function getBirthYear() {
        var rand = Math.random() * 100;
        if (rand < 70) {
            // 70% 概率：2004-2007
            return Math.floor(Math.random() * 4) + 2004;
        } else if (rand < 82) {
            // 12% 概率：2001-2003
            return Math.floor(Math.random() * 3) + 2001;
        } else {
            // 18% 概率：2008-2010
            return Math.floor(Math.random() * 3) + 2008;
        }
    }
    document.querySelector('#q1').value = getBirthYear();

    //2 性别 - 男生37-45%，女生55-64%（取中间值：男生41%，女生59%）
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    bili = [41, 59];  // 男生41%，女生59%
    ops[danxuan(bili)].click()

    //3 下拉框题
    xiala_click(document.querySelectorAll('.select2-selection.select2-selection--single')[xiala_index])
    xiala_index += 1
    ops = document.querySelectorAll('#select2-q3-results li')
    ops = Array.prototype.slice.call(ops);
    ops = ops.slice(1, ops.length);
    bili = randomBili(ops.length - 1);
    xialaElement_click(ops[danxuan(bili)])

    //4 高考成绩 - A选项约占5%；B选项占30%；C选项约占35%；D选项约占30%
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    bili = [5, 30, 35, 30];  // A:5%, B:30%, C:35%, D:30%
    ops[danxuan(bili)].click()

    //5 高校类型 - A选项约占4%；B选项占16%；C选项约占65%；D选项约占15%
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    bili = [4, 16, 65, 15];  // A:4%, B:16%, C:65%, D:15%
    ops[danxuan(bili)].click()

    //6-8 单选题 (3个单选题)
    for (let i = 6; i <= 8; i++) {
        ops = lists[ccc].querySelectorAll('div')
        ccc += 1
        bili = randomBili(ops.length);
        ops[danxuan(bili)].click()
    }

    //9 兄弟姐妹数量 - 1个比例更多，3个及以上占10%以下
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    // 假设选项是：1个，2个，3个，4个及以上
    // 1个占60%，2个占30%，3个占8%，4个及以上占2%
    bili = [60, 30, 8, 2];
    ops[danxuan(bili)].click()

    //10-11 单选题 (2个单选题 - 父母学历，随机分布)
    for (let i = 10; i <= 11; i++) {
        ops = lists[ccc].querySelectorAll('div')
        ccc += 1
        bili = randomBili(ops.length);
        ops[danxuan(bili)].click()
    }

    //12 父亲工作单位性质 - 从A→D与学费支付能力正相关
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    // 假设A是最不稳定，D是最稳定，按正相关分布
    bili = [15, 25, 35, 25];  // 向稳定方向倾斜
    ops[danxuan(bili)].click()

    //13 母亲工作单位性质 - 从A→D与学费支付能力正相关
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    // 同样向稳定方向倾斜
    bili = [15, 25, 35, 25];
    ops[danxuan(bili)].click()

    //14 家庭年总收入分布
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    // ①3万及以下7%，②3.1-6万18%，③④共30%，⑤⑥⑦共30%，⑧30.1-50万10%，⑨50万以上5%
    bili = [7, 18, 15, 15, 10, 10, 10, 10, 5];  // 重新分配以匹配9个选项
    ops[danxuan(bili)].click()

    //15 家庭经济负担 - 与支付能力负相关，随机分布
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    bili = randomBili(ops.length);  // 保持随机分布
    ops[danxuan(bili)].click()

    //16 填空题 - 学费、住宿费、生活费赋值
    // (1)学费：文史类4000-6000，理工类5000-8000，东部5500-7000，西部3500-5000，艺术类8000-15000，个位数为0
    // (2)住宿费：90%在800-1500，10%在1500-2000，个位数为0
    // (3)生活费：1301-1500占15%，1500-2000占45%，2000-3000占30%，3000以上占5%，剩余5%小于1300或大于3000
    
    function getTuitionFee() {
        // 随机选择专业类型和地区
        let rand = Math.random();
        if (rand < 0.3) {
            // 30% 文史类 4000-6000
            return Math.floor(Math.random() * 21 + 40) * 100;
        } else if (rand < 0.6) {
            // 30% 理工类 5000-8000
            return Math.floor(Math.random() * 31 + 50) * 100;
        } else if (rand < 0.8) {
            // 20% 艺术类 8000-15000
            return Math.floor(Math.random() * 71 + 80) * 100;
        } else if (rand < 0.9) {
            // 10% 东部 5500-7000
            return Math.floor(Math.random() * 16 + 55) * 100;
        } else {
            // 10% 西部 3500-5000
            return Math.floor(Math.random() * 16 + 35) * 100;
        }
    }
    
    function getAccommodationFee() {
        if (Math.random() < 0.9) {
            // 90% 800-1500
            return Math.floor(Math.random() * 8 + 8) * 100;
        } else {
            // 10% 1500-2000
            return Math.floor(Math.random() * 6 + 15) * 100;
        }
    }
    
    function getLivingExpenses() {
        let rand = Math.random() * 100;
        if (rand < 15) {
            // 15% 1301-1500
            return Math.floor(Math.random() * 200 + 1301);
        } else if (rand < 60) {
            // 45% 1500-2000
            return Math.floor(Math.random() * 501 + 1500);
        } else if (rand < 90) {
            // 30% 2000-3000
            return Math.floor(Math.random() * 1001 + 2000);
        } else if (rand < 95) {
            // 5% 3000以上
            return Math.floor(Math.random() * 1000 + 3000);
        } else {
            // 5% 小于1300
            return Math.floor(Math.random() * 500 + 800);
        }
    }

    let q16_parent = document.querySelector('#q16_1').parentElement;
    let q16_labels = q16_parent.querySelectorAll('label');
    let q16_1_inputs = q16_parent.querySelector('#q16_1');
    let q16_2_inputs = q16_parent.querySelector('#q16_2');
    let q16_3_inputs = q16_parent.querySelector('#q16_3');
    
    // 学费赋值
    if (q16_1_inputs) {
        let tuition = getTuitionFee();
        q16_1_inputs.value = tuition;
        if (q16_labels[0]) {
            let span1 = q16_labels[0].querySelector('span.textCont');
            if (span1) span1.textContent = tuition;
        }
    }
    
    // 住宿费赋值
    if (q16_2_inputs) {
        let accommodation = getAccommodationFee();
        q16_2_inputs.value = accommodation;
        if (q16_labels[1]) {
            let span2 = q16_labels[1].querySelector('span.textCont');
            if (span2) span2.textContent = accommodation;
        }
    }
    
    // 生活费赋值
    if (q16_3_inputs) {
        let living = getLivingExpenses();
        q16_3_inputs.value = living;
        if (q16_labels[2]) {
            let span3 = q16_labels[2].querySelector('span.textCont');
            if (span3) span3.textContent = living;
        }
    }
    ccc += 1
    //17 资金来源比例 - 家庭供给64%，奖学金7%，助学金13%，助学贷款13%，勤工助学3%
    let fund_sources = {
        family: 64,      // 家庭供给
        scholarship: 7,  // 奖学金
        grant: 13,       // 助学金
        loan: 13,        // 助学贷款
        work_study: 3    // 勤工助学
    };
    
    let drv17_containers = document.querySelectorAll('#drv17_1, #drv17_2, #drv17_3, #drv17_4, #drv17_5');
    let fund_values = [fund_sources.family, fund_sources.scholarship, fund_sources.grant, fund_sources.loan, fund_sources.work_study];
    
    // 赋值到input元素
    for (let i = 0; i < drv17_containers.length && i < fund_values.length; i++) {
        let input_element = drv17_containers[i].querySelector('input');
        if (input_element) {
            input_element.value = fund_values[i];
            input_element.label = fund_values[i];
        }
    }

    //18 单选题
    ops = lists[13].querySelectorAll('div')
    ccc = 14
    bili = randomBili(ops.length);
    ops[danxuan(bili)].click()

    //19 填空题 - 学费意愿
    function getTuitionFee(currentSchool = true) {
        let tuition;
        if (currentSchool) {
            // 当前学校：4000-20000，下限4000，中位数6000-8000，上限15000-20000
            let rand = Math.random() * 100;
            if (rand < 30) {
                // 30% 较低区间：4000-6000
                tuition = Math.floor(Math.random() * 21 + 40) * 100;
            } else if (rand < 70) {
                // 40% 中位数区间：6000-8000
                tuition = Math.floor(Math.random() * 21 + 60) * 100;
            } else if (rand < 95) {
                // 25% 较高区间：15000-20000
                tuition = Math.floor(Math.random() * 51 + 150) * 100;
            } else {
                // 5% 异常值：8000-15000
                tuition = Math.floor(Math.random() * 71 + 80) * 100;
            }
        } else {
            // 国内前十：10000-50000，下限8000，主力区间20000-40000，上限80000
            let rand = Math.random() * 100;
            if (rand < 10) {
                // 10% 下限区间：8000-20000
                tuition = Math.floor(Math.random() * 121 + 80) * 100;
            } else if (rand < 70) {
                // 60% 主力区间：20000-40000
                tuition = Math.floor(Math.random() * 201 + 200) * 100;
            } else if (rand < 95) {
                // 25% 上限区间：40000-80000
                tuition = Math.floor(Math.random() * 401 + 400) * 100;
            } else {
                // 5% 异常值：超过80000
                tuition = Math.floor(Math.random() * 201 + 800) * 100;
            }
        }
        return tuition;
    }

    let drv19_containers = document.querySelectorAll('#drv19_1, #drv19_2');
    if (drv19_containers[0]) {
        let currentSchoolTuition = getTuitionFee(true);
        let input1 = drv19_containers[0].querySelector('input');
        if (input1) input1.value = currentSchoolTuition;
    }
    if (drv19_containers[1]) {
        let topSchoolTuition = getTuitionFee(false);
        let input2 = drv19_containers[1].querySelector('input');
        if (input2) input2.value = topSchoolTuition;
    }

    //20 单选题 - 学费上涨承受能力
    let divRefTab20 = document.querySelector('#divRefTab20');
    if (divRefTab20) {
        for (let i = 1; i <= 6; i++) {
            let tr_element = divRefTab20.querySelector('#drv20_' + i);
            if (tr_element) {
                let a_elements = tr_element.querySelectorAll('a');
                if (a_elements.length > 0) {
                    // 根据家庭经济情况调整承受能力
                    // 这里简化处理，实际应根据前面题目的家庭收入情况动态调整
                    let random_index = Math.floor(Math.random() * a_elements.length);
                    a_elements[random_index].click();
                }
            }
        }
    }
    //21 单选题 - 学费上涨接受程度
    let divRefTab21 = document.querySelector('#divRefTab21');
    if (divRefTab21) {
        for (let i = 1; i <= 12; i++) {
            let tr_element = divRefTab21.querySelector('#drv21_' + i);
            if (tr_element) {
                let a_elements = tr_element.querySelectorAll('a');
                if (a_elements.length > 0) {
                    // 国内前十(第7-12题)的接受程度普遍高于当前学校(第1-6题)
                    let random_index;
                    if (i <= 6) {
                        // 当前学校：接受程度较低
                        random_index = Math.floor(Math.random() * Math.max(1, Math.floor(a_elements.length * 0.6)));
                    } else {
                        // 国内前十：接受程度较高
                        random_index = Math.floor(Math.random() * Math.max(1, Math.ceil(a_elements.length * 0.4))) + Math.floor(a_elements.length * 0.6);
                    }
                    random_index = Math.min(random_index, a_elements.length - 1);
                    a_elements[random_index].click();
                }
            }
        }
    }

    //22 单选题 - 学费用途了解程度
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    // [1]30%-40%, [2]30%-35%, [3]15%-20%, [4]5%-10%, [5]<5%
    bili = [35, 32, 18, 8, 7]; // 调整为接近要求的占比
    ops[danxuan(bili)].click()


    //23 多选题 - 学费上涨接受原因（最多选三项）
    ops = lists[ccc].querySelectorAll('div');
    ccc += 1
    // [1]4%, [2]15%, [3]20%, [4]23%, [5]13%, [6]10%, [7]3%, [8]12%
    // 调整占比使其和为100%，并确保最多选三项
    let optionProbs = [4, 15, 20, 23, 13, 10, 3, 12];
    let selectedCount = 0;
    let maxSelections = 3;
    
    for (let i = 0; i < ops.length && selectedCount < maxSelections; i++) {
        if (Math.random() * 100 < optionProbs[i]) {
            ops[i].click();
            selectedCount++;
        }
    }
    
    // 确保至少选一项
    if (selectedCount === 0) {
        let randomIndex = Math.floor(Math.random() * ops.length);
        ops[randomIndex].click();
    }

    //24 单选题 - 实际情况调查
    let divRefTab24 = document.querySelector('#divRefTab24');
    let selectedFor28 = false;
    let selectedFor29 = false;
    let selectedFor30 = false;
    
    if (divRefTab24) {
        // 选项1: "是"占60%-75%
        let q24_1 = divRefTab24.querySelector('#drv24_1');
        if (q24_1) {
            let a_elements = q24_1.querySelectorAll('a');
            let isSelected = Math.random() * 100 < 67.5; // 67.5%中间值
            let index = isSelected ? 0 : Math.floor(Math.random() * (a_elements.length - 1)) + 1;
            a_elements[index].click();
        }
        
        // 选项2: "是"占30%-50%
        let q24_2 = divRefTab24.querySelector('#drv24_2');
        if (q24_2) {
            let a_elements = q24_2.querySelectorAll('a');
            let isSelected = Math.random() * 100 < 40; // 40%中间值
            let index = isSelected ? 0 : Math.floor(Math.random() * (a_elements.length - 1)) + 1;
            a_elements[index].click();
        }
        
        // 选项3: "是"占60%-65%
        let q24_3 = divRefTab24.querySelector('#drv24_3');
        if (q24_3) {
            let a_elements = q24_3.querySelectorAll('a');
            let isSelected = Math.random() * 100 < 62.5; // 62.5%中间值
            let index = isSelected ? 0 : Math.floor(Math.random() * (a_elements.length - 1)) + 1;
            a_elements[index].click();
        }
        
        // 选项4: "是"占15%-20%，选择后跳转至28题
        let q24_4 = divRefTab24.querySelector('#drv24_4');
        if (q24_4) {
            let a_elements = q24_4.querySelectorAll('a');
            selectedFor28 = Math.random() * 100 < 17.5; // 17.5%中间值
            let index = selectedFor28 ? 0 : Math.floor(Math.random() * (a_elements.length - 1)) + 1;
            a_elements[index].click();
        }
        
        // 选项5: "是"占10%-15%，选择后跳转至29题
        let q24_5 = divRefTab24.querySelector('#drv24_5');
        if (q24_5) {
            let a_elements = q24_5.querySelectorAll('a');
            selectedFor29 = Math.random() * 100 < 12.5; // 12.5%中间值
            let index = selectedFor29 ? 0 : Math.floor(Math.random() * (a_elements.length - 1)) + 1;
            a_elements[index].click();
        }
        
        // 选项6: "是"占20%-25%，选择后跳转至30题
        let q24_6 = divRefTab24.querySelector('#drv24_6');
        if (q24_6) {
            let a_elements = q24_6.querySelectorAll('a');
            selectedFor30 = Math.random() * 100 < 22.5; // 22.5%中间值
            let index = selectedFor30 ? 0 : Math.floor(Math.random() * (a_elements.length - 1)) + 1;
            a_elements[index].click();
        }
    }

    //25 单选题 - 上大学的原因
    let divRefTab25 = document.querySelector('#divRefTab25');
    if (divRefTab25) {
        // 各选项"很重要"的占比
        let veryImportantProbs = [20, 13, 15, 12, 10, 9, 9, 3, 9];
        
        for (let i = 1; i <= 10; i++) {
            let tr_element = divRefTab25.querySelector('#drv25_' + i);
            if (tr_element) {
                let a_elements = tr_element.querySelectorAll('a');
                if (a_elements.length > 0) {
                    let random_index;
                    if (Math.random() * 100 < veryImportantProbs[i-1]) {
                        // 选择"很重要"
                        random_index = 0;
                    } else {
                        // 随机选择其他选项
                        random_index = Math.floor(Math.random() * (a_elements.length - 1)) + 1;
                    }
                    a_elements[random_index].click();
                }
            }
        }
    }

    //26 单选题 - 起薪水平
    let divRefTab26 = document.querySelector('#divRefTab26');
    if (divRefTab26) {
        for (let i = 1; i <= 8; i++) {
            let tr_element = divRefTab26.querySelector('#drv26_' + i);
            if (tr_element) {
                let a_elements = tr_element.querySelectorAll('a');
                if (a_elements.length > 0) {
                    // 随机分布，理论上与学校层次和专业类型成正比
                    let random_index = Math.floor(Math.random() * a_elements.length);
                    a_elements[random_index].click();
                }
            }
        }
    }

    //27 单选题 - 期望就业部门
    ops = lists[ccc].querySelectorAll('div')
    ccc += 1
    // 政府部门、事业单位薪资略低于外资、国有和私营企业
    // 简化处理，随机选择但偏向于企业
    bili = [15, 20, 25, 20, 15, 5]; // 假设选项顺序为：政府、事业单位、国企、外资、私企、其他
    ops[danxuan(bili)].click()


    //28 填空题
    tiankong_list = ['3800', '5800', '10000'];
    bili = [33, 33, 34];
    document.querySelector('#q28').value = tiankong_list[danxuan(bili)]


    //29 填空题
    tiankong_list = ['3800', '5800', '10000'];
    bili = [33, 33, 34];
    document.querySelector('#q29').value = tiankong_list[danxuan(bili)]

    //30 填空题
    tiankong_list = ['3800', '5800', '10000'];
    bili = [33, 33, 34];
    document.querySelector('#q30').value = tiankong_list[danxuan(bili)]
    //提交函数 - 完整处理流程：点击提交→处理弹窗→安全校验→完成
    let submitCount = 0;
    let verificationHandled = false;
    
    function completeQuestionnaire() {
        console.log('开始提交问卷...');
        
        // 第一步：点击提交按钮
        setTimeout(function () {
            console.log('点击提交按钮');
            document.querySelector('#ctlNext').click();
            
            // 第二步：等待并处理安全校验弹窗
            setTimeout(function () {
                handleSecurityPopup();
            }, 2000);
            
        }, 1000);
    }
    
    function handleSecurityPopup() {
        console.log('处理安全校验弹窗...');
        
        // 查找并点击弹窗的确认按钮
        let popupFound = false;
        
        // 尝试多种方式查找弹窗确认按钮
        let confirmSelectors = [
            '#layui-layer1 .layui-layer-btn0',  // 标准的layui弹窗确认按钮
            '.layui-layer-btn0',                  // 通用确认按钮类
            '//div[contains(@class,"layui-layer-btn")]//a[contains(text(),"确认")]', // XPath方式
            '//button[contains(text(),"确认")]',  // 按钮文本包含确认
            '//button[contains(text(),"重新提交")]', // 按钮文本包含重新提交
            '.layui-layer-page .layui-layer-btn',  // 页面弹窗按钮
            '#layui-layer1 .layui-layer-btn'      // 特定层弹窗按钮
        ];
        
        for (let selector of confirmSelectors) {
            try {
                let confirmButton = null;
                
                if (selector.startsWith('//')) {
                    // XPath选择器
                    let result = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    confirmButton = result.singleNodeValue;
                } else {
                    // CSS选择器
                    confirmButton = document.querySelector(selector);
                }
                
                if (confirmButton && confirmButton.offsetParent !== null) {
                    console.log('找到确认按钮:', selector);
                    confirmButton.click();
                    popupFound = true;
                    
                    // 等待弹窗关闭后处理安全校验
                    setTimeout(function() {
                        handleSecurityVerification();
                    }, 2000);
                    
                    break;
                }
            } catch (e) {
                console.log('选择器失败:', selector, e);
            }
        }
        
        if (!popupFound) {
            console.log('未找到标准弹窗，尝试通用方式...');
            // 尝试查找任何可见的确认按钮
            let allButtons = document.querySelectorAll('button, a');
            for (let btn of allButtons) {
                if ((btn.textContent.includes('确认') || btn.textContent.includes('重新提交')) && 
                    btn.offsetParent !== null && 
                    window.getComputedStyle(btn).display !== 'none') {
                    console.log('找到通用确认按钮');
                    btn.click();
                    popupFound = true;
                    
                    setTimeout(function() {
                        handleSecurityVerification();
                    }, 2000);
                    
                    break;
                }
            }
        }
        
        if (!popupFound) {
            console.log('未找到确认按钮，直接进入安全校验处理');
            handleSecurityVerification();
        }
    }
    
    function handleSecurityVerification() {
        console.log('处理安全校验...');
        
        // 第零步：等待弹窗完全展示，然后主动触发验证机制
        waitForPopupThenTriggerVerification();
    }
    
    // 新增函数：等待弹窗展示完成后再触发验证
    function waitForPopupThenTriggerVerification() {
        console.log('等待验证弹窗完全展示...');
        
        let popupCheckCount = 0;
        let maxPopupChecks = 20; // 最多检查20次（约40秒）
        
        let popupCheckInterval = setInterval(function() {
            popupCheckCount++;
            
            // 检查是否有验证相关的弹窗或元素出现
            let hasVerificationPopup = document.querySelector('#aliyunCaptcha-window-popup') !== null;
            let hasVerificationElements = document.querySelectorAll('[class*="verify"], [class*="captcha"], [class*="check"]').length > 0;
            let hasStartButton = document.querySelector('[class*="start"], [class*="verify"]') !== null;
            
            console.log(`弹窗检查 ${popupCheckCount}: 验证弹窗=${hasVerificationPopup}, 验证元素=${hasVerificationElements}, 开始按钮=${hasStartButton}`);
            
            // 如果检测到验证相关元素，等待它们完全展示
            if (hasVerificationPopup || hasVerificationElements || hasStartButton) {
                console.log('检测到验证相关元素，等待3秒确保完全展示...');
                
                setTimeout(function() {
                    console.log('验证弹窗展示完成，开始触发验证机制...');
                    clearInterval(popupCheckInterval);
                    
                    // 现在可以安全地开始验证流程
                    triggerVerificationMechanism();
                    
                    // 延迟执行后续步骤，确保弹窗完全加载
                    setTimeout(function() {
                        findAndClickStartVerification();
                    }, 2000); // 2秒延迟
                    
                    // 用户要求：弹窗展示完整三秒后触发点击验证
                    setTimeout(function() {
                        console.log('弹窗展示完整3秒后触发点击验证...');
                        handleAliVerification();
                    }, 3000); // 3秒延迟，满足用户要求
                    
                    // 启动验证过程监控
                    startVerificationMonitoring();
                    
                }, 3000); // 等待3秒确保弹窗完全展示
                
                return;
            }
            
            // 如果长时间没有检测到验证元素，也尝试触发验证
            if (popupCheckCount >= maxPopupChecks) {
                console.log('长时间未检测到验证弹窗，尝试直接触发验证机制...');
                clearInterval(popupCheckInterval);
                
                triggerVerificationMechanism();
                setTimeout(findAndClickStartVerification, 2000);
                setTimeout(handleAliVerification, 5000);
            }
            
        }, 2000); // 每2秒检查一次
    }
    
    // 新增函数：持续监控验证过程
    function startVerificationMonitoring() {
        console.log('开始持续监控验证过程...');
        
        let checkInterval = setInterval(function() {
            try {
                // 检查是否已经完成提交
                let successElement = document.querySelector('.success-tip') ||
                                   document.querySelector('.complete-message') ||
                                   document.querySelector('[class*="success"]') ||
                                   document.querySelector('.submit-success') ||
                                   document.querySelector('.finish-tip');
                
                if (successElement && successElement.offsetParent !== null) {
                    console.log('问卷提交成功！');
                    clearInterval(checkInterval);
                    verificationHandled = true;
                    return;
                }
                
                // 检查是否还在验证过程中
                let verifyingElement = document.querySelector('.verifying') ||
                                     document.querySelector('.nc-verifying') ||
                                     document.querySelector('[class*="verif"]');
                
                if (verifyingElement && verifyingElement.offsetParent !== null) {
                    console.log('正在验证中...');
                }
                
            } catch (e) {
                console.log('验证过程检查错误:', e);
            }
            
            submitCount++;
            if (submitCount >= 30) { // 最多检查30次（约60秒）
                clearInterval(checkInterval);
                console.log('验证处理超时');
            }
        }, 2000);
    }
    
    function findAndClickStartVerification() {
        console.log('查找开始智能校验按钮...');
        
        // 多种选择器来查找"开始智能校验"按钮
        let startVerificationSelectors = [
            '//button[contains(text(),"开始智能校验")]',  // XPath：按钮文本包含"开始智能校验"
            '//div[contains(text(),"开始智能校验")]',   // XPath：div文本包含"开始智能校验"
            '//a[contains(text(),"开始智能校验")]',     // XPath：链接文本包含"开始智能校验"
            '[class*="start-verification"]',            // CSS：类名包含start-verification
            '[class*="startVerify"]',                  // CSS：类名包含startVerify
            '[id*="startVerification"]',                // CSS：ID包含startVerification
            '.nc-btn',                                  // CSS：nc-button类
            '.verification-start-btn',                  // CSS：验证开始按钮
            '.start-btn',                               // CSS：开始按钮
            '.smart-verify-btn',                        // CSS：智能验证按钮
            '//button[contains(text(),"验证")]',         // XPath：按钮文本包含"验证"
            '//div[contains(text(),"验证")]',            // XPath：div文本包含"验证"
            '[class*="verify"]',                       // CSS：类名包含verify
            '[class*="captcha"]',                      // CSS：类名包含captcha
            '.btn-primary',                             // CSS：主要按钮
            '.submit-btn'                               // CSS：提交按钮
        ];
        
        for (let selector of startVerificationSelectors) {
            try {
                let startButton = null;
                
                if (selector.startsWith('//')) {
                    // XPath选择器
                    let result = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    startButton = result.singleNodeValue;
                } else {
                    // CSS选择器
                    startButton = document.querySelector(selector);
                }
                
                if (startButton && startButton.offsetParent !== null && 
                    (startButton.textContent.includes('开始智能校验') || 
                     startButton.textContent.includes('开始验证') ||
                     startButton.textContent.includes('智能校验'))) {
                    console.log('找到开始智能校验按钮:', selector);
                    
                    // 模拟人类点击行为
                    simulateHumanClick(startButton);
                    
                    setTimeout(function() {
                        console.log('开始智能校验按钮已点击');
                    }, 1000);
                    
                    return true;
                }
            } catch (e) {
                console.log('开始校验按钮选择器失败:', selector, e);
            }
        }
        
        // 如果没找到特定按钮，尝试通用方式
        console.log('尝试通用方式查找开始按钮...');
        let allButtons = document.querySelectorAll('button, div, a');
        for (let btn of allButtons) {
            if ((btn.textContent.includes('开始智能校验') || 
                 btn.textContent.includes('开始验证') || 
                 btn.textContent.includes('智能校验')) && 
                btn.offsetParent !== null && 
                window.getComputedStyle(btn).display !== 'none') {
                console.log('通过通用方式找到开始智能校验按钮');
                simulateHumanClick(btn);
                return true;
            }
        }
        
        console.log('未找到开始智能校验按钮，可能直接进入验证环节');
        return false;
    }
    
    // 主动触发验证机制
    function triggerVerificationMechanism() {
        console.log('主动触发验证机制...');
        
        // 查找可能触发验证的元素
        let triggerSelectors = [
            '//button[contains(text(),"验证")]',           // XPath：按钮文本包含"验证"
            '//div[contains(text(),"验证")]',              // XPath：div文本包含"验证"
            '//span[contains(text(),"验证")]',             // XPath：span文本包含"验证"
            '[class*="verify"]',                           // CSS：类名包含verify
            '[class*="captcha"]',                        // CSS：类名包含captcha
            '[class*="check"]',                            // CSS：类名包含check
            '[class*="validation"]',                     // CSS：类名包含validation
            '.btn-verify',                                 // CSS：验证按钮
            '.verification-trigger',                       // CSS：验证触发器
            '.captcha-check',                              // CSS：验证码检查
            '#verify-btn',                                 // CSS：验证按钮ID
            '.submit-verify',                              // CSS：提交验证
            '[data-action="verify"]',                    // CSS：数据动作验证
            '[onclick*="verify"]',                         // CSS：点击事件包含verify
            '[onclick*="captcha"]',                      // CSS：点击事件包含captcha
        ];
        
        for (let selector of triggerSelectors) {
            try {
                let triggerElement = null;
                
                if (selector.startsWith('//')) {
                    // XPath选择器
                    let result = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    triggerElement = result.singleNodeValue;
                } else {
                    // CSS选择器
                    triggerElement = document.querySelector(selector);
                }
                
                if (triggerElement && triggerElement.offsetParent !== null) {
                    console.log('找到验证触发元素:', selector);
                    
                    // 先尝试悬停触发
                    let hoverEvent = new MouseEvent('mouseover', {
                        bubbles: true,
                        cancelable: true
                    });
                    triggerElement.dispatchEvent(hoverEvent);
                    
                    setTimeout(() => {
                        // 然后点击触发
                        simulateHumanClick(triggerElement);
                        console.log('已触发验证机制');
                    }, 500);
                    
                    return true;
                }
            } catch (e) {
                console.log('触发验证选择器失败:', selector, e);
            }
        }
        
        // 如果没找到特定触发器，尝试通用方式
        console.log('尝试通用方式触发验证...');
        let allElements = document.querySelectorAll('button, div, span, a, input');
        for (let element of allElements) {
            if ((element.textContent.includes('验证') || 
                 element.textContent.includes('校验') || 
                 element.textContent.includes('确认') ||
                 element.value?.includes('验证') ||
                 element.value?.includes('校验')) && 
                element.offsetParent !== null && 
                window.getComputedStyle(element).display !== 'none') {
                console.log('通过通用方式找到验证触发元素');
                
                // 先悬停再点击
                let hoverEvent = new MouseEvent('mouseover', {
                    bubbles: true,
                    cancelable: true
                });
                element.dispatchEvent(hoverEvent);
                
                setTimeout(() => {
                    simulateHumanClick(element);
                }, 300);
                
                return true;
            }
        }
        
        console.log('未找到验证触发机制，可能验证已自动触发');
        return false;
    }
    
    function handleAliVerification() {
        console.log('处理阿里人机校验（超级增强版验证检测）...');
        
        // 首先检查是否有阿里云弹窗验证码
        let aliyunPopup = document.querySelector('#aliyunCaptcha-window-popup');
        if (aliyunPopup && aliyunPopup.offsetParent !== null) {
            console.log('检测到阿里云验证码弹窗！');
            return handleAliyunPopupVerification(aliyunPopup);
        }
        
        // 检查其他可能的弹窗
        let otherPopups = [
            '.captcha-popup',
            '[class*="captcha-window"]',
            '[class*="verify-popup"]',
            '.modal-captcha',
            '.captcha-modal'
        ];
        
        for (let popupSelector of otherPopups) {
            let popup = document.querySelector(popupSelector);
            if (popup && popup.offsetParent !== null) {
                console.log(`检测到验证码弹窗: ${popupSelector}`);
                return handlePopupVerification(popup);
            }
        }
        
        // 检测标准验证类型
        let verificationType = detectVerificationType();
        console.log('检测到的验证类型:', verificationType);
        
        switch (verificationType) {
            case 'slider':
                return handleSliderVerification();
            case 'checkbox':
                return handleCheckboxVerification();
            case 'image':
                return handleImageVerification();
            case 'text':
                return handleTextVerification();
            default:
                console.log('未识别验证类型，尝试通用处理...');
                return handleUniversalVerification();
        }
    }
    
    // 专门处理阿里云弹窗验证码
    function handleAliyunPopupVerification(popup) {
        console.log('处理阿里云弹窗验证码...');
        
        // 等待弹窗完全加载
        setTimeout(() => {
            console.log('开始分析弹窗内容...');
            
            // 第一步：查找点击式验证元素（用户说"就是点击 不是滑块"）
            let clickSelectors = [
                'input[type="checkbox"]',
                '[class*="checkbox"]',
                '[class*="check"]',
                '[class*="verify"]',
                '[class*="captcha"]',
                '[class*="confirm"]',
                '[class*="agree"]',
                '.verify-btn',
                '.check-btn',
                '.confirm-btn',
                '[data-action="verify"]',
                '[data-action="check"]',
                '[role="checkbox"]',
                '[aria-checked]'
            ];
            
            let verifyElements = [];
            for (let selector of clickSelectors) {
                let elements = popup.querySelectorAll(selector);
                verifyElements.push(...elements);
            }
            
            console.log(`在阿里云弹窗中找到 ${verifyElements.length} 个点击验证元素`);
            
            if (verifyElements.length > 0) {
                // 优先点击第一个可见的验证元素
                for (let element of verifyElements) {
                    if (element.offsetParent !== null) {
                        console.log('点击阿里云弹窗中的验证元素:', element.tagName, element.className);
                        
                        // 多重点击策略
                        clickElementMultipleWays(element);
                        
                        // 等待验证完成
                        setTimeout(() => {
                            checkAliyunPopupResult(popup);
                        }, 3000);
                        
                        return true;
                    }
                }
            } else {
                // 第二步：查找文本中包含验证相关文字的按钮
                let buttons = popup.querySelectorAll('button, div, span, a');
                for (let button of buttons) {
                    let text = button.textContent.toLowerCase();
                    if ((text.includes('验证') || text.includes('确认') || text.includes('同意') || 
                         text.includes('check') || text.includes('verify') || text.includes('confirm')) &&
                        button.offsetParent !== null) {
                        console.log('找到文本验证按钮:', button.textContent);
                        clickElementMultipleWays(button);
                        
                        setTimeout(() => {
                            checkAliyunPopupResult(popup);
                        }, 3000);
                        
                        return true;
                    }
                }
                
                // 第三步：尝试查找滑块（备用方案）
                let sliderElements = popup.querySelectorAll('[class*="slider"], [class*="drag"]');
                if (sliderElements.length > 0) {
                    console.log('在阿里云弹窗中找到滑块验证（备用方案）');
                    return handleSliderInPopup(popup);
                }
                
                // 终极方案：尝试点击弹窗中的任何可点击区域
                console.log('使用终极方案：点击弹窗区域');
                return clickPopupArea(popup);
            }
        }, 2000);
        
        return true;
    }
    
    // 多重点击策略 - 确保点击生效
    function clickElementMultipleWays(element) {
        console.log('执行多重点击策略...');
        
        // 策略1：标准点击
        simulateHumanClick(element);
        
        setTimeout(() => {
            // 策略2：直接触发点击事件
            let clickEvent = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            element.dispatchEvent(clickEvent);
        }, 200);
        
        setTimeout(() => {
            // 策略3：触发change事件（对于checkbox）
            if (element.type === 'checkbox') {
                element.checked = !element.checked;
                let changeEvent = new Event('change', {
                    bubbles: true,
                    cancelable: true
                });
                element.dispatchEvent(changeEvent);
                console.log('触发了checkbox的change事件');
            }
        }, 400);
        
        setTimeout(() => {
            // 策略4：触发input事件
            let inputEvent = new Event('input', {
                bubbles: true,
                cancelable: true
            });
            element.dispatchEvent(inputEvent);
        }, 600);
        
        setTimeout(() => {
            // 策略5：触发focus和blur事件
            element.focus();
            setTimeout(() => {
                element.blur();
            }, 100);
        }, 800);
        
        console.log('多重点击策略执行完成');
    }
    
    // 处理弹窗中的滑块验证
    function handleSliderInPopup(popup) {
        let slider = popup.querySelector('[class*="slider"]') || popup.querySelector('[class*="drag"]');
        if (!slider) return false;
        
        console.log('在弹窗中处理滑块验证...');
        
        // 获取滑块轨道
        let track = popup.querySelector('[class*="track"]') || popup.querySelector('[class*="rail"]') || slider.parentElement;
        if (!track) return false;
        
        let trackRect = track.getBoundingClientRect();
        let sliderRect = slider.getBoundingClientRect();
        
        let distance = trackRect.width - sliderRect.width;
        let startX = sliderRect.left + sliderRect.width / 2;
        let startY = sliderRect.top + sliderRect.height / 2;
        
        // 生成动态轨迹
        let trajectory = generateDynamicTrajectory(startX, startY, distance);
        
        // 在弹窗上下文中执行滑动
        executeTrajectoryInPopup(slider, trajectory);
        
        return true;
    }
    
    // 点击弹窗区域
    function clickPopupArea(popup) {
        console.log('尝试点击弹窗区域...');
        
        let rect = popup.getBoundingClientRect();
        let centerX = rect.left + rect.width / 2;
        let centerY = rect.top + rect.height / 2;
        
        console.log(`弹窗位置: (${rect.left}, ${rect.top}), 大小: ${rect.width}x${rect.height}`);
        
        // 策略1：点击弹窗中心区域（可能包含隐式验证）
        console.log('策略1：点击弹窗中心区域');
        simulateMouseMovement(centerX, centerY);
        
        setTimeout(() => {
            let centerClick = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                clientX: centerX,
                clientY: centerY,
                button: 0
            });
            popup.dispatchEvent(centerClick);
        }, 300);
        
        // 策略2：在弹窗内多点点击（模拟人类寻找验证区域）
        setTimeout(() => {
            console.log('策略2：多点点击弹窗区域');
            for (let i = 0; i < 5; i++) {
                setTimeout(() => {
                    // 在弹窗内随机位置点击
                    let offsetX = (Math.random() - 0.5) * (rect.width * 0.6); // 60%范围内
                    let offsetY = (Math.random() - 0.5) * (rect.height * 0.6);
                    let x = centerX + offsetX;
                    let y = centerY + offsetY;
                    
                    // 确保点击在弹窗内
                    if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
                        simulateMouseMovement(x, y);
                        
                        setTimeout(() => {
                            let clickEvent = new MouseEvent('click', {
                                bubbles: true,
                                cancelable: true,
                                clientX: x,
                                clientY: y,
                                button: 0
                            });
                            popup.dispatchEvent(clickEvent);
                            console.log(`点击弹窗区域 ${i + 1}: (${x}, ${y})`);
                        }, 100);
                    }
                }, i * 400);
            }
        }, 1000);
        
        // 策略3：查找弹窗内的可点击元素并点击
        setTimeout(() => {
            console.log('策略3：点击弹窗内可点击元素');
            let clickableElements = popup.querySelectorAll('div, span, p, img, svg');
            console.log(`找到 ${clickableElements.length} 个潜在可点击元素`);
            
            for (let i = 0; i < Math.min(3, clickableElements.length); i++) {
                let element = clickableElements[i];
                if (element.offsetParent !== null) {
                    let elemRect = element.getBoundingClientRect();
                    let clickX = elemRect.left + elemRect.width / 2;
                    let clickY = elemRect.top + elemRect.height / 2;
                    
                    simulateMouseMovement(clickX, clickY);
                    
                    setTimeout(() => {
                        let clickEvent = new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            clientX: clickX,
                            clientY: clickY,
                            button: 0
                        });
                        element.dispatchEvent(clickEvent);
                        console.log(`点击弹窗内元素 ${i + 1}: ${element.tagName} (${clickX}, ${clickY})`);
                    }, i * 200);
                }
            }
        }, 3000);
        
        return true;
    }
    
    // 检查阿里云弹窗验证结果
    function checkAliyunPopupResult(popup) {
        console.log('检查阿里云弹窗验证结果...');
        
        // 检查弹窗是否关闭或验证成功指示器
        let successIndicators = [
            '[class*="success"]',
            '[class*="complete"]',
            '[class*="verified"]',
            '[style*="display: none"]', // 弹窗隐藏了
            ':not([style*="display: block"])' // 弹窗不显示了
        ];
        
        for (let indicator of successIndicators) {
            try {
                let element = popup.querySelector(indicator);
                if (element || !popup.offsetParent) {
                    console.log('阿里云弹窗验证可能已完成！');
                    return true;
                }
            } catch (e) {
                // 忽略错误
            }
        }
        
        // 如果弹窗还在，可能需要更多操作
        console.log('阿里云弹窗仍在显示，可能需要进一步操作...');
        return false;
    }
    
    // 通用弹窗验证处理
    function handlePopupVerification(popup) {
        console.log('处理通用验证码弹窗...');
        return handleAliyunPopupVerification(popup); // 使用相同的处理逻辑
    }
    
    // 检测验证类型
    function detectVerificationType() {
        console.log('检测验证类型...');
        
        // 滑块验证检测
        let sliderElements = [
            '.nc-slider-button',
            '.slider',
            '[class*="slider"]',
            '.drag-button',
            '.nc-drag-button',
            '#nc_1_n1z',
            '.nc_iconfont.btn_slide'
        ];
        
        for (let selector of sliderElements) {
            let elements = document.querySelectorAll(selector);
            if (elements.length > 0 && elements[0].offsetParent !== null) {
                console.log('检测到滑块验证元素:', selector);
                return 'slider';
            }
        }
        
        // Checkbox验证检测
        let checkboxElements = [
            'input[type="checkbox"]',
            '.nc-checkbox',
            '.checkbox',
            '[class*="checkbox"]',
            '#nc_1__scale_text',
            '.nc_scale'
        ];
        
        for (let selector of checkboxElements) {
            let elements = document.querySelectorAll(selector);
            if (elements.length > 0 && elements[0].offsetParent !== null) {
                console.log('检测到Checkbox验证元素:', selector);
                return 'checkbox';
            }
        }
        
        // 图片验证检测
        let imageElements = [
            '[class*="image-verify"]',
            '[class*="pic-verify"]',
            '.click-verify',
            '.image-captcha'
        ];
        
        for (let selector of imageElements) {
            let elements = document.querySelectorAll(selector);
            if (elements.length > 0 && elements[0].offsetParent !== null) {
                console.log('检测到图片验证元素:', selector);
                return 'image';
            }
        }
        
        // 文本验证检测
        let textElements = [
            '[class*="text-verify"]',
            '[class*="input-verify"]',
            '.geetest_input'
        ];
        
        for (let selector of textElements) {
            let elements = document.querySelectorAll(selector);
            if (elements.length > 0 && elements[0].offsetParent !== null) {
                console.log('检测到文本验证元素:', selector);
                return 'text';
            }
        }
        
        // 通过文本内容检测
        let allElements = document.querySelectorAll('div, span, p, label');
        for (let elem of allElements) {
            let text = (elem.textContent || '').trim();
            if (text.includes('滑块')) return 'slider';
            if (text.includes('checkbox') || text.includes('复选框')) return 'checkbox';
            if (text.includes('图片') || text.includes('图像')) return 'image';
            if (text.includes('输入') || text.includes('文字')) return 'text';
        }
        
        return 'unknown';
    }
    
    function handleCheckboxVerification() {
        console.log('处理Checkbox验证（超级增强版）...');
        
        // 增强版checkbox选择器 - 更全面的元素查找
        let checkboxSelectors = [
            // 标准checkbox选择器
            'input[type="checkbox"]',
            '.nc-checkbox',
            '[class*="checkbox"]',
            
            // 阿里巴巴验证相关
            '.alibaba-checkbox',
            '.ali-checkbox',
            '.verification-checkbox',
            '.smart-verify-checkbox',
            '.captcha-checkbox',
            '.security-checkbox',
            
            // 特定ID和类
            '#nc_1__scale_text',
            '.nc_scale',
            '.nc_wrapper',
            '.nc-container',
            '#verify-checkbox',
            '#captcha-checkbox',
            '#smart-verify',
            
            // 通用包含验证关键字的元素
            '[class*="verify"]',
            '[class*="captcha"]',
            '[class*="security"]',
            '[id*="verify"]',
            '[id*="captcha"]',
            
            // 新增的更具体选择器
            'label[class*="checkbox"]',
            'div[class*="checkbox"]',
            'span[class*="checkbox"]',
            '.checkbox-wrapper',
            '.verify-wrapper',
            '.captcha-wrapper'
        ];
        
        let foundElements = [];
        
        // 首先收集所有可能的元素
        for (let selector of checkboxSelectors) {
            try {
                let elements = [];
                
                if (selector.startsWith('//')) {
                    // XPath选择器
                    let result = document.evaluate(selector, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
                    for (let i = 0; i < result.snapshotLength; i++) {
                        let element = result.snapshotItem(i);
                        if (element && element.offsetParent !== null) {
                            elements.push(element);
                        }
                    }
                } else {
                    // CSS选择器
                    let found = document.querySelectorAll(selector);
                    found.forEach(el => {
                        if (el.offsetParent !== null) {
                            elements.push(el);
                        }
                    });
                }
                
                if (elements.length > 0) {
                    console.log(`选择器 "${selector}" 找到 ${elements.length} 个元素`);
                    foundElements.push(...elements);
                }
            } catch (e) {
                console.log(`选择器错误: ${selector}`, e);
            }
        }
        
        // 通过文本内容查找验证元素
        console.log('通过文本内容查找验证元素...');
        let allElements = document.querySelectorAll('div, span, input, button, label, a');
        for (let elem of allElements) {
            const text = (elem.textContent || '').trim();
            const className = elem.className || '';
            const id = elem.id || '';
            const title = elem.title || '';
            const placeholder = elem.placeholder || '';
            
            if (
                (text.includes('人机验证') || 
                 text.includes('智能验证') || 
                 text.includes('安全验证') ||
                 text.includes('我不是机器人') ||
                 text.includes('点击验证') ||
                 text.includes('进行验证') ||
                 text.includes('checkbox')) ||
                (className.includes('checkbox') || 
                 className.includes('verify') || 
                 className.includes('captcha') ||
                 className.includes('security')) ||
                (id.includes('checkbox') || 
                 id.includes('verify') || 
                 id.includes('captcha')) ||
                (title.includes('验证') ||
                 title.includes('checkbox')) ||
                (placeholder.includes('验证') ||
                 placeholder.includes('checkbox')) ||
                elem.type === 'checkbox'
            ) {
                if (elem.offsetParent !== null && !foundElements.includes(elem)) {
                    foundElements.push(elem);
                    console.log('通过文本找到验证元素:', {
                        tagName: elem.tagName,
                        text: text.substring(0, 50),
                        className: className,
                        id: id
                    });
                }
            }
        }
        
        // 去重并优先处理最可能的元素
        foundElements = Array.from(new Set(foundElements));
        console.log(`总共找到 ${foundElements.length} 个可能的验证元素`);
        
        if (foundElements.length === 0) {
            console.log('未找到验证元素，启动验证重试机制...');
            setTimeout(function() {
                retryVerification(0);
            }, 2000);
            return false;
        }
        
        // 按优先级排序：真正的checkbox > 包含checkbox类的元素 > 其他
        foundElements.sort(function(a, b) {
            const aScore = getElementPriorityScore(a);
            const bScore = getElementPriorityScore(b);
            return bScore - aScore; // 分数高的在前
        });
        
        // 点击前3个最有可能的元素
        let clickCount = 0;
        let maxClicks = Math.min(3, foundElements.length);
        
        function clickNextElement() {
            if (clickCount >= maxClicks) {
                console.log('完成验证元素点击，等待验证结果...');
                setTimeout(function() {
                    checkVerificationResult();
                }, 5000);
                return;
            }
            
            const element = foundElements[clickCount];
            console.log(`点击第 ${clickCount + 1} 个验证元素 (优先级分数: ${getElementPriorityScore(element)})`);
            
            try {
                simulateHumanClick(element);
                clickCount++;
                
                setTimeout(function() {
                    clickNextElement();
                }, 1500);
                
            } catch (e) {
                console.log(`点击第 ${clickCount + 1} 个元素失败:`, e);
                clickCount++;
                clickNextElement();
            }
        }
        
        clickNextElement();
        return true;
    }
    
    // 获取元素的优先级分数
    function getElementPriorityScore(element) {
        let score = 0;
        
        // 是真正的checkbox输入框
        if (element.type === 'checkbox') {
            score += 100;
        }
        
        // 包含关键类名
        const className = element.className || '';
        if (className.includes('checkbox')) score += 50;
        if (className.includes('verify')) score += 30;
        if (className.includes('captcha')) score += 30;
        if (className.includes('security')) score += 20;
        
        // 包含关键ID
        const id = element.id || '';
        if (id.includes('checkbox')) score += 40;
        if (id.includes('verify')) score += 25;
        if (id.includes('captcha')) score += 25;
        
        // 文本内容包含关键词
        const text = (element.textContent || '').trim();
        if (text.includes('人机验证')) score += 60;
        if (text.includes('智能验证')) score += 60;
        if (text.includes('安全验证')) score += 50;
        if (text.includes('我不是机器人')) score += 70;
        
        // 元素可见且可交互
        if (element.offsetParent !== null) score += 10;
        if (element.tagName === 'INPUT') score += 20;
        if (element.tagName === 'BUTTON') score += 15;
        if (element.tagName === 'LABEL') score += 15;
        
        return score;
    }
    
    // 重试验证元素查找
    function retryFindVerificationElements() {
        console.log('重试验证元素查找...');
        
        // 检查是否有iframe，验证可能在iframe中
        let iframes = document.querySelectorAll('iframe');
        console.log(`找到 ${iframes.length} 个iframe`);
        
        if (iframes.length > 0) {
            console.log('检查iframe中的验证元素...');
            for (let i = 0; i < iframes.length; i++) {
                try {
                    let iframeDoc = iframes[i].contentDocument || iframes[i].contentWindow.document;
                    if (iframeDoc) {
                        console.log(`检查第 ${i + 1} 个iframe...`);
                        // 在iframe中查找验证元素
                        let iframeVerification = iframeDoc.querySelector('input[type="checkbox"]') ||
                                               iframeDoc.querySelector('[class*="verify"]') ||
                                               iframeDoc.querySelector('[class*="captcha"]');
                        if (iframeVerification) {
                            console.log('在iframe中找到验证元素！');
                            // 切换到iframe上下文并处理验证
                            setTimeout(() => {
                                handleIframeVerification(iframes[i]);
                            }, 1000);
                            return true;
                        }
                    }
                } catch (e) {
                    console.log(`访问第 ${i + 1} 个iframe失败:`, e);
                }
            }
        }
        
        // 检查是否有shadow DOM
        const allElements = document.querySelectorAll('*');
        let hasShadowRoot = false;
        allElements.forEach(el => {
            if (el.shadowRoot) {
                hasShadowRoot = true;
                console.log('发现shadow root元素');
                // 在shadow DOM中查找验证元素
                let shadowVerification = el.shadowRoot.querySelector('input[type="checkbox"]') ||
                                        el.shadowRoot.querySelector('[class*="verify"]');
                if (shadowVerification) {
                    console.log('在shadow DOM中找到验证元素！');
                    simulateHumanClick(shadowVerification);
                    return true;
                }
            }
        });
        
        if (!hasShadowRoot && iframes.length === 0) {
            console.log('仍未找到验证元素，可能验证已完成或不需要验证');
            return false;
        }
        
        return true;
    }
    
    // 处理iframe中的验证
    function handleIframeVerification(iframe) {
        console.log('处理iframe中的验证...');
        try {
            let iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            if (iframeDoc) {
                // 在iframe上下文中执行验证处理
                let checkbox = iframeDoc.querySelector('input[type="checkbox"]') ||
                              iframeDoc.querySelector('[class*="verify"]');
                if (checkbox) {
                    checkbox.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    setTimeout(() => {
                        checkbox.click();
                        console.log('已点击iframe中的验证元素');
                    }, 1000);
                }
            }
        } catch (e) {
            console.log('处理iframe验证失败:', e);
        }
    }
    
    // 验证失败重试机制
    function retryVerification(attemptCount = 0) {
        const maxAttempts = 3;
        
        if (attemptCount >= maxAttempts) {
            console.log('验证重试次数已达上限，可能验证已完成或不需要验证');
            return false;
        }
        
        console.log(`第 ${attemptCount + 1} 次验证重试...`);
        
        // 等待一段时间后重试
        setTimeout(() => {
            // 重新检测验证类型
            let verificationType = detectVerificationType();
            console.log('重试时检测到的验证类型:', verificationType);
            
            if (verificationType !== 'unknown') {
                // 重新尝试验证
                handleAliVerification();
            } else {
                // 继续重试
                retryVerification(attemptCount + 1);
            }
        }, 3000 + attemptCount * 2000); // 递增等待时间
        
        return true;
    }
    
    function simulateHumanClick(element) {
        // 增强版人类点击模拟 - 更真实的鼠标行为
        console.log('执行增强版人类点击模拟...');
        
        // 滚动到元素位置（平滑滚动）
        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        setTimeout(function() {
            const rect = element.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            // 添加随机偏移，模拟人类不精确的点击
            const offsetX = (Math.random() - 0.5) * 20;
            const offsetY = (Math.random() - 0.5) * 20;
            const x = centerX + offsetX;
            const y = centerY + offsetY;
            
            // 模拟鼠标移动轨迹
            simulateMouseMovement(x, y);
            
            setTimeout(function() {
                // 创建完整的鼠标事件序列 - 更接近真实用户行为
                const events = [
                    new MouseEvent('mouseover', {
                        bubbles: true,
                        cancelable: true,
                        clientX: x,
                        clientY: y,
                        button: 0
                    }),
                    new MouseEvent('mouseenter', {
                        bubbles: true,
                        cancelable: true,
                        clientX: x,
                        clientY: y,
                        button: 0
                    }),
                    new MouseEvent('mousedown', {
                        bubbles: true,
                        cancelable: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 1
                    }),
                    new MouseEvent('mouseup', {
                        bubbles: true,
                        cancelable: true,
                        clientX: x,
                        clientY: y,
                        button: 0,
                        buttons: 0
                    }),
                    new MouseEvent('click', {
                        bubbles: true,
                        cancelable: true,
                        clientX: x,
                        clientY: y,
                        button: 0
                    })
                ];
                
                // 按顺序触发事件，模拟真实点击节奏
                events.forEach(function(event, index) {
                    setTimeout(function() {
                        element.dispatchEvent(event);
                        if (index === events.length - 1) {
                            console.log('增强版点击完成');
                        }
                    }, index * 50);
                });
                
            }, 500 + Math.random() * 1000); // 随机延迟，模拟人类思考时间
            
        }, 1000);
    }
    
    // 模拟鼠标移动轨迹（动态算法）
    function simulateMouseMovement(targetX, targetY) {
        // 动态参数生成
        const steps = 8 + Math.floor(Math.random() * 15); // 8-22步随机
        const speedVariation = 0.5 + Math.random() * 1.0; // 0.5-1.5倍速度变化
        const curveIntensity = Math.random() * 20 - 10; // -10到+10像素的曲线强度
        const hesitationProbability = 0.3; // 30%概率出现犹豫
        
        let currentX = Math.random() * window.innerWidth;
        let currentY = Math.random() * window.innerHeight;
        
        // 生成动态轨迹点
        const trajectory = [];
        let hesitationPoints = [];
        
        // 随机生成犹豫点
        if (Math.random() < hesitationProbability) {
            const hesitationCount = 1 + Math.floor(Math.random() * 2);
            for (let i = 0; i < hesitationCount; i++) {
                hesitationPoints.push(Math.floor(Math.random() * (steps - 2)) + 1);
            }
        }
        
        for (let i = 0; i <= steps; i++) {
            const progress = i / steps;
            
            // 基础线性插值
            let nextX = currentX + (targetX - currentX) * progress;
            let nextY = currentY + (targetY - currentY) * progress;
            
            // 添加贝塞尔曲线效果
            if (curveIntensity !== 0) {
                const curve = Math.sin(progress * Math.PI) * curveIntensity;
                nextX += curve * (1 - progress); // 接近目标时曲线效果减弱
            }
            
            // 添加随机抖动（模拟人类手抖）
            const jitterX = (Math.random() - 0.5) * 5;
            const jitterY = (Math.random() - 0.5) * 5;
            nextX += jitterX;
            nextY += jitterY;
            
            // 处理犹豫点
            let stepDelay = (30 + Math.random() * 40) / speedVariation;
            
            if (hesitationPoints.includes(i)) {
                // 在犹豫点附近小幅度回退
                const backtrackX = (Math.random() - 0.5) * 15;
                const backtrackY = (Math.random() - 0.5) * 15;
                nextX += backtrackX;
                nextY += backtrackY;
                stepDelay *= 2.5; // 犹豫点延迟增加
                
                // 添加额外的轨迹点来模拟犹豫
                trajectory.push({
                    x: nextX,
                    y: nextY,
                    delay: stepDelay + Math.random() * 100
                });
            }
            
            // 起始和结束阶段减速（模拟人类行为）
            if (i < 2 || i > steps - 2) {
                stepDelay *= 1.8;
            }
            
            trajectory.push({
                x: nextX,
                y: nextY,
                delay: stepDelay
            });
        }
        
        // 执行动态轨迹
        executeMouseTrajectory(trajectory);
    }
    
    // 执行鼠标轨迹
    function executeMouseTrajectory(trajectory) {
        let index = 0;
        
        function executeNextMove() {
            if (index >= trajectory.length) {
                return; // 轨迹完成
            }
            
            const point = trajectory[index];
            
            const moveEvent = new MouseEvent('mousemove', {
                bubbles: true,
                cancelable: true,
                clientX: point.x,
                clientY: point.y,
                button: 0
            });
            
            document.dispatchEvent(moveEvent);
            index++;
            
            setTimeout(executeNextMove, point.delay);
        }
        
        executeNextMove();
    }
    
    function checkVerificationResult() {
        console.log('检查验证结果...');
        
        // 检查验证是否成功
        let successIndicators = [
            '.nc-success',                          // 验证成功
            '[class*="success"]',                   // 包含success的元素
            '.verification-success',                // 验证成功
            '.validate-success',                    // 校验成功
            '//div[contains(@class,"success")]',    // XPath：包含success的div
            '//span[contains(text(),"验证成功")]',   // XPath：文本包含验证成功
            '//div[contains(text(),"验证成功")]'     // XPath：文本包含验证成功
        ];
        
        for (let selector of successIndicators) {
            try {
                let successElement = null;
                
                if (selector.startsWith('//')) {
                    let result = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
                    successElement = result.singleNodeValue;
                } else {
                    successElement = document.querySelector(selector);
                }
                
                if (successElement && successElement.offsetParent !== null) {
                    console.log('验证成功！');
                    return true;
                }
            } catch (e) {
                // 忽略错误，继续检查
            }
        }
        
        console.log('验证结果检查完成');
        return false;
    }
    
    function handleImageVerification() {
        console.log('处理图片验证...');
        
        // 图片验证通常需要点击特定图片
        let imageSelectors = [
            '[class*="image-verify"]',
            '[class*="pic-verify"]',
            '.click-verify',
            '.image-captcha',
            '[class*="captcha-image"]',
            '.verify-image'
        ];
        
        let foundImages = [];
        for (let selector of imageSelectors) {
            let elements = document.querySelectorAll(selector);
            elements.forEach(el => {
                if (el.offsetParent !== null) {
                    foundImages.push(el);
                }
            });
        }
        
        if (foundImages.length === 0) {
            console.log('未找到图片验证元素');
            return false;
        }
        
        console.log(`找到 ${foundImages.length} 个图片验证元素`);
        
        // 随机点击一些图片（模拟人类行为）
        let clickCount = Math.min(2, foundImages.length);
        for (let i = 0; i < clickCount; i++) {
            setTimeout(() => {
                let randomIndex = Math.floor(Math.random() * foundImages.length);
                simulateHumanClick(foundImages[randomIndex]);
            }, i * 1000);
        }
        
        return true;
    }
    
    function handleTextVerification() {
        console.log('处理文本验证...');
        
        // 查找文本输入框
        let textInputs = document.querySelectorAll('input[type="text"]');
        let verifyInputs = [];
        
        textInputs.forEach(input => {
            let className = input.className || '';
            let id = input.id || '';
            let placeholder = input.placeholder || '';
            
            if (className.includes('verify') || 
                id.includes('verify') || 
                placeholder.includes('验证') ||
                placeholder.includes('请输入')) {
                verifyInputs.push(input);
            }
        });
        
        if (verifyInputs.length === 0) {
            console.log('未找到文本验证输入框');
            return false;
        }
        
        // 模拟输入常见验证文本
        let commonTexts = ['1234', 'abcd', '验证', 'test'];
        verifyInputs.forEach((input, index) => {
            setTimeout(() => {
                let randomText = commonTexts[Math.floor(Math.random() * commonTexts.length)];
                input.value = randomText;
                input.dispatchEvent(new Event('input', { bubbles: true }));
                console.log(`输入文本验证: ${randomText}`);
            }, index * 500);
        });
        
        return true;
    }
    
    function handleUniversalVerification() {
        console.log('处理通用验证（终极方案）...');
        
        // 终极方案：尝试页面上所有可能的可点击元素
        let allElements = document.querySelectorAll('div, span, button, a, label, input');
        let clickableElements = [];
        
        allElements.forEach(el => {
            if (el.offsetParent !== null) {
                let rect = el.getBoundingClientRect();
                if (rect.width > 20 && rect.height > 20 && rect.width < 200 && rect.height < 100) {
                    // 过滤掉太小或太大的元素
                    clickableElements.push(el);
                }
            }
        });
        
        console.log(`找到 ${clickableElements.length} 个可能的可点击元素`);
        
        // 按位置排序，优先点击页面中央附近的元素
        clickableElements.sort((a, b) => {
            let rectA = a.getBoundingClientRect();
            let rectB = b.getBoundingClientRect();
            
            let centerX = window.innerWidth / 2;
            let centerY = window.innerHeight / 2;
            
            let distA = Math.sqrt(Math.pow(rectA.left + rectA.width/2 - centerX, 2) + Math.pow(rectA.top + rectA.height/2 - centerY, 2));
            let distB = Math.sqrt(Math.pow(rectB.left + rectB.width/2 - centerX, 2) + Math.pow(rectB.top + rectB.height/2 - centerY, 2));
            
            return distA - distB; // 距离小的在前
        });
        
        // 点击前5个最可能的元素
        let maxAttempts = Math.min(5, clickableElements.length);
        for (let i = 0; i < maxAttempts; i++) {
            setTimeout(() => {
                console.log(`通用验证：尝试点击第 ${i + 1} 个元素`);
                simulateHumanClick(clickableElements[i]);
            }, i * 1000);
        }
        
        return true;
    }
    
    // 在弹窗上下文中执行轨迹
    function executeTrajectoryInPopup(slider, trajectory) {
        console.log('在弹窗中执行轨迹滑动...');
        
        let index = 0;
        
        function executeNextPopupMove() {
            if (index >= trajectory.length) {
                console.log('弹窗轨迹执行完成');
                
                // 等待验证结果
                setTimeout(() => {
                    checkAliyunPopupResult(slider.closest('#aliyunCaptcha-window-popup') || document.querySelector('#aliyunCaptcha-window-popup'));
                }, 2000);
                
                return;
            }
            
            const point = trajectory[index];
            
            // 创建鼠标事件 - 在弹窗上下文中
            const mouseMove = new MouseEvent('mousemove', {
                bubbles: true,
                cancelable: true,
                clientX: point.x,
                clientY: point.y,
                button: 0,
                buttons: 1
            });
            
            slider.dispatchEvent(mouseMove);
            
            index++;
            
            setTimeout(() => {
                executeNextPopupMove();
            }, point.delay);
        }
        
        // 开始拖拽
        const mouseDown = new MouseEvent('mousedown', {
            bubbles: true,
            cancelable: true,
            clientX: trajectory[0].x,
            clientY: trajectory[0].y,
            button: 0,
            buttons: 1
        });
        
        slider.dispatchEvent(mouseDown);
        
        setTimeout(() => {
            executeNextPopupMove();
        }, 100);
    }
    
    function handleSliderVerification() {
        console.log('处理滑块验证（动态轨迹算法）...');
        
        // 查找滑块元素
        let slider = document.querySelector('.nc-slider-button') ||
                    document.querySelector('.slider') ||
                    document.querySelector('[class*="slider-button"]') ||
                    document.querySelector('.drag-button') ||
                    document.querySelector('[class*="drag"]');
        
        if (slider) {
            console.log('找到滑块，启动动态轨迹滑动算法...');
            
            const rect = slider.getBoundingClientRect();
            const startX = rect.left + rect.width / 2;
            const startY = rect.top + rect.height / 2;
            
            // 动态计算滑动距离（250-350像素之间随机）
            const baseDistance = 250 + Math.random() * 100;
            
            // 生成动态滑动轨迹
            const trajectory = generateDynamicTrajectory(startX, startY, baseDistance);
            
            console.log(`生成动态轨迹：${trajectory.length}个点，总距离：${baseDistance.toFixed(1)}像素`);
            
            // 模拟真实鼠标按下
            const mouseDown = new MouseEvent('mousedown', {
                bubbles: true,
                cancelable: true,
                clientX: startX,
                clientY: startY,
                button: 0,
                buttons: 1
            });
            
            slider.dispatchEvent(mouseDown);
            
            // 执行动态轨迹滑动
            executeDynamicTrajectory(trajectory, slider);
            
        } else {
            console.log('未找到滑块元素，尝试其他验证方式...');
        }
    }
    
    // 生成动态滑动轨迹
    function generateDynamicTrajectory(startX, startY, distance) {
        const trajectory = [];
        const steps = 15 + Math.floor(Math.random() * 15); // 15-30步随机
        
        // 添加随机因素使每次轨迹不同
        const speedVariation = 0.3 + Math.random() * 0.4; // 0.3-0.7倍速度变化
        const curveIntensity = Math.random() * 30 - 15; // -15到+15像素的曲线强度
        const hesitationPoints = Math.floor(Math.random() * 3); // 0-2个犹豫点
        
        let currentX = startX;
        let currentY = startY;
        let hesitationIndices = [];
        
        // 随机选择犹豫点位置
        for (let i = 0; i < hesitationPoints; i++) {
            hesitationIndices.push(Math.floor(Math.random() * (steps - 2)) + 1);
        }
        
        for (let i = 0; i <= steps; i++) {
            const progress = i / steps;
            
            // 基础线性移动
            let targetX = startX + (distance * progress);
            let targetY = startY;
            
            // 添加曲线运动（贝塞尔曲线效果）
            if (curveIntensity !== 0) {
                const curve = Math.sin(progress * Math.PI) * curveIntensity;
                targetY += curve;
            }
            
            // 添加随机抖动（模拟人类手抖）
            const jitterX = (Math.random() - 0.5) * 3;
            const jitterY = (Math.random() - 0.5) * 3;
            targetX += jitterX;
            targetY += jitterY;
            
            // 处理犹豫点（停顿和回退）
            if (hesitationIndices.includes(i)) {
                // 在犹豫点添加回退动作
                const backtrack = -5 - Math.random() * 10;
                targetX += backtrack;
                
                // 添加额外的轨迹点来模拟犹豫
                trajectory.push({
                    x: targetX,
                    y: targetY,
                    delay: 100 + Math.random() * 200 // 额外延迟100-300ms
                });
            }
            
            // 计算步间延迟（模拟人类速度变化）
            let stepDelay = (20 + Math.random() * 30) / speedVariation;
            
            // 在滑动开始和结束时减慢速度
            if (i < 3 || i > steps - 3) {
                stepDelay *= 1.5; // 开始和结束阶段减慢50%
            }
            
            trajectory.push({
                x: targetX,
                y: targetY,
                delay: stepDelay
            });
        }
        
        return trajectory;
    }
    
    // 执行动态轨迹
    function executeDynamicTrajectory(trajectory, slider) {
        let index = 0;
        
        function executeNextPoint() {
            if (index >= trajectory.length) {
                // 轨迹执行完成，模拟鼠标释放
                const lastPoint = trajectory[trajectory.length - 1];
                
                const mouseUp = new MouseEvent('mouseup', {
                    bubbles: true,
                    cancelable: true,
                    clientX: lastPoint.x,
                    clientY: lastPoint.y,
                    button: 0,
                    buttons: 0
                });
                
                slider.dispatchEvent(mouseUp);
                console.log('动态轨迹滑动完成！');
                
                // 检查验证结果
                setTimeout(function() {
                    checkVerificationResult();
                }, 1000);
                
                return;
            }
            
            const point = trajectory[index];
            
            // 创建鼠标移动事件
            const mouseMove = new MouseEvent('mousemove', {
                bubbles: true,
                cancelable: true,
                clientX: point.x,
                clientY: point.y,
                button: 0,
                buttons: 1
            });
            
            // 移动鼠标
            document.dispatchEvent(mouseMove);
            
            index++;
            
            // 设置下一步的延迟
            setTimeout(executeNextPoint, point.delay);
        }
        
        // 开始执行轨迹
        executeNextPoint();
    }
    
    // 启动提交流程
    completeQuestionnaire();

    /*
        //---------------------------------------------------------------------------------------------------
    
        //单选题模板
        ops = lists[ccc].querySelectorAll('li')
        ccc+=1
        bili = [];
        ops[danxuan(bili)].click()
    
        //---------------------------------------------------------------------------------------------------
    
        //多选题模板（至少选一个选项）
        ops = lists[ccc].querySelectorAll('li')
        ccc+=1
        bili = [];
        temp_flag = false
    
        while(!temp_flag){
            for(let count = 0;count<bili.length;count++){
                if(duoxuan(bili[count])){
                    ops[count].click();
                    temp_flag = true;
                }
            }
        }
    
        //---------------------------------------------------------------------------------------------------
    
        //多选题模板（可自定义至少选一个选项）
        ops = lists[ccc].querySelectorAll('li');
        ccc+=1;
        bili = [];
        min_options = 3  //设置最少选择的项数
        temp_flag = 0;
        while(temp_flag<min_options){
            let temp_answer = []
            for(let count = 0;count<bili.length;count++){
                if(duoxuan(bili[count])){
                    temp_answer.push(count)
                    temp_flag+=1
                }
                if(count==bili.length-1){
                    if(temp_flag<min_options){
                        temp_flag = 0
                    }
                    else{
                        for(let count = 0;count<temp_answer.length;count++){
                            ops[temp_answer[count]].click();
                        }
                    }
                }
            }
        }
    
        //---------------------------------------------------------------------------------------------------
    
        //填空题模板（固定答案）
        document.querySelector('#q题号').value='自定义答案'
    
        //---------------------------------------------------------------------------------------------------
    
        //填空题模板（多个答案，可定制比例）
        tiankong_list = ['王翠花','小明','小红'];
        bili = [33,33,34];
        document.querySelector('#q题号').value=tiankong_list[danxuan(bili)]
    
        //---------------------------------------------------------------------------------------------------
    
        //单选的量表题模板
        liangbiao_lists = document.querySelectorAll('#div题号 tbody tr')
        liangbiao_index=0
        //题号-1
        ops = liangbiao_lists[liangbiao_index].querySelectorAll('td')
        liangbiao_index+=1
        bili = [20,20,20,20,20];
        ops[danxuan(bili)].click()
    
        //---------------------------------------------------------------------------------------------------
    
        //多选的量表题模板
        liangbiao_lists = document.querySelectorAll('#div题号 tbody tr')
        liangbiao_index=0
        //题号-1
        ops = liangbiao_lists[liangbiao_index].querySelectorAll('td')
        liangbiao_index+=1
        bili = [50,50,50,50];
        temp_flag = false
        while(!temp_flag){
            for(let count = 0;count<bili.length;count++){
                if(duoxuan(bili[count])){
                    ops[count].click();
                    temp_flag = true;
                }
            }
        }
    
        //---------------------------------------------------------------------------------------------------
    
        //下拉框题模板
        xiala_click(document.querySelectorAll('.select2-selection.select2-selection--single')[xiala_index])
        xiala_index+=1
        ops = document.querySelectorAll('#select2-q题号-results li')
        ops = Array.prototype.slice.call(ops); //非ie浏览器正常
        ops = ops.slice(1,ops.length);
        bili = randomBili(ops.length-1);//默认所有选项平均分配
        xialaElement_click(ops[danxuan(bili)])
    
        //---------------------------------------------------------------------------------------------------
    
        /*
        //点击提交按钮
        setTimeout( function(){
            //document.querySelector('#submit_button').click()
            var ev = document.createEvent('HTMLEvents');
            ev.clientX = 20
            ev.clientY = 20
            ev.initEvent('click', false, true);
            document.querySelector('#submit_button').dispatchEvent(ev)
        }, 3 * 1000 );
    */
    //===========================结束==============================
    //返回随机bili 参数为随机个数
    function randomBili(num) {
        let a = Math.floor(100 / num);
        let yu = 100 - a * num;
        let list = [];
        for (let i = 0; i < num; i++) {
            list.push(a)
        }
        for (let i = 0; i < yu; i++) {
            list[i] = list[i] + 1
        }
        return list;
    }
    //累加list前num数的和
    function leijia(list, num) {
        var sum = 0
        for (var i = 0; i < num; i++) {
            sum += list[i];
        }
        return sum;
    }

    //生成从minNum到maxNum的随机数
    function randomNum(minNum, maxNum) {
        switch (arguments.length) {
            case 1:
                return parseInt(Math.random() * minNum + 1, 10);
                break;
            case 2:
                return parseInt(Math.random() * (maxNum - minNum + 1) + minNum, 10);
                break;
            default:
                return 0;
                break;
        }
    }
    //判断num是否在指定区间内
    function isInRange(num, start, end) {
        if (num >= start && num <= end) {
            return true;
        } else {
            return false;
        }
    }
    //单选题执行函数
    function danxuan(bili) {
        var pp = randomNum(1, 100)
        for (var i = 1; i <= bili.length; i++) {
            var start = 0;
            if (i != 1) {
                start = leijia(bili, i - 1)
            }
            var end = leijia(bili, i);
            if (isInRange(pp, start, end)) {
                return i - 1;
                break;
            }
        }
    }
    //多选题执行函数
    function duoxuan(probability) {
        var flag = false;
        var i = randomNum(1, 100);
        if (isInRange(i, 1, probability)) {
            flag = true;
        }
        return flag;
    }

    //清楚cookie
    function clearCookie() {
        var keys = document.cookie.match(/[^ =;]+(?=\=)/g);
        if (keys) {
            for (var i = keys.length; i--;) {
                document.cookie = keys[i] + '=0;path=/;expires=' + new Date(0).toUTCString();//清除当前域名下的,例如：m.kevis.com
                document.cookie = keys[i] + '=0;path=/;domain=' + document.domain + ';expires=' + new Date(0).toUTCString();//清除当前域名下的，例如 .m.kevis.com
                document.cookie = keys[i] + '=0;path=/;domain=kevis.com;expires=' + new Date(0).toUTCString();//清除一级域名下的或指定的，例如 .kevis.com
            }
        }
    }
    //滑动验证函数
    function yanzhen() {
        var event = document.createEvent('MouseEvents');
        event.initEvent('mousedown', true, false);
        document.querySelector("#nc_1_n1z").dispatchEvent(event);
        event = document.createEvent('MouseEvents');
        event.initEvent('mousemove', true, false);
        Object.defineProperty(event, 'clientX', { get() { return 260; } })
        document.querySelector("#nc_1_n1z").dispatchEvent(event);
    }

    //滚动到末尾函数
    function scrollToBottom() {
        (function () {
            var y = document.body.scrollTop;
            var step = 500;
            window.scroll(0, y);
            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 50);
                }
                else {
                    window.scroll(0, y);
                    document.title += "scroll-done";
                }
            }
            setTimeout(f, 1000);
        })();
    }

    //点击下拉框方法
    function xiala_click(e) {
        let fireOnThis = e;
        let evObj = document.createEvent('MouseEvents');
        evObj.initMouseEvent('mousedown', true, true, this, 1, 12, 345, 7, 220, false, false, true, false, 0, null);
        fireOnThis.dispatchEvent(evObj);

    }

    //点击下拉框中的选项方法
    function xialaElement_click(e) {
        let fireOnThis = e;
        let evObj = document.createEvent('MouseEvents');
        evObj.initMouseEvent('mouseup', true, true, this, 1, 12, 345, 7, 220, false, false, true, false, 0, null);
        fireOnThis.dispatchEvent(evObj);
    }
})();