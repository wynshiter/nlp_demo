#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
'''
@Author  :   {SEASON}
@License :   (C) Copyright 2013-2022, {OLD_IT_WANG}
@Contact :   {shiter@live.cn}
@Software:   PyCharm
@File    :   NLP_DEMO -- pkuseg
@Time    :   2019/7/18 9:10
@Desc    :

'''
#-------------------------------------------------------------------------------


import pkuseg

seg = pkuseg.pkuseg(model_name='medicine',postag=True)  # 程序会自动下载所对应的细领域模型
text = seg.cut('乙肝大三阳冠心病都是慢性病')              # 进行分词

string_冠心病 = '''冠状动脉粥样硬化性心脏病是冠状动脉血管发生动脉粥样硬化病变而引起血管腔狭窄或阻塞，
造成心肌缺血、缺氧或坏死而导致的心脏病，常常被称为“冠心病”。但是冠心病的范围可能更广泛，还包括炎症、栓塞等导致管腔狭窄或闭塞。世界卫生组织将冠心病分为5大类
：无症状心肌缺血（隐匿性冠心病）、心绞痛、心肌梗死、缺血性心力衰竭（缺血性心脏病）和猝死5种临床类型。临床中常常分为稳定性冠心病和急性冠状动脉综合征。'''

print(text)
print(seg.cut(string_冠心病))



# seg = pkuseg.pkuseg(postag=True)  # 开启词性标注功能
# text = seg.cut('我爱北京天安门')    # 进行分词和词性标注
# print(text)