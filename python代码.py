from multiprocessing import current_process

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler 

# 1. 创建数据集
np.random.seed(42)
n_samples = 500

area = np.random.normal(1500, 300, n_samples)
bedrooms = np.random.randint(1, 5, n_samples)
age = np.random.randint(0, 50, n_samples)
city = np.random.choice(['NewYork', 'LA', 'Chicago'], n_samples)

price_class = ((area > 1500) & (city != 'Chicago')).astype(int)

noise_1 = np.random.normal(0, 1, n_samples)
noise_2 = area * 0.95 + np.random.normal(0, 30, n_samples)

df = pd.DataFrame({
    'area': area,
    'bedrooms': bedrooms,
    'age': age,
    'city': city,
    'noise_1': noise_1,
    'noise_2': noise_2,
    'price_class': price_class
})

# 特征工程
scaler = StandardScaler()
data = scaler.fit_transform(df[['area', 'bedrooms', 'age']])

encoder = OneHotEncoder(sparse_output=False)
encoded_city = encoder.fit_transform(df[['city']])

df['area_per_bedroom'] = df['area'] / df['bedrooms']

# 合并特征（注意：这里用了 area_per_bedroom，不是重复的 area）
X = np.hstack([data, encoded_city, df[['area_per_bedroom']].values])
y = df['price_class'].values

feature_names = ['area', 'bedrooms', 'age'] + list(encoder.get_feature_names_out()) + ['area_per_bedroom']

# ========== 关键修正：先划分数据集 ==========
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"训练集大小: {X_train.shape[0]}")
print(f"测试集大小: {X_test.shape[0]}")
print(f"原始特征数量: {X.shape[1]}")

# ========== 1. SelectKBest ==========
selector = SelectKBest(score_func=f_classif, k=3)
X_train_kbest = selector.fit_transform(X_train, y_train)  # 只在训练集上 fit
X_test_kbest = selector.transform(X_test)                  # 测试集只 transform，防止测试结果虚高

selected_mask = selector.get_support()
selected_features = [feature_names[i] for i in range(len(feature_names)) if selected_mask[i]]
print(f"SelectKBest 选中的特征: {selected_features}")

# LogisticRegression on SelectKBest
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train_kbest, y_train)
print(f"KBest+LR Acc: {accuracy_score(y_test, lr.predict(X_test_kbest)):.4f}")

# ========== 2. PCA ==========
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

print(f"PCA 方差解释比: {pca.explained_variance_ratio_}")

# RandomForest on PCA
rfc_pca = RandomForestClassifier(n_estimators=100, random_state=42)
rfc_pca.fit(X_train_pca, y_train)
y_pred_pca = rfc_pca.predict(X_test_pca)
acc_pca = accuracy_score(y_test, y_pred_pca)
print(f"PCA + RandomForest 准确率: {acc_pca:.4f}")

# ========== 3. RFE ==========
estimator = RandomForestClassifier(n_estimators=50, random_state=42)
selector_rfe = RFE(estimator, n_features_to_select=3)
X_train_rfe = selector_rfe.fit_transform(X_train, y_train)
X_test_rfe = selector_rfe.transform(X_test)

selected_rfe = [feature_names[i] for i, m in enumerate(selector_rfe.get_support()) if m]
print(f"RFE 选中的特征: {selected_rfe}")

rfc_rfe = RandomForestClassifier(n_estimators=100, random_state=42)
rfc_rfe.fit(X_train_rfe, y_train)
acc_rfe = accuracy_score(y_test, rfc_rfe.predict(X_test_rfe))
print(f"RFE + RandomForest 准确率: {acc_rfe:.4f}")

# ========== 4. 原始特征（基准）==========
rfc_original = RandomForestClassifier(n_estimators=100, random_state=42)
rfc_original.fit(X_train, y_train)
acc_original = accuracy_score(y_test, rfc_original.predict(X_test))
print(f"原始特征 + RandomForest 准确率: {acc_original:.4f}")

# ========== 5. SelectKBest + RandomForest ==========
rfc_kbest = RandomForestClassifier(n_estimators=100, random_state=42)
rfc_kbest.fit(X_train_kbest, y_train)
acc_kbest = accuracy_score(y_test, rfc_kbest.predict(X_test_kbest))
print(f"SelectKBest + RandomForest 准确率: {acc_kbest:.4f}")

# ========== 6. 结果对比 ==========
print("\n" + "=" * 50)
print("准确率对比汇总")
print("=" * 50)
print(f"原始特征 (基准):     {acc_original:.4f}")
print(f"SelectKBest (过滤法): {acc_kbest:.4f}")
print(f"RFE (包装法):         {acc_rfe:.4f}")
print(f"PCA (无监督降维):     {acc_pca:.4f}")
print("=" * 50)

# ========== 7. PCA 可视化 ==========
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

scatter1 = axes[0].scatter(X_train_pca[:, 0], X_train_pca[:, 1], 
                           c=y_train, cmap='coolwarm', alpha=0.6, edgecolors='k')
axes[0].set_xlabel(f'第一主成分 (方差比: {pca.explained_variance_ratio_[0]:.2%})')
axes[0].set_ylabel(f'第二主成分 (方差比: {pca.explained_variance_ratio_[1]:.2%})')
axes[0].set_title('PCA降维后 - 训练集')
plt.colorbar(scatter1, ax=axes[0], label='价格等级')

scatter2 = axes[1].scatter(X_test_pca[:, 0], X_test_pca[:, 1], 
                           c=y_test, cmap='coolwarm', alpha=0.6, edgecolors='k')
axes[1].set_xlabel(f'第一主成分 (方差比: {pca.explained_variance_ratio_[0]:.2%})')
axes[1].set_ylabel(f'第二主成分 (方差比: {pca.explained_variance_ratio_[1]:.2%})')
axes[1].set_title('PCA降维后 - 测试集')
plt.colorbar(scatter2, ax=axes[1], label='价格等级')

plt.tight_layout()
plt.show()