#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
虚拟数据生成脚本
为课程代码生成所需的各种CSV数据文件
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 设置随机种子以确保结果可重现
np.random.seed(42)

def create_directories():
    """创建必要的目录"""
    dirs = ['data', 'cache']
    for dir_name in dirs:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"创建目录: {dir_name}")

def generate_stock_prices():
    """生成股票价格数据"""
    print("生成股票价格数据...")
    
    # 股票列表
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'JPM', 'BAC', 'TSLA', 'NVDA']
    
    # 生成日期范围（过去2年）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 过滤工作日
    dates = dates[dates.weekday < 5]  # 0-4 代表周一到周五
    
    all_data = []
    
    for stock in stocks:
        # 为每只股票生成价格数据
        initial_price = np.random.uniform(50, 300)  # 初始价格
        
        # 生成价格序列（几何布朗运动）
        returns = np.random.normal(0.0005, 0.02, len(dates))  # 日收益率
        prices = [initial_price]
        
        for ret in returns[1:]:
            new_price = prices[-1] * (1 + ret)
            prices.append(max(new_price, 1))  # 确保价格不为负
        
        # 生成OHLC数据
        for i, (date, close) in enumerate(zip(dates, prices)):
            # 生成开盘价、最高价、最低价
            daily_volatility = np.random.uniform(0.005, 0.03)
            
            open_price = close * (1 + np.random.normal(0, daily_volatility/2))
            high_price = max(open_price, close) * (1 + np.random.uniform(0, daily_volatility))
            low_price = min(open_price, close) * (1 - np.random.uniform(0, daily_volatility))
            
            # 生成成交量
            volume = np.random.randint(100000, 10000000)
            
            all_data.append({
                'date': date,
                'symbol': stock,
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close, 2),
                'volume': volume
            })
    
    df = pd.DataFrame(all_data)
    
    # 保存完整数据
    df.to_csv('stock_data.csv', index=False)
    df.to_csv('stock_prices.csv', index=False)
    
    # 保存按股票分组的数据
    for stock in stocks:
        stock_data = df[df['symbol'] == stock].copy()
        stock_data.set_index('date', inplace=True)
        stock_data.to_csv(f'data/{stock}.csv')
    
    print(f"生成了 {len(df)} 条股票价格记录")
    return df

def generate_stock_returns(stock_prices_df):
    """生成股票收益率数据"""
    print("生成股票收益率数据...")
    
    # 计算收益率
    returns_data = []
    
    for symbol in stock_prices_df['symbol'].unique():
        symbol_data = stock_prices_df[stock_prices_df['symbol'] == symbol].copy()
        symbol_data = symbol_data.sort_values('date')
        
        # 计算日收益率
        symbol_data['returns'] = symbol_data['close'].pct_change()
        
        # 移除第一行（NaN值）
        symbol_data = symbol_data.dropna()
        
        for _, row in symbol_data.iterrows():
            returns_data.append({
                'date': row['date'],
                'symbol': symbol,
                'returns': round(row['returns'], 6)
            })
    
    returns_df = pd.DataFrame(returns_data)
    
    # 透视表格式（日期为索引，股票为列）
    pivot_returns = returns_df.pivot(index='date', columns='symbol', values='returns')
    pivot_returns.to_csv('stock_returns.csv')
    
    print(f"生成了股票收益率数据，形状: {pivot_returns.shape}")
    return pivot_returns

def generate_portfolio_data():
    """生成投资组合相关数据"""
    print("生成投资组合数据...")
    
    # 生成日期范围
    dates = pd.date_range('2022-01-01', '2023-12-31', freq='D')
    dates = dates[dates.weekday < 5]  # 工作日
    
    # 投资组合收益率
    portfolio_returns = pd.DataFrame({
        'portfolio_return': np.random.normal(0.0008, 0.015, len(dates))
    }, index=dates)
    portfolio_returns.to_csv('portfolio_returns.csv')
    
    # 基准收益率
    benchmark_returns = pd.DataFrame({
        'benchmark_return': np.random.normal(0.0006, 0.012, len(dates))
    }, index=dates)
    benchmark_returns.to_csv('benchmark_returns.csv')
    
    # 投资组合权重
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'JPM']
    weights_data = []
    
    for date in dates[::30]:  # 每月更新权重
        weights = np.random.dirichlet(np.ones(len(stocks)))  # 生成权重和为1的随机权重
        for stock, weight in zip(stocks, weights):
            weights_data.append({
                'date': date,
                'symbol': stock,
                'weight': round(weight, 4)
            })
    
    weights_df = pd.DataFrame(weights_data)
    portfolio_weights = weights_df.pivot(index='date', columns='symbol', values='weight')
    portfolio_weights.to_csv('portfolio_weights.csv')
    
    # 基准权重（等权重）
    benchmark_weights = pd.DataFrame(
        np.full((len(portfolio_weights), len(stocks)), 1/len(stocks)),
        index=portfolio_weights.index,
        columns=stocks
    )
    benchmark_weights.to_csv('benchmark_weights.csv')
    
    # 资产收益率
    asset_returns_data = []
    for date in dates:
        for stock in stocks:
            asset_returns_data.append({
                'date': date,
                'symbol': stock,
                'return': np.random.normal(0.0008, 0.02)
            })
    
    asset_returns_df = pd.DataFrame(asset_returns_data)
    asset_returns = asset_returns_df.pivot(index='date', columns='symbol', values='return')
    asset_returns.to_csv('asset_returns.csv')
    
    print("生成了投资组合相关数据")

def generate_financial_features():
    """生成金融特征数据"""
    print("生成金融特征数据...")
    
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'JPM', 'BAC', 'TSLA', 'NVDA']
    
    features_data = []
    for stock in stocks:
        features_data.append({
            'ticker': stock,
            'market_cap': np.random.uniform(100, 3000),  # 市值（十亿美元）
            'pe_ratio': np.random.uniform(10, 50),       # 市盈率
            'pb_ratio': np.random.uniform(1, 10),        # 市净率
            'debt_to_equity': np.random.uniform(0.1, 2), # 负债权益比
            'roe': np.random.uniform(0.05, 0.30),        # 净资产收益率
            'revenue_growth': np.random.uniform(-0.1, 0.5), # 营收增长率
            'beta': np.random.uniform(0.5, 2.0),         # 贝塔系数
            'dividend_yield': np.random.uniform(0, 0.06) # 股息收益率
        })
    
    features_df = pd.DataFrame(features_data)
    features_df.set_index('ticker', inplace=True)
    features_df.to_csv('stock_features.csv')
    
    print(f"生成了 {len(features_df)} 只股票的特征数据")

def generate_transaction_data():
    """生成交易数据"""
    print("生成交易数据...")
    
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'JPM']
    
    # 生成随机交易记录
    transactions = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(1000):  # 生成1000条交易记录
        transaction_date = start_date + timedelta(days=np.random.randint(0, 365))
        stock = np.random.choice(stocks)
        action = np.random.choice(['buy', 'sell'])
        quantity = np.random.randint(10, 1000)
        price = np.random.uniform(50, 300)
        
        transactions.append({
            'date': transaction_date,
            'symbol': stock,
            'action': action,
            'quantity': quantity,
            'price': round(price, 2),
            'amount': round(quantity * price, 2)
        })
    
    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv('transactions.csv', index=False)
    
    print(f"生成了 {len(transactions_df)} 条交易记录")

def generate_credit_data():
    """生成信用数据"""
    print("生成信用数据...")
    
    n_samples = 10000
    
    credit_data = pd.DataFrame({
        'age': np.random.randint(18, 80, n_samples),
        'income': np.random.lognormal(10, 0.5, n_samples),
        'credit_score': np.random.randint(300, 850, n_samples),
        'debt_to_income': np.random.uniform(0, 1, n_samples),
        'employment_years': np.random.randint(0, 40, n_samples),
        'loan_amount': np.random.uniform(1000, 100000, n_samples),
        'default': np.random.binomial(1, 0.1, n_samples)  # 10%违约率
    })
    
    credit_data.to_csv('credit_data.csv', index=False)
    print(f"生成了 {len(credit_data)} 条信用数据记录")

def generate_news_data():
    """生成新闻数据"""
    print("生成新闻数据...")
    
    # 新闻标题示例
    news_titles = [
        "Tech stocks rally on strong earnings",
        "Federal Reserve hints at rate cuts",
        "Oil prices surge amid supply concerns",
        "Banking sector shows resilience",
        "Market volatility increases",
        "Economic indicators point to growth",
        "Trade tensions ease between nations",
        "Cryptocurrency market rebounds"
    ]
    
    dates = pd.date_range('2023-01-01', '2023-12-31', freq='D')
    
    news_data = []
    for date in dates:
        # 每天生成1-3条新闻
        num_news = np.random.randint(1, 4)
        for _ in range(num_news):
            news_data.append({
                'date': date,
                'title': np.random.choice(news_titles),
                'sentiment': np.random.uniform(-1, 1),  # 情感分数
                'relevance': np.random.uniform(0, 1)    # 相关性分数
            })
    
    news_df = pd.DataFrame(news_data)
    news_df.to_csv('news_data.csv', index=False)
    
    print(f"生成了 {len(news_df)} 条新闻数据")

def generate_financial_data():
    """生成综合金融数据"""
    print("生成综合金融数据...")
    
    # 生成包含多种金融指标的数据集
    dates = pd.date_range('2020-01-01', '2023-12-31', freq='D')
    dates = dates[dates.weekday < 5]  # 工作日
    
    financial_data = []
    
    for date in dates:
        financial_data.append({
            'date': date,
            'sp500': 3000 + np.cumsum(np.random.normal(0.5, 15)),
            'nasdaq': 8000 + np.cumsum(np.random.normal(0.8, 25)),
            'vix': max(10, 20 + np.random.normal(0, 5)),
            'treasury_10y': max(0.5, 2.5 + np.random.normal(0, 0.3)),
            'dxy': 95 + np.random.normal(0, 2),  # 美元指数
            'gold': 1800 + np.random.normal(0, 30),
            'oil': max(20, 70 + np.random.normal(0, 10))
        })
    
    financial_df = pd.DataFrame(financial_data)
    financial_df.to_csv('financial_data.csv', index=False)
    
    print(f"生成了 {len(financial_df)} 条综合金融数据")

def main():
    """主函数"""
    print("开始生成虚拟数据...")
    print("=" * 50)
    
    # 创建目录
    create_directories()
    
    # 生成各种数据文件
    stock_prices_df = generate_stock_prices()
    generate_stock_returns(stock_prices_df)
    generate_portfolio_data()
    generate_financial_features()
    generate_transaction_data()
    generate_credit_data()
    generate_news_data()
    generate_financial_data()
    
    print("=" * 50)
    print("所有虚拟数据生成完成！")
    print("\n生成的文件列表:")
    
    files = [
        'stock_data.csv', 'stock_prices.csv', 'stock_returns.csv',
        'portfolio_returns.csv', 'benchmark_returns.csv',
        'portfolio_weights.csv', 'benchmark_weights.csv', 'asset_returns.csv',
        'stock_features.csv', 'transactions.csv', 'credit_data.csv',
        'news_data.csv', 'financial_data.csv'
    ]
    
    for file in files:
        if os.path.exists(file):
            size = os.path.getsize(file) / 1024  # KB
            print(f"✓ {file} ({size:.1f} KB)")
    
    print("\n现在您可以运行课程中的代码示例了！")

if __name__ == "__main__":
    main()