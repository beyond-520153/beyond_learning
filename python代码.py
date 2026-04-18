import pandas as pd
import numpy as np
from datetime import datetime, date

# 设置随机种子，保证结果可复现
np.random.seed(42)

# 生成10000条销售记录
n = 10000

data = {
    '订单号': [f'ORD-{i:05d}' for i in range(1, n+1)],
    '订单日期': pd.date_range('2024-01-01', periods=n, freq='h').strftime('%Y-%m-%d'),
    '客户ID': np.random.randint(1000, 2000, n),
    '客户等级': np.random.choice(['普通', '白银', '黄金', '钻石'], n, p=[0.5, 0.25, 0.15, 0.1]),
    '产品类别': np.random.choice(['电子产品', '服装', '食品', '家居', '美妆'], n, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    '产品名称': np.random.choice(['手机', '电脑', 'T恤', '连衣裙', '零食', '饮料', '沙发', '床垫', '面膜', '口红'], n),
    '单价': np.random.randint(50, 5000, n),
    '数量': np.random.randint(1, 10, n),
    '折扣': np.random.choice([0, 0.05, 0.1, 0.15, 0.2], n, p=[0.6, 0.15, 0.1, 0.08, 0.07]),
    '是否退货': np.random.choice([0, 1], n, p=[0.95, 0.05]),
    '发货城市': np.random.choice(['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安'], n),
    '配送方式': np.random.choice(['快递', '同城配送', '门店自提'], n, p=[0.7, 0.2, 0.1])
}

df = pd.DataFrame(data)
df['销售额'] = df['单价'] * df['数量'] * (1 - df['折扣'])
df.loc[df['是否退货'] == 1, '销售额'] = 0

# 随机插入一些缺失值
missing_idx = np.random.choice(n, size=int(n*0.03), replace=False)
df.loc[missing_idx, '折扣'] = np.nan

#将数值保存到excel文件里
df.to_excel('output.xlsx')

#日期处理：将订单日期转换为datetime类型，并提取 年、月、日、星期几 为新列
df['订单日期'] = pd.to_datetime(df['订单日期'])
df['年'] = df['订单日期'].dt.year
df['月'] = df['订单日期'].dt.month
df['日'] = df['订单日期'].dt.day
df['星期几'] = df['订单日期'].dt.day_name() #day_name()获取星期几

#缺失值处理：折扣列的缺失值，用该产品类别的平均折扣填充
#获取折扣列的缺失值数量
#print(df['折扣'].isna().sum()) 
df['折扣'].fillna(df['折扣'].mean(), inplace = True) #使用inplace = True来直接在原表上进行修改

#异常值检测：找出单价 > 4000 或数量 > 8 的订单，标记为 异常标记 列（True/False）
df['异常标记'] = False #首先初始化所有异常标记都为False
df.loc[(df['单价'] > 4000) | (df['数量'] > 8) , '异常标记'] = True #满足条件的改为True

#删除重复：检查是否有重复订单号，如有则删除
print(df['订单号'].nunique(), df['订单号'].count()) #获取去重之后的数值,以及订单号的唯一数值数
#因为count和nunique数值相同，所以说明没有相同的订单号，但是依然进行去重
df = df.drop_duplicates(subset = ['订单号'])

#新增列：计算 折扣金额 = 单价 × 数量 × 折扣
df['折扣金额'] = df['单价'] * df['数量'] * df['折扣']

#月度销售趋势：按月统计总销售额、订单数、平均客单价（销售额/订单数）
month_data = df.groupby('月').agg(
    总销售额 = ('销售额', 'sum'),
    订单数 = ('订单号', 'count'),
    平均客单价 = ('销售额', 'mean')
)

#客户等级分析：统计各等级客户的消费总额、订单数、人均消费
customer_data = df.groupby('客户等级').agg(
    消费总额 = ('销售额', 'sum'),
    订单数 = ('订单号', 'count'),
    人均消费 = ('销售额', 'mean')
)

#产品类别分析：找出销售额前3的产品类别，以及它们的主力产品（销售额最高的产品）
product_data = df.groupby('产品类别')['销售额'].sum()

top3_best_sell_product = product_data.reset_index().sort_values('销售额', ascending= False).head(3)
best_sell_product = top3_best_sell_product.head(1)

#城市分析：计算每个城市的销售额、订单数、平均折扣，找出业绩最好的城市
city_data = df.groupby('发货城市').agg(
    销售额 = ('销售额', 'sum'),
    订单数 = ('订单号', 'count'),
    平均折扣 = ('折扣', 'mean')
)

best_sell_city = city_data.sort_values('销售额').head(1).reset_index()

#退货分析：计算整体退货率，以及各产品类别的退货率
total_return_rate = df['是否退货'].mean()
print(f'总体退货率是：{total_return_rate}')
product_return_rate = df.groupby('产品类别')['是否退货'].mean()

#交叉分析：创建透视表，行=客户等级，列=产品类别，值=销售额，聚合=求和
customer_pivot_table = df.pivot_table(index = '客户等级', columns = '产品类别', values = '销售额', aggfunc = 'sum')

#多级分组：按 发货城市 和 产品类别 分组，计算销售额总和和平均折扣
category_table = df.groupby(['发货城市', '产品类别']).agg(
    销售总额 = ('销售额', 'sum'),
    平均折扣 = ('折扣', 'mean')
)

#累计统计：按日期顺序，计算每日累计销售额
day_sell_count = df.groupby('订单日期')['销售额'].sum().sort_index().cumsum()

#排名：找出销售额最高的前10个客户ID
customer_sell_count = df.groupby('客户ID')['销售额'].sum()
top10_sell_customer = customer_sell_count.reset_index().sort_values('销售额', ascending = False).head(10)

#留存分析：计算每个月的活跃客户数（有购买记录的客户去重计数）
active_customer_count = df['客户ID'].nunique()

#R（最近购买时间）：计算每个客户最后购买日期距今天数
today = datetime.today() #使用datetime.today()获取今天日期
current_customer_buy = df.groupby('客户ID')['订单日期'].max() #使用max获取最大消费日期（最后消费日期）
R = (today - current_customer_buy).dt.days.reset_index()
R.rename(columns = {'订单日期': '上一次消费'}, inplace = True)

#F（购买频率）：计算每个客户的订单数
F = df.groupby('客户ID')['订单号'].nunique().reset_index()
F.rename(columns = {'订单号': '订单量'}, inplace = True)

#M（消费金额）：计算每个客户的消费总额
M = df.groupby('客户ID')['销售额'].sum().reset_index()
M.rename(columns={'销售额': '消费额'}, inplace = True)

#将三张表合成一张，保证index是对应的
rfm = R.merge(F, on = '客户ID').merge(M, on = '客户ID')

#根据 RFM 分数将客户分为：高价值客户、潜力客户、普通客户、流失客户
#分别使用R，F，M的平均值来进行后续的判断
aveg_R = rfm['上一次消费'].mean() 
aveg_F = rfm['订单量'].mean() 
aveg_M = rfm['消费额'].mean()

conditions = [
    (rfm['上一次消费'] < aveg_R) & (rfm['订单量'] > aveg_F) & (rfm['消费额'] > aveg_M), #高价值客户
    (rfm['上一次消费'] < aveg_R) & (rfm['订单量'] > aveg_F), #潜力客户
    (rfm['上一次消费'] >= aveg_R) & (rfm['订单量'] <= aveg_F) #流失客户
]
choices = ['高价值客户', '潜力客户', '流失客户']

#使用select进行分类
rfm['客户类型'] = np.select(conditions, choices, default = '普通客户')
rfm.to_csv('客户类型分析表.csv')

#计算每月的环比增长率：使用pct_change()函数
monthly_sale_count = df.groupby('月')['销售额'].sum().reset_index()
monthly_sale_count['环比增长率'] = monthly_sale_count['销售额'].pct_change() * 100
print(monthly_sale_count)
monthly_sale_count.to_csv('每月环比增长表.csv')