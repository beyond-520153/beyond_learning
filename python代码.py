import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 示例数据
months = ['1月', '2月', '3月', '4月', '5月', '6月']
sales_2023 = [120, 135, 150, 140, 160, 180]
sales_2024 = [130, 145, 160, 155, 175, 195]

'''
practice1：折线图
plt.figure(figsize=(10, 6))
plt.title('月度销售额对比')
plt.plot(
    months, sales_2023,
    marker = 'o',
    linewidth = 2,
    color = 'blue',
    label = '2023年'
)
plt.plot(
    months, sales_2024,
    marker = 'o',
    linewidth = 2,
    color = 'orange',
    label = '2024年'
)

plt.xlabel('月份')
plt.ylabel('销售额(万元)')

for i, (x, y) in enumerate(zip(months, sales_2023)):
    plt.text(i, y + 3, str(y), ha='center', va='bottom', fontsize = 9)

for i, (x, y) in enumerate(zip(months, sales_2024)):
    plt.text(i, y + 3, str(y), ha = 'center', va = 'bottom', fontsize = 9)

plt.legend(loc = 'upper left', title = '年份', fontsize = 9)
plt.grid(True, linestyle = '--', alpha = 0.5)
plt.show()
'''

'''
practice2:柱状图

plt.figure(figsize = (10, 8))
plt.bar(months, sales_2024,
        color = 'steelblue',
        edgecolor = 'black', #边框的颜色为黑色
        linewidth = 1, #边框的线长为1
        alpha = 0.7
        )
plt.title('2024年月度销售额')

for i, (month, sale) in enumerate(zip(months, sales_2024)):
    plt.text(i, sale + 3, str(sale), ha = 'center', va = 'bottom', fontsize = 9) #ha是水平对齐，va是垂直对齐

plt.ylim(100, 250)
plt.show()
'''

'''
practice3:饼图

products = ['手机', '电脑', '平板', '耳机', '手表']
sales_ratio = [35, 28, 18, 12, 7]
plt.figure(figsize= (10, 8))
#autopct表示小数点位数，explode表示突出，传入的参数是一个列表，shadow表示阴影，startangle是起始角度
plt.pie(sales_ratio, labels = products, autopct = '%1.1f%%', explode = [0.05, 0, 0, 0, 0], shadow= True, startangle= 90)

plt.title('产品销售额占比')
plt.show()
'''

'''
practice4:散点图加上polyfit进行拟合

ad_cost = [5, 8, 12, 15, 20, 25, 30, 35, 40, 45]
sales = [50, 65, 80, 95, 110, 130, 145, 160, 175, 190]

plt.figure(figsize= (10, 8))
plt.title('广告费与销售额关系')
plt.xlabel('广告费（万元）')
plt.ylabel('广告费（万元）')
plt.scatter(ad_cost, sales, color = 'red', alpha = 0.6, s = 100)
xielv, jieju = np.polyfit(ad_cost, sales, deg = 1) #使用polyfit对直线进行拟合，返回截距和斜率

x_fit = np.linspace(min(ad_cost), max(ad_cost), 100) #获取x坐标的array
y_fit = x_fit * xielv + jieju #使用计算获取y的array

plt.plot(x_fit, y_fit,
         color = 'red',
         linewidth = 1,
         linestyle = '--'
         )
plt.show()
'''

'''
practice5:子图布局

fig, axes = plt.subplots(2, 2, figsize = (10, 8))
axes[0, 0].plot(months, sales_2024,
                      color = 'steelblue',
                      label = '2024年销售额图'
                      )

axes[0, 1].bar(months, sales_2024,
                     color = 'orange',
                     edgecolor = 'black',
                     alpha = 0.8
                     )
axes[1, 0].pie(sales_2024, labels = months,
               autopct = '%1.1f%%',
               shadow = True,
               startangle = 90
               )

axes[1, 1].scatter(months, sales_2024)
plt.show()
'''

'''
practice6:多图叠加

plt.figure(figsize = (10, 8))
plt.bar(months, sales_2024,
        color = 'orange',
        edgecolor = 'black',
        linewidth = 1,
        alpha = 0.6,
        label = '柱状图'
        )
plt.plot(months, sales_2024,
         color = 'steelblue',
         linewidth = 1,
         marker = 'o',
         label = '折线图'
         )
plt.legend(loc = 'upper left')
plt.show()
'''

'''
practice7:水平条形图

products = ['手机', '电脑', '平板', '耳机', '手表', '相机']
sales = [350, 280, 200, 150, 100, 80]

#将两组数据组成一个dataframe，直接在dataframe中进行数值排序
plt.figure(figsize = (10, 8))
data = pd.DataFrame({
    '产品': products,
    '销量': sales
}) 

data.sort_values('销量', inplace=True)
plt.barh(data['产品'], data['销量'],
         color = 'orange',
         edgecolor = 'black',
         linewidth = 1,
         alpha = 0.5
         )
for i, sale in enumerate(data['销量']): #直接使用data里面的数据进行输出
    plt.text(sale, i, str(sale), ha = 'center', va = 'bottom', fontsize = 9)
plt.ylabel('产品名称')
plt.xlabel('销量（台）')
plt.title('各产品销量排行', fontsize = 9)
plt.show()
'''

'''
practice8:堆叠面积图

months = ['1月', '2月', '3月', '4月', '5月', '6月']
sales_2023 = [120, 135, 150, 140, 160, 180]
sales_2024 = [130, 145, 160, 155, 175, 195]

plt.figure(figsize=(10, 6))

# 堆叠面积图：fill_between的第二个参数是起始的y值，第三个参数是截止的y值
# plt.fill_between(months, 0, sales_2023, alpha=0.5, label='2023年')
# plt.fill_between(months, sales_2023, [sales_2023[i] + sales_2024[i] for i in range(len(months))], 
#                  alpha=0.5, label='2024年')

# 或者使用 stackplot（更简单）：直接传入多个y值的序列，每一个序列都加在在前一个上面
plt.stackplot(months,sales_2023, sales_2024 , labels=['2023年', '2024年'], alpha=0.5)

plt.title('两年销售额对比（面积图）')
plt.xlabel('月份')
plt.ylabel('销售额（万元）')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
'''

'''
practice9:直方图和箱型图

data = np.random.normal(80, 10, 1000)
fig, axes = plt.subplots(1, 2, figsize = (10, 8))
axes[0].hist(data, bins = 20, color = 'green', edgecolor = 'black', alpha = 0.7)

axes[1].boxplot(data, vert=False, patch_artist=True, #vert表示方向False表示水平方向，True表示垂直方向，patch_artist表示填充颜色
                boxprops=dict(facecolor='lightblue', color='black'), #boxprops表示箱体的属性
                whiskerprops=dict(color='black'), #whiskerprops表示箱线的属性
                capprops=dict(color='black'), #capprops表示帽线属性
                medianprops=dict(color='red', linewidth=2))  #medianprops表示中位数线的属性
fig.suptitle('考试成绩分析')
plt.show()
'''


months = ['1月', '2月', '3月', '4月', '5月', '6月']
sales_2024 = [130, 145, 160, 155, 175, 195]
x = range(len(months))

plt.figure(figsize=(12, 6))

# 绘制折线图
plt.plot(x, sales_2024, 
         marker='o', 
         markersize=8,
         linewidth=2.5,
         color='steelblue',
         label='2024年销售额')

# 设置 X 轴刻度标签
plt.xticks(x, months)

# 添加数据标签
for i, sale in enumerate(sales_2024):
    offset = 5 if sale < 180 else -10
    va = 'bottom' if sale < 180 else 'top'
    plt.text(i, sale + offset, str(sale), ha='center', va=va, fontsize=10, fontweight='bold')

# 添加水平参考线（平均值线）
avg_sales = np.mean(sales_2024)
plt.axhline(y=float(avg_sales), color='gray', linestyle='--', linewidth=1.5, label=f'平均值: {avg_sales:.1f}')

# 标注最高点
max_idx = sales_2024.index(max(sales_2024))
max_month = months[max_idx]
max_sale = max(sales_2024)
plt.annotate(f'最高点: {max_sale}万元',
             xy=(max_idx, max_sale),
             xytext=(max_idx + 0.5, max_sale + 10),
             arrowprops=dict(arrowstyle='->', color='red'),
             fontsize=10, color='red')

# 标题和标签
plt.title('2024年月度销售额趋势', fontsize=14, fontweight='bold')
plt.xlabel('月份', fontsize=12)
plt.ylabel('销售额（万元）', fontsize=12)

# 网格线（虚线，透明度0.3）
plt.grid(True, linestyle='--', alpha=0.3)

# 图例
plt.legend(loc='upper left')
plt.show()
