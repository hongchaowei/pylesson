#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用户提供的聚类分析代码示例
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def test_clustering_analysis():
    """测试聚类分析代码"""
    print("测试股票收益数据聚类分析")
    print("=" * 50)
    
    try:
        # 加载股票收益数据
        stocks = pd.read_csv('stock_returns.csv', index_col='date')
        print(f"✓ 成功加载数据，形状: {stocks.shape}")
        print(f"✓ 数据日期范围: {stocks.index.min()} 到 {stocks.index.max()}")
        print(f"✓ 股票列表: {list(stocks.columns)}")
        
        # 显示数据基本信息
        print("\n数据预览:")
        print(stocks.head())
        
        print("\n数据统计信息:")
        print(stocks.describe())
        
        # 检查缺失值
        missing_values = stocks.isnull().sum()
        print(f"\n缺失值统计:")
        print(missing_values)
        
        # 删除包含缺失值的行
        stocks_clean = stocks.dropna()
        print(f"\n清理后数据形状: {stocks_clean.shape}")
        
        # 数据标准化
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(stocks_clean)
        print(f"✓ 数据标准化完成，形状: {scaled_data.shape}")
        
        # 聚类分析
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        print(f"✓ K-means聚类完成，发现 {len(np.unique(clusters))} 个聚类")
        
        # 分析聚类结果
        stocks_clean['cluster'] = clusters
        cluster_stats = stocks_clean.groupby('cluster').mean()
        
        print("\n聚类统计结果:")
        print(cluster_stats)
        
        # 聚类分布
        cluster_counts = pd.Series(clusters).value_counts().sort_index()
        print("\n各聚类的样本数量:")
        print(cluster_counts)
        
        # 可视化聚类结果
        plt.figure(figsize=(15, 10))
        
        # 1. 聚类分布饼图
        plt.subplot(2, 3, 1)
        plt.pie(cluster_counts.values, labels=[f'聚类{i}' for i in cluster_counts.index], autopct='%1.1f%%')
        plt.title('聚类分布')
        
        # 2. 聚类中心热力图
        plt.subplot(2, 3, 2)
        cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=stocks_clean.columns[:-1])
        sns.heatmap(cluster_centers, annot=True, cmap='RdYlBu_r', center=0)
        plt.title('聚类中心热力图')
        plt.ylabel('聚类')
        
        # 3. 股票收益率分布
        plt.subplot(2, 3, 3)
        for i in range(len(stocks_clean.columns)-1):
            plt.hist(stocks_clean.iloc[:, i], alpha=0.5, label=stocks_clean.columns[i], bins=30)
        plt.title('股票收益率分布')
        plt.xlabel('收益率')
        plt.ylabel('频次')
        plt.legend()
        
        # 4. 聚类结果散点图（前两个主成分）
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(scaled_data)
        
        plt.subplot(2, 3, 4)
        scatter = plt.scatter(pca_data[:, 0], pca_data[:, 1], c=clusters, cmap='viridis')
        plt.colorbar(scatter)
        plt.title(f'PCA聚类可视化\n(解释方差: {pca.explained_variance_ratio_.sum():.2%})')
        plt.xlabel('第一主成分')
        plt.ylabel('第二主成分')
        
        # 5. 聚类内股票收益率箱线图
        plt.subplot(2, 3, 5)
        cluster_returns = []
        cluster_labels = []
        for cluster_id in sorted(stocks_clean['cluster'].unique()):
            cluster_data = stocks_clean[stocks_clean['cluster'] == cluster_id]
            for col in cluster_data.columns[:-1]:  # 排除cluster列
                cluster_returns.extend(cluster_data[col].values)
                cluster_labels.extend([f'聚类{cluster_id}'] * len(cluster_data))
        
        cluster_df = pd.DataFrame({'收益率': cluster_returns, '聚类': cluster_labels})
        sns.boxplot(data=cluster_df, x='聚类', y='收益率')
        plt.title('各聚类收益率分布')
        plt.xticks(rotation=45)
        
        # 6. 聚类稳定性分析
        plt.subplot(2, 3, 6)
        inertias = []
        k_range = range(2, 11)
        for k in k_range:
            kmeans_temp = KMeans(n_clusters=k, random_state=42)
            kmeans_temp.fit(scaled_data)
            inertias.append(kmeans_temp.inertia_)
        
        plt.plot(k_range, inertias, 'bo-')
        plt.axvline(x=5, color='red', linestyle='--', alpha=0.7, label='选择的K=5')
        plt.title('肘部法则确定最优聚类数')
        plt.xlabel('聚类数 (K)')
        plt.ylabel('簇内平方和 (Inertia)')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('clustering_analysis_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # 详细分析报告
        print("\n" + "=" * 50)
        print("详细聚类分析报告")
        print("=" * 50)
        
        for cluster_id in sorted(stocks_clean['cluster'].unique()):
            cluster_data = stocks_clean[stocks_clean['cluster'] == cluster_id]
            print(f"\n聚类 {cluster_id}:")
            print(f"  样本数量: {len(cluster_data)}")
            print(f"  平均收益率: {cluster_data.iloc[:, :-1].mean().mean():.4f}")
            print(f"  收益率标准差: {cluster_data.iloc[:, :-1].std().mean():.4f}")
            print(f"  最佳表现股票: {cluster_data.iloc[:, :-1].mean().idxmax()}")
            print(f"  最差表现股票: {cluster_data.iloc[:, :-1].mean().idxmin()}")
        
        # 投资建议
        print("\n" + "=" * 50)
        print("基于聚类结果的投资建议")
        print("=" * 50)
        
        best_cluster = cluster_stats.mean(axis=1).idxmax()
        worst_cluster = cluster_stats.mean(axis=1).idxmin()
        
        print(f"\n🎯 推荐聚类: 聚类 {best_cluster}")
        print(f"   - 平均收益率最高: {cluster_stats.mean(axis=1)[best_cluster]:.4f}")
        print(f"   - 包含股票: {', '.join(cluster_stats.columns)}")
        
        print(f"\n⚠️  谨慎聚类: 聚类 {worst_cluster}")
        print(f"   - 平均收益率最低: {cluster_stats.mean(axis=1)[worst_cluster]:.4f}")
        
        # 风险分析
        print(f"\n📊 风险分析:")
        volatilities = stocks_clean.groupby('cluster').std().mean(axis=1)
        print(f"   - 最低波动聚类: 聚类 {volatilities.idxmin()} (标准差: {volatilities.min():.4f})")
        print(f"   - 最高波动聚类: 聚类 {volatilities.idxmax()} (标准差: {volatilities.max():.4f})")
        
        return True
        
    except FileNotFoundError:
        print("❌ 错误: 找不到 stock_returns.csv 文件")
        print("请先运行 generate_sample_data.py 生成数据文件")
        return False
        
    except Exception as e:
        print(f"❌ 运行出错: {str(e)}")
        return False

def main():
    """主函数"""
    print("股票收益数据聚类分析测试")
    print("这个脚本将测试您提供的聚类分析代码示例")
    print()
    
    success = test_clustering_analysis()
    
    if success:
        print("\n✅ 聚类分析测试完成！")
        print("\n📁 生成的文件:")
        print("   - clustering_analysis_results.png (可视化结果)")
        print("\n💡 提示:")
        print("   - 您可以调整聚类数量 (n_clusters) 来获得不同的聚类结果")
        print("   - 可以尝试不同的聚类算法，如 DBSCAN 或层次聚类")
        print("   - 建议结合基本面分析来验证聚类结果的合理性")
    else:
        print("\n❌ 测试失败，请检查错误信息")

if __name__ == "__main__":
    main()