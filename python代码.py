from math import nan
from operator import index
from turtle import fill, forward

from networkx import reverse
import pandas as pd
import numpy as np
'''
practice1:创建series

import pandas as pd
import numpy as np
#方法1：列表创建
s = pd.Series([1, 2, 3], index = ['a', 'b', 'c'])
print(s)
#方法2: 字典创建
s = pd.Series({'a' : 1, 'b' : 2, 'c' : 3})
print(s)
#与numpy一起使用创建series
s = pd.Series(np.arange(1, 5), index = np.arange(0, 4))
print(s)
#自定义索引
s = pd.Series(np.zeros(5), index = np.arange(1, 6))
print(s)
'''

'''
practice2:创建series

import pandas as pd
import numpy as np
s = pd.Series(np.arange(10, 60, 10), index = ['a', 'b', 'c', 'd', 'e'values], name = 'my_series', dtype=float)
print(s)
'''

'''
practice3:查看series的属性

import pandas as pd
s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
print(s.values, s.index, s.shape, s.size, s.dtype, s.name)
'''

'''
practice4:位置索引和标签索引

import pandas as pd
s = pd.Series([10, 20, 30, 40, 50], index=['a', 'b', 'c', 'd', 'e'])
print(s.iloc[2])
print(s.loc['c'])
print(s.iloc[1:4])
print(s.loc['b' : 'd'])
print(s.tail(2))
print(s.head(3))
'''

'''
practice5:布尔索引

import pandas as pd
s = pd.Series([15, 25, 35, 45, 55, 65, 75, 85, 95])
print(s[s > 50])
print(s[(s >= 30) & (s <= 70)])
print(s[s % 2 == 0])
print(s[s % 5 == 0])
'''

'''
practice6:head和tail

s = pd.Series(range(1, 101))
print(s.head())
print(s.head(10))
print(s.tail())
print(s.tail(8))
'''

'''
practice7:检测缺失值

s = pd.Series([1, None, np.nan, 4, pd.NA, 6, None, 8])
print(s[s.isna()].index)
print(s[s.isna()].size)
print(s.count())
print(s[s.isna()].size / s.size)
'''

'''
practice8:填充缺失值

s = pd.Series([10, None, 30, None, 50, None, 70])
print(s.fillna(0))
print(s.ffill())
print(s.bfill())
print(s.fillna(s.mean()))
print(s.fillna(s.median()))
'''

'''
practice9:

s = pd.Series([1, None, 3, np.nan, 5, None, 7, 8])
print(s.dropna())
s_dropped = s.dropna()
print(s_dropped.reset_index(drop=True))
print(s.dropna(inplace=True))
'''

'''
practice10:基本运算

s1 = pd.Series([1, 2, 3, 4, 5])
s2 = pd.Series([5, 4, 3, 2, 1])
print(s1 + s2)
print(s1 - s2)
print(s1 * s2)
print(s1 / s2)
print(s1 ** 2)
print(np.sqrt(s1))
'''

'''
practice11:统计方法

s = pd.Series([15, 25, 35, 45, 55, 65, 75, 85, 95])
print(s.sum())
print(s.mean())
print(s.median())
print(s.std())
print(s.var())
print(s.max())
print(s.min())
print(s.argmin())
print(s.argmax())
print(s.cumsum()) #累计和：求出当前位置之前（包括当前位置）所有元素的和
'''

'''
practice12:value_counts和unique

s = pd.Series(['A', 'B', 'A', 'C', 'B', 'A', 'D', 'C', 'A', 'B'])
print(s.value_counts())
print(s.nunique())
print(s.value_counts())
print(s.value_counts() / s.count())
print(s.mode())
'''

'''
practice13:数据标准化

s = pd.Series([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
s_mean = s.mean()
s_std = s.std()
s_max = s.max()
s_min = s.min()
print((s - s_mean) / s_std)
print((s - s_min) / (s_max - s_min))
s1 = (s - s_mean) / s_std
print(s1.mean(), s1.std())
'''

'''
practice14:where的使用

s = pd.Series([10, 25, 33, 48, 52, 67, 74, 89, 95])
print(np.where(s < 30, 0, s))
print(np.where(s > 80, 100, s))
print(np.where((s > 30) & (s < 60), 50, s))
print(np.where(s >= 60, '及格', '不及格'))
'''

s = pd.Series([85, 92, 78, 95, 88, 92, 76, 89, 95, 84])
print(s.sort_values())
print(s.sort_values(ascending= False)) #降序排序
print(s.sort_index())


