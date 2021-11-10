'''
Date: 2021-11-10 22:30:51
LastEditors: Guo Yuqin,12032421@mail.sustech.edu.cn
LastEditTime: 2021-11-10 22:32:56
FilePath: /servoDogVersion1.0/servodogVersion2.0/test_method.py
'''

from enum import Enum

Power = Enum("Power",([0.2,0.5]))

print(Power(1))