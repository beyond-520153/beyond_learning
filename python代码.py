import jieba
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
# 查看数据的基本信息（形状、列名、数据类型）

# 计算每门科目的平均值、最大值、最小值

# 按班级（class）分组，计算每门科目的平均分

# 绘制数学成绩的直方图（matplotlib）

# 绘制数学和英语的散点图，观察相关性
# 数据：学生考试成绩
data = {
    'name': ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'],
    'math': [85, 92, 78, 88, 95, 76, 89, 91],
    'english': [78, 88, 85, 90, 92, 80, 86, 89],
    'science': [90, 85, 82, 88, 94, 79, 91, 93],
    'class': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B']
}
df = pd.DataFrame(data)
'''
print(df.info()) #查看基本数据
print(df.describe()) #使用describe计算每一列的大致信息

df_class = df.groupby('class')[['math', 'english', 'science']].mean() 

fig, axes = plt.subplots(1, 2, figsize = (10, 9))

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 


axes[0].hist(df['math'], label = '数学成绩分布直方图')
axes[1].scatter(df['math'], df['english'], label = '数学/英语成绩散点图')
axes[0].legend(loc = 'upper left')
axes[1].legend(loc = 'upper left')
axes[1].set_xlabel('数学/分')
axes[1].set_ylabel('英语/分')

plt.show()
'''


# 将数据划分为训练集和测试集（test_size=0.3, random_state=42）

# 使用 OneHotEncoder 对 class 特征进行编码

# 将编码后的特征与数值特征合并

# 使用 LinearRegression（线性回归）训练模型

# 计算测试集上的预测准确率（使用 R² 分数）
class_encoder = OneHotEncoder(sparse_output= False)
encoded_class = class_encoder.fit_transform(df[['class']])

X = np.hstack([df[['math', 'english']], encoded_class])
y = df['science']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    train_size= 0.7,
    random_state= 42
)

model = LinearRegression()
model.fit(X_train, y_train)
print(f"R² 分数: {model.score(X_test, y_test):.3f}")



# 使用 jieba 对所有文本进行分词

# 使用 CountVectorizer 构建词频矩阵

# 打印特征名称（词汇表）

# 找出出现次数最多的前3个词

# 计算第1篇文档和第3篇文档的余弦相似度
corpus = [
    "我喜欢打篮球和游泳",
    "篮球是一项很好的运动",
    "我更喜欢游泳而不是篮球",
    "足球和篮球都是球类运动",
    "今天天气很好适合游泳"
]

# 执行分词过程
tokenized = [' '.join(list(jieba.cut(text))) for text in corpus] 

# 使用CountVectorizer()构建词频矩阵
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(tokenized)

# 打印特征名称
print(vectorizer.get_feature_names_out())

word_freq = X.toarray().sum(axis=0)
print("词频:", dict(zip(vectorizer.get_feature_names_out(), word_freq)))




# 使用 DictVectorizer 提取特征（注意 name 列应该如何处理？）

# 输出特征名称和特征矩阵

# 将结果转换为 DataFrame 以便查看

# （进阶）编写一个简单函数，根据 category = '电子产品' 和 price > 3000 的规则，手动标记"是否高端电子产品"

data = [
    {'name': '产品A', 'category': '电子产品', 'price': 2999, 'rating': 4.5},
    {'name': '产品B', 'category': '服装', 'price': 199, 'rating': 4.2},
    {'name': '产品C', 'category': '电子产品', 'price': 4599, 'rating': 4.8},
    {'name': '产品D', 'category': '图书', 'price': 59, 'rating': 4.0},
    {'name': '产品E', 'category': '服装', 'price': 399, 'rating': 4.3},
]

data_filtered = [{k : v for k , v in item.items() if k != 'name'}for item in data] # 由于产品名称是固定属性没有预测价值，但是产品种类代表了价格所以有价值需要保留，所以去除name

dictvectorizer = DictVectorizer(sparse = False)
X = dictvectorizer.fit_transform(data_filtered) 

d = pd.DataFrame(X, columns= dictvectorizer.get_feature_names_out())

# 处理高端电子产品列
d['是否为高端电子产品'] = False
d.loc[(d['category=电子产品'] == 1) & (d['price'] > 3000), '是否为高端电子产品'] = True





# 提取 text 和 label，将 label 转换为数值（spam=1, ham=0）

# 使用 jieba 对 text 进行中文分词

# 使用 TfidfVectorizer（或 CountVectorizer）提取文本特征

# 划分训练集和测试集（test_size=0.25, random_state=42）

# 使用 MultinomialNB（朴素贝叶斯）训练分类器

# 预测测试集并输出准确率

# （进阶）使用 classification_report 输出精确率、召回率、F1分数

data = [
    {"text": "免费领取100元优惠券", "label": "spam"},
    {"text": "会议通知：今天下午3点开会", "label": "ham"},
    {"text": "恭喜您中奖了，点击领取奖金", "label": "spam"},
    {"text": "妈妈，今晚回家吃饭吗", "label": "ham"},
    {"text": "限时特惠，五折抢购", "label": "spam"},
    {"text": "作业已提交，请查收", "label": "ham"},
    {"text": "您的账户异常，请立即登录", "label": "spam"},
    {"text": "周末一起去爬山吗", "label": "ham"},
]

text = [item['text'] for item in data if 'text' in item]
label = [1 if item['label'] == 'spam' else 0 for item in data]

text_tokenizer = [' '.join(list(jieba.cut(item))) for item in text]

X_train, X_test, y_train, y_test = train_test_split(
    text_tokenizer, label,
    train_size= 0.75,
    random_state= 42,
    stratify=label
)

text_tokenized = CountVectorizer()
X_train_vec = text_tokenized.fit_transform(X_train) #对训练集使用fit_transform
X_test_vec = text_tokenized.transform(X_test) #对测试集使用transform

# 5. 训练分类器
clf = MultinomialNB()
clf.fit(X_train_vec, y_train)

# 6. 预测并输出准确率
y_pred = clf.predict(X_test_vec)
print(f"准确率: {accuracy_score(y_test, y_pred):.2f}")

# 7. 进阶：输出详细评估报告
print("\n分类报告:")
print(classification_report(y_test, y_pred, target_names=['ham', 'spam']))