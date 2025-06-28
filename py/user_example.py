#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户提供的聚类分析代码示例
现在可以正常运行，因为我们已经生成了所需的数据文件
"""

import pandas as pd 
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler 

print("运行用户提供的聚类分析代码示例")
print("=" * 50)

# 加载股票收益数据 
stocks = pd.read_csv('stock_returns.csv', index_col='date') 
print(f"✓ 成功加载数据，形状: {stocks.shape}")
print(f"✓ 股票列表: {list(stocks.columns)}")

# 显示数据预览
print("\n数据预览:")
print(stocks.head())

# 处理缺失值
stocks = stocks.dropna()
print(f"\n清理后数据形状: {stocks.shape}")

# 数据标准化 
scaler = StandardScaler() 
scaled_data = scaler.fit_transform(stocks) 
print(f"✓ 数据标准化完成")

# 聚类分析 
kmeans = KMeans(n_clusters=5, random_state=42) 
clusters = kmeans.fit_predict(scaled_data) 
print(f"✓ K-means聚类完成，发现 {len(set(clusters))} 个聚类")

# 分析聚类结果 
stocks['cluster'] = clusters 
cluster_stats = stocks.groupby('cluster').mean()

print("\n聚类统计结果:")
print(cluster_stats)

print("\n各聚类的样本数量:")
print(stocks['cluster'].value_counts().sort_index())

print("\n✅ 用户代码运行成功！")
print("\n💡 说明:")
print("   - 现在您的代码可以正常运行了")
print("   - 我们生成了包含8只股票约2年历史数据的虚拟数据集")
print("   - 数据包括AAPL, MSFT, GOOG, AMZN, JPM, BAC, TSLA, NVDA")
print("   - 您可以修改聚类数量或尝试其他参数")