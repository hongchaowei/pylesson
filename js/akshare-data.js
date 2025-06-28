// AkShare数据模拟模块
// 由于前端无法直接调用Python的akshare库，这里提供模拟数据和虚拟数据生成器

/**
 * 模拟股票数据生成器
 */
class MockStockData {
    constructor() {
        this.stockCodes = {
            '000001.SZ': '平安银行',
            '000002.SZ': '万科A',
            '600000.SH': '浦发银行',
            '600036.SH': '招商银行',
            '600519.SH': '贵州茅台',
            '000858.SZ': '五粮液',
            '002415.SZ': '海康威视',
            '000725.SZ': '京东方A'
        };
    }

    /**
     * 生成随机股价数据
     * @param {string} symbol - 股票代码
     * @param {number} days - 天数
     * @param {number} basePrice - 基础价格
     */
    generateStockPrices(symbol, days = 252, basePrice = 100) {
        const data = [];
        let currentPrice = basePrice;
        const startDate = new Date();
        startDate.setDate(startDate.getDate() - days);

        for (let i = 0; i < days; i++) {
            const date = new Date(startDate);
            date.setDate(date.getDate() + i);
            
            // 模拟价格波动（几何布朗运动）
            const drift = 0.0001; // 年化收益率
            const volatility = 0.02; // 日波动率
            const randomShock = (Math.random() - 0.5) * 2;
            const priceChange = currentPrice * (drift + volatility * randomShock);
            
            currentPrice = Math.max(currentPrice + priceChange, 1); // 确保价格为正
            
            const open = currentPrice * (1 + (Math.random() - 0.5) * 0.01);
            const high = Math.max(open, currentPrice) * (1 + Math.random() * 0.02);
            const low = Math.min(open, currentPrice) * (1 - Math.random() * 0.02);
            const volume = Math.floor(Math.random() * 1000000 + 100000);
            
            data.push({
                date: date.toISOString().split('T')[0],
                open: parseFloat(open.toFixed(2)),
                high: parseFloat(high.toFixed(2)),
                low: parseFloat(low.toFixed(2)),
                close: parseFloat(currentPrice.toFixed(2)),
                volume: volume,
                symbol: symbol,
                name: this.stockCodes[symbol] || '未知股票'
            });
        }
        
        return data;
    }

    /**
     * 获取股票基本信息
     * @param {string} symbol - 股票代码
     */
    getStockInfo(symbol) {
        const baseData = {
            symbol: symbol,
            name: this.stockCodes[symbol] || '未知股票',
            market: symbol.endsWith('.SH') ? '上海证券交易所' : '深圳证券交易所',
            industry: this.getRandomIndustry(),
            marketCap: Math.floor(Math.random() * 1000000000000), // 随机市值
            pe: parseFloat((Math.random() * 50 + 5).toFixed(2)),
            pb: parseFloat((Math.random() * 10 + 0.5).toFixed(2)),
            roe: parseFloat((Math.random() * 30 + 5).toFixed(2))
        };
        
        return baseData;
    }

    /**
     * 获取随机行业
     */
    getRandomIndustry() {
        const industries = [
            '银行', '房地产', '白酒', '科技', '医药',
            '新能源', '汽车', '电子', '化工', '钢铁'
        ];
        return industries[Math.floor(Math.random() * industries.length)];
    }

    /**
     * 生成财务数据
     * @param {string} symbol - 股票代码
     * @param {number} quarters - 季度数
     */
    generateFinancialData(symbol, quarters = 12) {
        const data = [];
        const currentDate = new Date();
        
        for (let i = quarters - 1; i >= 0; i--) {
            const quarter = new Date(currentDate);
            quarter.setMonth(quarter.getMonth() - i * 3);
            
            const revenue = Math.floor(Math.random() * 10000000000 + 1000000000);
            const netProfit = Math.floor(revenue * (Math.random() * 0.2 + 0.05));
            
            data.push({
                period: `${quarter.getFullYear()}Q${Math.floor(quarter.getMonth() / 3) + 1}`,
                revenue: revenue,
                netProfit: netProfit,
                grossMargin: parseFloat((Math.random() * 50 + 20).toFixed(2)),
                netMargin: parseFloat(((netProfit / revenue) * 100).toFixed(2)),
                roe: parseFloat((Math.random() * 25 + 5).toFixed(2)),
                roa: parseFloat((Math.random() * 15 + 2).toFixed(2)),
                debtRatio: parseFloat((Math.random() * 60 + 20).toFixed(2))
            });
        }
        
        return data;
    }

    /**
     * 生成技术指标数据
     * @param {Array} priceData - 价格数据
     */
    calculateTechnicalIndicators(priceData) {
        const indicators = [];
        
        for (let i = 0; i < priceData.length; i++) {
            const data = priceData[i];
            const indicator = {
                date: data.date,
                close: data.close
            };
            
            // 计算移动平均线
            if (i >= 4) {
                const ma5 = priceData.slice(i - 4, i + 1)
                    .reduce((sum, d) => sum + d.close, 0) / 5;
                indicator.ma5 = parseFloat(ma5.toFixed(2));
            }
            
            if (i >= 19) {
                const ma20 = priceData.slice(i - 19, i + 1)
                    .reduce((sum, d) => sum + d.close, 0) / 20;
                indicator.ma20 = parseFloat(ma20.toFixed(2));
            }
            
            // 计算RSI
            if (i >= 13) {
                const gains = [];
                const losses = [];
                
                for (let j = i - 13; j <= i; j++) {
                    if (j > 0) {
                        const change = priceData[j].close - priceData[j - 1].close;
                        if (change > 0) {
                            gains.push(change);
                            losses.push(0);
                        } else {
                            gains.push(0);
                            losses.push(Math.abs(change));
                        }
                    }
                }
                
                const avgGain = gains.reduce((sum, g) => sum + g, 0) / gains.length;
                const avgLoss = losses.reduce((sum, l) => sum + l, 0) / losses.length;
                
                if (avgLoss !== 0) {
                    const rs = avgGain / avgLoss;
                    indicator.rsi = parseFloat((100 - (100 / (1 + rs))).toFixed(2));
                }
            }
            
            // 计算MACD
            if (i >= 25) {
                // 简化的MACD计算
                const ema12 = this.calculateEMA(priceData.slice(0, i + 1), 12);
                const ema26 = this.calculateEMA(priceData.slice(0, i + 1), 26);
                indicator.macd = parseFloat((ema12 - ema26).toFixed(4));
            }
            
            indicators.push(indicator);
        }
        
        return indicators;
    }

    /**
     * 计算指数移动平均线
     * @param {Array} data - 价格数据
     * @param {number} period - 周期
     */
    calculateEMA(data, period) {
        const multiplier = 2 / (period + 1);
        let ema = data[0].close;
        
        for (let i = 1; i < data.length; i++) {
            ema = (data[i].close * multiplier) + (ema * (1 - multiplier));
        }
        
        return ema;
    }
}

/**
 * 模拟宏观经济数据
 */
class MockMacroData {
    /**
     * 生成GDP数据
     * @param {number} years - 年数
     */
    generateGDPData(years = 10) {
        const data = [];
        const currentYear = new Date().getFullYear();
        let baseGDP = 100; // 万亿元
        
        for (let i = years - 1; i >= 0; i--) {
            const year = currentYear - i;
            const growthRate = Math.random() * 0.04 + 0.06; // 6%-10%增长率
            baseGDP *= (1 + growthRate);
            
            data.push({
                year: year,
                gdp: parseFloat(baseGDP.toFixed(2)),
                growthRate: parseFloat((growthRate * 100).toFixed(2)),
                quarter: [
                    { q: 'Q1', value: baseGDP * 0.24 },
                    { q: 'Q2', value: baseGDP * 0.25 },
                    { q: 'Q3', value: baseGDP * 0.25 },
                    { q: 'Q4', value: baseGDP * 0.26 }
                ]
            });
        }
        
        return data;
    }

    /**
     * 生成CPI数据
     * @param {number} months - 月数
     */
    generateCPIData(months = 36) {
        const data = [];
        const currentDate = new Date();
        let baseCPI = 100;
        
        for (let i = months - 1; i >= 0; i--) {
            const date = new Date(currentDate);
            date.setMonth(date.getMonth() - i);
            
            const monthlyChange = (Math.random() - 0.5) * 0.01; // -0.5% to 0.5%
            baseCPI *= (1 + monthlyChange);
            
            data.push({
                date: date.toISOString().split('T')[0].substring(0, 7), // YYYY-MM
                cpi: parseFloat(baseCPI.toFixed(2)),
                yoyChange: parseFloat(((Math.random() * 4 + 1)).toFixed(2)), // 1%-5%
                momChange: parseFloat((monthlyChange * 100).toFixed(2))
            });
        }
        
        return data;
    }

    /**
     * 生成利率数据
     * @param {number} months - 月数
     */
    generateInterestRateData(months = 24) {
        const data = [];
        const currentDate = new Date();
        let baseRate = 4.35; // 基准利率
        
        for (let i = months - 1; i >= 0; i--) {
            const date = new Date(currentDate);
            date.setMonth(date.getMonth() - i);
            
            // 利率变化较小
            const change = (Math.random() - 0.5) * 0.5;
            baseRate = Math.max(0.1, baseRate + change);
            
            data.push({
                date: date.toISOString().split('T')[0].substring(0, 7),
                lpr1y: parseFloat(baseRate.toFixed(2)),
                lpr5y: parseFloat((baseRate + 0.65).toFixed(2)),
                depositRate: parseFloat((baseRate - 2.1).toFixed(2)),
                loanRate: parseFloat((baseRate + 1.5).toFixed(2))
            });
        }
        
        return data;
    }
}

/**
 * 模拟期货和期权数据
 */
class MockDerivativesData {
    /**
     * 生成期货数据
     * @param {string} contract - 合约代码
     * @param {number} days - 天数
     */
    generateFuturesData(contract = 'IF2312', days = 100) {
        const data = [];
        let basePrice = 4000;
        const currentDate = new Date();
        
        for (let i = days - 1; i >= 0; i--) {
            const date = new Date(currentDate);
            date.setDate(date.getDate() - i);
            
            const volatility = 0.025;
            const change = basePrice * volatility * (Math.random() - 0.5) * 2;
            basePrice = Math.max(basePrice + change, 1000);
            
            const open = basePrice * (1 + (Math.random() - 0.5) * 0.01);
            const high = Math.max(open, basePrice) * (1 + Math.random() * 0.02);
            const low = Math.min(open, basePrice) * (1 - Math.random() * 0.02);
            
            data.push({
                date: date.toISOString().split('T')[0],
                contract: contract,
                open: parseFloat(open.toFixed(2)),
                high: parseFloat(high.toFixed(2)),
                low: parseFloat(low.toFixed(2)),
                close: parseFloat(basePrice.toFixed(2)),
                volume: Math.floor(Math.random() * 100000 + 10000),
                openInterest: Math.floor(Math.random() * 500000 + 100000)
            });
        }
        
        return data;
    }

    /**
     * 生成期权数据
     * @param {string} underlying - 标的资产
     * @param {number} spotPrice - 现货价格
     */
    generateOptionsData(underlying = '50ETF', spotPrice = 3.0) {
        const data = [];
        const strikes = [2.8, 2.9, 3.0, 3.1, 3.2];
        const expirations = ['2024-01', '2024-02', '2024-03'];
        
        expirations.forEach(expiry => {
            strikes.forEach(strike => {
                // 计算期权价格（简化的Black-Scholes）
                const timeToExpiry = 0.25; // 3个月
                const riskFreeRate = 0.03;
                const volatility = 0.25;
                
                const callPrice = this.blackScholes('call', spotPrice, strike, timeToExpiry, riskFreeRate, volatility);
                const putPrice = this.blackScholes('put', spotPrice, strike, timeToExpiry, riskFreeRate, volatility);
                
                data.push({
                    underlying: underlying,
                    expiration: expiry,
                    strike: strike,
                    type: 'call',
                    price: parseFloat(callPrice.toFixed(4)),
                    impliedVol: parseFloat((volatility * 100).toFixed(2)),
                    delta: parseFloat(this.calculateDelta('call', spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4)),
                    gamma: parseFloat(this.calculateGamma(spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4)),
                    theta: parseFloat(this.calculateTheta('call', spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4)),
                    vega: parseFloat(this.calculateVega(spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4))
                });
                
                data.push({
                    underlying: underlying,
                    expiration: expiry,
                    strike: strike,
                    type: 'put',
                    price: parseFloat(putPrice.toFixed(4)),
                    impliedVol: parseFloat((volatility * 100).toFixed(2)),
                    delta: parseFloat(this.calculateDelta('put', spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4)),
                    gamma: parseFloat(this.calculateGamma(spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4)),
                    theta: parseFloat(this.calculateTheta('put', spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4)),
                    vega: parseFloat(this.calculateVega(spotPrice, strike, timeToExpiry, riskFreeRate, volatility).toFixed(4))
                });
            });
        });
        
        return data;
    }

    /**
     * Black-Scholes期权定价公式
     */
    blackScholes(type, S, K, T, r, sigma) {
        const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
        const d2 = d1 - sigma * Math.sqrt(T);
        
        if (type === 'call') {
            return S * this.normalCDF(d1) - K * Math.exp(-r * T) * this.normalCDF(d2);
        } else {
            return K * Math.exp(-r * T) * this.normalCDF(-d2) - S * this.normalCDF(-d1);
        }
    }

    /**
     * 计算Delta
     */
    calculateDelta(type, S, K, T, r, sigma) {
        const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
        
        if (type === 'call') {
            return this.normalCDF(d1);
        } else {
            return this.normalCDF(d1) - 1;
        }
    }

    /**
     * 计算Gamma
     */
    calculateGamma(S, K, T, r, sigma) {
        const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
        return this.normalPDF(d1) / (S * sigma * Math.sqrt(T));
    }

    /**
     * 计算Theta
     */
    calculateTheta(type, S, K, T, r, sigma) {
        const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
        const d2 = d1 - sigma * Math.sqrt(T);
        
        const term1 = -(S * this.normalPDF(d1) * sigma) / (2 * Math.sqrt(T));
        
        if (type === 'call') {
            const term2 = -r * K * Math.exp(-r * T) * this.normalCDF(d2);
            return (term1 + term2) / 365;
        } else {
            const term2 = r * K * Math.exp(-r * T) * this.normalCDF(-d2);
            return (term1 + term2) / 365;
        }
    }

    /**
     * 计算Vega
     */
    calculateVega(S, K, T, r, sigma) {
        const d1 = (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (sigma * Math.sqrt(T));
        return S * this.normalPDF(d1) * Math.sqrt(T) / 100;
    }

    /**
     * 标准正态分布累积分布函数
     */
    normalCDF(x) {
        return 0.5 * (1 + this.erf(x / Math.sqrt(2)));
    }

    /**
     * 标准正态分布概率密度函数
     */
    normalPDF(x) {
        return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI);
    }

    /**
     * 误差函数近似
     */
    erf(x) {
        const a1 = 0.254829592;
        const a2 = -0.284496736;
        const a3 = 1.421413741;
        const a4 = -1.453152027;
        const a5 = 1.061405429;
        const p = 0.3275911;
        
        const sign = x >= 0 ? 1 : -1;
        x = Math.abs(x);
        
        const t = 1.0 / (1.0 + p * x);
        const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
        
        return sign * y;
    }
}

// 创建全局实例
const mockStockData = new MockStockData();
const mockMacroData = new MockMacroData();
const mockDerivativesData = new MockDerivativesData();

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MockStockData,
        MockMacroData,
        MockDerivativesData,
        mockStockData,
        mockMacroData,
        mockDerivativesData
    };
}