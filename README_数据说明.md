# 课程虚拟数据说明

## 概述

为了解决课程代码中缺少数据文件的问题，我们生成了一套完整的虚拟金融数据集。这些数据可以支持课程中所有的代码示例正常运行。

## 快速开始

### 1. 生成数据
```bash
python generate_sample_data.py
```

### 2. 测试用户示例代码
```bash
python user_example.py
```

### 3. 运行完整的聚类分析测试
```bash
python test_clustering_example.py
```

## 生成的数据文件

### 股票数据
- **stock_data.csv** / **stock_prices.csv**: 完整的股票OHLCV数据
  - 包含8只股票：AAPL, MSFT, GOOG, AMZN, JPM, BAC, TSLA, NVDA
  - 时间跨度：约2年的交易日数据
  - 字段：date, symbol, open, high, low, close, volume

- **stock_returns.csv**: 股票收益率数据（透视表格式）
  - 日期为索引，股票代码为列
  - 用于您提供的聚类分析代码示例

### 投资组合数据
- **portfolio_returns.csv**: 投资组合收益率
- **benchmark_returns.csv**: 基准收益率
- **portfolio_weights.csv**: 投资组合权重
- **benchmark_weights.csv**: 基准权重
- **asset_returns.csv**: 资产收益率

### 特征数据
- **stock_features.csv**: 股票基本面特征
  - 市值、市盈率、市净率、负债权益比等
  - 用于机器学习和因子分析

### 交易数据
- **transactions.csv**: 模拟交易记录
  - 包含买卖操作、数量、价格等信息

### 其他数据
- **credit_data.csv**: 信用风险数据（10,000条记录）
- **news_data.csv**: 新闻情感数据
- **financial_data.csv**: 综合金融市场数据

## 用户示例代码说明

您提供的代码现在可以正常运行：

```python
import pandas as pd 
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler 

# 加载股票收益数据 
stocks = pd.read_csv('stock_returns.csv', index_col='date') 

# 数据标准化 
scaler = StandardScaler() 
scaled_data = scaler.fit_transform(stocks) 

# 聚类分析 
kmeans = KMeans(n_clusters=5, random_state=42) 
clusters = kmeans.fit_predict(scaled_data) 

# 分析聚类结果 
stocks['cluster'] = clusters 
cluster_stats = stocks.groupby('cluster').mean()
```

## 数据特点

### 真实性
- 使用几何布朗运动模拟股票价格走势
- 考虑了实际的市场波动率和收益率分布
- 包含了合理的交易量和基本面指标

### 完整性
- 涵盖了课程中所有需要的数据类型
- 支持时间序列分析、聚类分析、回归分析等
- 包含缺失值处理的测试场景

### 可扩展性
- 可以轻松修改股票列表和时间范围
- 支持添加新的特征和指标
- 代码结构清晰，便于定制

## 使用建议

### 学习用途
1. **数据探索**: 先运行基本的数据查看和统计分析
2. **算法测试**: 尝试不同的机器学习算法和参数
3. **可视化**: 使用matplotlib和seaborn创建图表
4. **回测**: 构建和测试交易策略

### 实际应用
1. **替换数据源**: 将CSV文件替换为真实的金融数据API
2. **扩展特征**: 添加更多技术指标和基本面数据
3. **实时更新**: 实现数据的定期更新机制

## 常见问题

### Q: 数据是真实的吗？
A: 这些是模拟数据，但基于真实的金融市场统计特性生成，适合学习和测试使用。

### Q: 可以修改股票列表吗？
A: 可以，修改`generate_sample_data.py`中的`stocks`列表，然后重新运行即可。

### Q: 如何添加更多历史数据？
A: 修改`generate_sample_data.py`中的日期范围参数，增加`timedelta(days=730)`中的天数。

### Q: 数据更新频率如何？
A: 当前生成的是静态数据，如需实时数据，建议集成yfinance或其他金融数据API。

## 技术支持

如果您在使用过程中遇到问题：

1. 检查Python环境是否安装了所需的库：
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```

2. 确保所有数据文件都已正确生成

3. 查看错误信息，通常包含具体的问题描述

## 扩展学习

基于这些数据，您可以尝试：

- **高级聚类算法**: DBSCAN, 层次聚类, 谱聚类
- **时间序列分析**: ARIMA, GARCH, Prophet
- **机器学习**: 随机森林, XGBoost, 神经网络
- **投资组合优化**: 马科维茨模型, 风险平价
- **风险管理**: VaR计算, 压力测试

祝您学习愉快！🚀