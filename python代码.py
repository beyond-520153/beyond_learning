from itertools import count
from math import inf
from tkinter import Variable

import pandas as pd
import numpy as np

# 创建示例 CSV 文件
df = pd.DataFrame({
    '员工ID': [101, 102, 103, 104, 105, 106],
    '姓名': ['张三', '李四', '王五', '赵六', '钱七', '孙八'],
    '部门': ['销售部', '技术部', '销售部', '技术部', '市场部', '市场部'],
    '工资': [8000, 12000, None, 15000, 9000, None],
    '入职日期': ['2020-01-15', '2019-03-20', '2021-06-10', '2018-11-01', '2022-02-28', '2020-08-15'],
    '绩效分': ['A', 'B', 'A', 'C', 'B', 'A'],
    '加班时长': [20, 35, 15, None, 25, 30]
})

df.to_csv('book_report.csv', index=False, encoding='utf-8-sig')
content = pd.read_csv('book_report.csv')

'''
practice1:数据导入和查看

# 1.1 读取 employees.csv 文件
# 1.2 显示前3行数据
# 1.3 显示数据的基本信息（info）
# 1.4 显示数据的统计摘要（describe）
# 1.5 查看数据的形状（行数列数）

content = pd.read_csv('book_report.csv')
print(content.head(3))
print(content.info())
print(content.describe())
print(content.shape)
'''

'''
practice2:数据类型转换

# 2.1 检查每列的数据类型
# 2.2 将'入职日期'列转换为 datetime 类型
# 2.3 将'工资'列转换为 int 类型（处理缺失值后再转）
# 2.4 将'绩效分'列转换为 category 类型

print(content.dtypes)
print(pd.to_datetime(content['入职日期'])) #使用to_datetime函数来将数据类型转换为datetime类型
print(content['工资'].dropna().astype('int64'))
print(content['绩效分'].astype('category'))
'''

'''
practice3:缺失值处理

# 3.1 统计每列缺失值的数量
# 3.2 计算'工资'列的缺失值比例
# 3.3 用'工资'列的中位数填充缺失值
# 3.4 删除'加班时长'列有缺失值的行
# 3.5 用'部门'列的分组均值填充'工资'缺失值（不同部门用不同均值）

groupby:将数据按照列的一个或者多个数值分成多个组
transform:对分组后的数据进行转换操作，返回与原始数据相同形状的结果

print(content.isna().sum())
print(content['工资'].count() / content['工资'].size) #size是元素个数，itemsize是每个元素的字节数，nbytes是总的字节数
print(content['工资'].fillna(content['工资'].mean()))
print(content.dropna(subset = ['加班时长']))
print(content.groupby('部门')['工资'].transform(lambda x: x.fillna(x.mean()))) #用部门的分组均值填充工资的缺失值
'''

'''
practice4:数据筛选

# 4.1 筛选出工资大于10000的员工
# 4.2 筛选出部门为'技术部'的员工
# 4.3 筛选出工资大于10000且绩效分为'A'的员工
# 4.4 筛选出部门为'销售部'或'市场部'的员工
# 4.5 筛选出入职日期在2020年之后的员工

使用.dt.year来获取datetime类型的年份

print(content[content['工资'] > 10000])
print(content[content['部门'] == '技术部'])
print(content[(content['工资'] > 10000) & (content['绩效分'] == 'A')])
print(content[(content['部门'] == '销售部') | (content['部门'] == '市场部')])
print(content[pd.to_datetime(content['入职日期']).dt.year > 2020]) #使用to_datetime转换类型之后，.dt.year获取年份
'''

'''
practice5:数据变形

# 5.1 使用 melt 将'员工ID'、'姓名'、'部门'作为标识列，将'工资'和'加班时长'转换为长格式
# 5.2 使用 pivot 将长格式数据转回宽格式
# 5.3 创建透视表，行索引为'部门'，列索引为'绩效分'，值为'工资'，聚合函数为平均值

pivot_table:创建透视表，根据一个或多个列的值对数据进行分组、聚合、重组，四个参数分别index表示按什么分组，columns表示按什么展开，values表示统计的数据，aggfunc表示操作方式

pd_melt = pd.melt(content, id_vars = ['员工ID', '姓名', '部门'], value_vars = ['工资', '加班时长'])
print(pd_melt)
print(pd_melt.pivot(index = ['员工ID', '姓名', '部门'], columns = 'variable', values = 'value'))
print(content.pivot_table(index = '部门', columns = '绩效分', values = '工资', aggfunc= 'mean'))
'''

'''
practice6:数据分箱

# 6.1 使用 cut 将'工资'分成3个区间，标签为['低', '中', '高']
# 6.2 使用 qcut 将'工资'分成3组（等频分箱），标签为['低', '中', '高']
# 6.3 使用 cut 将'加班时长'分成 [0, 20, 30, 50] 区间，标签为['正常', '较多', '很多']

print(pd.cut(content['工资'], bins = 3, labels = ['低', '中', '高']))
print(pd.qcut(content['工资'], q = 3, labels = ['低', '中', '高']))
print(pd.cut(content['加班时长'], bins = [0, 20, 30, 50], labels = ['正常', '较多', '很多']))
'''

'''
practice7:分组聚合

# 7.1 按部门分组，计算每组的平均工资
# 7.2 按部门分组，计算每组的最高工资、最低工资、人数
# 7.3 按部门和绩效分分组，计算平均工资
# 7.4 使用 agg 方法，同时计算工资的总和、平均值、中位数

print(content.groupby('部门')['工资'].mean())
print(content.groupby('部门')['工资'].max(), content.groupby('部门')['工资'].min(), content.groupby('部门')['工资'].size())
print(content.groupby(['部门', '绩效分'])['工资'].mean())
print(content['工资'].agg(['sum', 'mean', 'median'])) #直接使用列表进行多个操作
''' 


'''
practice8:文件保存

# 8.1 将处理后的数据保存为 CSV 文件（不包含索引）
# 8.2 将数据保存为 Excel 文件
# 8.3 只保存'员工ID', '姓名', '部门', '工资'四列到新 CSV 文件

filled_content = content.groupby('部门')['工资'].transform(lambda x: x.fillna(x.mean())) #使用部门平均值来填充平均值
filled_content.to_csv('book_report.csv', index = False) #index = False:不包含索引保存文件

df.to_excel('output.xlsx', index=False, engine='openpyxl')

chosen_content = content.iloc[:, 0 : 4] #先行后列，行是所有行，列是0到3列
chosen_content.to_csv('book_report.csv')
'''

'''
practice9:综合分析
# 需求：分析员工绩效与工资的关系
# 9.1 添加新列'工资等级'，根据工资分箱（<10000为'低'，10000-13000为'中'，>13000为'高'）
# 9.2 按绩效分分组，计算平均工资
# 9.3 创建透视表：行=绩效分，列=工资等级，值=员工ID，聚合函数=计数
# 9.4 找出每个部门绩效分最高的员工

content['工资等级'] = pd.cut(content['工资'], bins = [0, 10000, 13000, inf], labels = ['低', '中', '高']) #inf表示无穷大
print(content.groupby('绩效分')['工资'].mean())
print(content.pivot_table(index = '绩效分', columns = '工资等级', values= '员工ID', aggfunc= 'count'))
print(content[content.groupby('部门')['绩效分'].transform(lambda x: x == x.max())]) #使用max获取绩效分的最大值
'''

raw_data = pd.DataFrame({
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': ['25', '三十', '35', '28', None],
    '工资': [8000, '一万二', 15000, None, 9500],
    '入职日期': ['2020.01.15', '2019-03-20', '2021/06/10', '2018-11-01', '2022-02-28'],
    '部门': ['销售部', '技术部', '销售部', '技术部', '市场部']
})

# 要求：
# 10.1 将'年龄'列中的'三十'转换为30，并转为整数类型
# 10.2 将'工资'列中的'一万二'转换为12000，并转为整数类型
# 10.3 将'入职日期'统一转换为 datetime 类型（处理多种日期格式）
# 10.4 检查并处理缺失值
# 10.5 最终输出清洗后的数据

raw_data = raw_data.replace('三十', 30)
raw_data['年龄'] = raw_data['年龄'].fillna(0).astype('int')


raw_data = raw_data.replace('一万二', 12000)
raw_data['工资'] = raw_data['工资'].fillna(0).astype('int')

raw_data['入职日期'] = pd.to_datetime(raw_data['入职日期'], format = 'mixed') #format = 'mixed'会自动识别多种格式

print(raw_data.isna())

