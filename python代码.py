from math import nan

import pandas as pd
import numpy as np
'''
practice1:创建dataframe

import pandas as pd
import numpy as np
#使用字典创建
df = pd.DataFrame({
    'name' : ['张三', '李四', '王五'],
    'age' : [20, 25, 30],
    'city' : ['北京', '上海', '广州']
})
print(df)

#使用numpy的randint创建
d = pd.DataFrame(np.random.randint(1, 100, size = (4, 3)), columns = ['A', 'B', 'C'])
print(d)
'''

'''
practice2:查看信息

df = pd.DataFrame({
    'name' : ['张三', '李四', '王五'],
    'age' : [20, 25, 30],
    'city' : ['北京', '上海', '广州']
})
print(df.head(3))
print(df.tail(2))
print(df.size)
print(df.columns)
print(df.dtypes)
print(df.describe())
'''

'''
practice3:列的获取

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})

print(df.Name)
print(df['Name'])
print(df[['Name', 'Score']], df[['Name', 'Score']].dtypes)
print(df)
'''

'''
practice4:行的获取

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
print(df.iloc[1])
print(df.iloc[1 : 4])
print(df.iloc[0 : 5 : 2])
print(df.iloc[0 : 3])
print(df.iloc[-1 : -4 : -1])
'''

'''
practice5:同时选择行和列

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
print(df)
print(df.loc[0]['Score'])
print(df.iloc[1, 1])
print(df.loc[1 : 3][['Name', 'Score']])
print(df.iloc[1 : 4, 0 : 3])
print(df[['Name', 'Score']])
'''

'''
practice6:单条件筛选

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
print(df[df.Age > 30])
print(df[df.City == '北京'])
print(df[df.Score >= 90])
'''

'''
practice7:多条件筛选

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
print(df[(df.Age > 25) & (df.Score > 80)])
print(df[(df.City == '北京') | (df.City == '上海')])
print((df.Age <= 30) & (df.Age >= 25))
print(df[df.Score != 85])
'''

'''
practice8:query的使用

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
print(df.query('Age > 30'))
print(df.query('City == "北京" & Score > 80'))
'''

'''
practice9:数据修改

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
df.loc[df['Name'] == 'Alice', 'Score'] = 90
df.loc[df['Age'] > 30, 'Score'] += 5
df.loc[df['City'] == '深圳', 'City'] = '广州'
df['Grade'] = np.where(df.Score >= 90, 'A', np.where(df.Score >= 80, 'B', np.where(df.Score >= 70, 'C', 'D')))
print(df)
'''

'''
practice10:添加和删除

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [25, 30, 35, 28, 32],
    'Score': [85, 92, 78, 88, 95],
    'City': ['北京', '上海', '广州', '北京', '深圳']
})
df['Department'] = 'CS'
df.loc[4] = ['Frank', 26, 88, '上海', 'CS']
df.drop('City', axis = 1, inplace = True) #0是行，1是列
df.drop(2, inplace = True) #inplace表示在原df上进行操作
print(df)
'''

'''
practice11:检测填充缺失值

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 2, 3, np.nan, 6],
    'C': [1, np.nan, 3, 4, np.nan],
    'D': [1, 2, 3, 4, 5]
})
print(df.isna())
print(df.count()) #检测每列的缺失值的数量
print(df.dropna(axis = 1)) #删除所有包含缺失值的行
print(df.fillna(0))
print(df.fillna(df.mean())) #用每列的均值填充缺失值
'''

'''
practice12:填充缺失值

df = pd.DataFrame({
    'A': [1, 2, np.nan, 4, 5],
    'B': [np.nan, 2, 3, np.nan, 6],
    'C': [1, np.nan, 3, 4, np.nan],
    'D': [1, 2, 3, 4, 5]
})
print(df.ffill())
print(df.bfill())        
print(df.dropna())       
print(df.dropna(axis = 1))  
'''

'''
practice13:排序

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Score': [85, 92, 85, 92, 88],
    'Age': [25, 30, 35, 28, 32]
})
print(df.sort_values('Score', ascending= False))   #ascending = False说明是降序排序
print(df.sort_values(['Score', 'Age'], ascending=[False, True]))     
'''
                                                                