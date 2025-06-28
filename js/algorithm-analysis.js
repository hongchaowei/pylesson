// 算法复杂度分析和性能基准测试模块

/**
 * 算法复杂度分析器
 */
class AlgorithmComplexityAnalyzer {
    constructor() {
        this.results = [];
        this.benchmarks = new Map();
    }

    /**
     * 分析时间复杂度
     * @param {Function} algorithm - 待分析的算法函数
     * @param {Function} dataGenerator - 数据生成器
     * @param {Array} inputSizes - 输入规模数组
     * @param {string} algorithmName - 算法名称
     */
    analyzeTimeComplexity(algorithm, dataGenerator, inputSizes, algorithmName) {
        const results = [];
        
        console.log(`\n=== ${algorithmName} 时间复杂度分析 ===`);
        
        for (const size of inputSizes) {
            const data = dataGenerator(size);
            const startTime = performance.now();
            
            // 执行算法
            algorithm(data);
            
            const endTime = performance.now();
            const executionTime = endTime - startTime;
            
            results.push({
                inputSize: size,
                executionTime: executionTime,
                algorithm: algorithmName
            });
            
            console.log(`输入规模: ${size}, 执行时间: ${executionTime.toFixed(4)}ms`);
        }
        
        // 分析复杂度趋势
        this.analyzeComplexityTrend(results, algorithmName);
        
        return results;
    }

    /**
     * 分析空间复杂度
     * @param {Function} algorithm - 待分析的算法函数
     * @param {number} inputSize - 输入规模
     * @param {string} algorithmName - 算法名称
     */
    analyzeSpaceComplexity(algorithm, inputSize, algorithmName) {
        console.log(`\n=== ${algorithmName} 空间复杂度分析 ===`);
        
        // 监控内存使用（简化版本）
        const memoryBefore = this.getMemoryUsage();
        
        // 执行算法
        const result = algorithm(inputSize);
        
        const memoryAfter = this.getMemoryUsage();
        const memoryUsed = memoryAfter - memoryBefore;
        
        console.log(`输入规模: ${inputSize}`);
        console.log(`内存使用: ${memoryUsed.toFixed(2)}MB`);
        console.log(`空间复杂度估算: O(${this.estimateSpaceComplexity(inputSize, memoryUsed)})`);
        
        return {
            inputSize,
            memoryUsed,
            algorithm: algorithmName
        };
    }

    /**
     * 获取内存使用情况（简化版本）
     */
    getMemoryUsage() {
        if (performance.memory) {
            return performance.memory.usedJSHeapSize / 1024 / 1024; // MB
        }
        return 0;
    }

    /**
     * 估算空间复杂度
     */
    estimateSpaceComplexity(inputSize, memoryUsed) {
        const ratio = memoryUsed / inputSize;
        
        if (ratio < 0.001) return '1';
        if (ratio < 0.1) return 'log n';
        if (ratio < 2) return 'n';
        if (ratio < inputSize) return 'n log n';
        return 'n²';
    }

    /**
     * 分析复杂度趋势
     */
    analyzeComplexityTrend(results, algorithmName) {
        if (results.length < 2) return;
        
        console.log(`\n${algorithmName} 复杂度趋势分析:`);
        
        for (let i = 1; i < results.length; i++) {
            const prev = results[i - 1];
            const curr = results[i];
            
            const sizeRatio = curr.inputSize / prev.inputSize;
            const timeRatio = curr.executionTime / prev.executionTime;
            
            let complexity = 'Unknown';
            if (timeRatio < sizeRatio * 0.5) complexity = 'O(log n) 或更好';
            else if (timeRatio < sizeRatio * 1.5) complexity = 'O(n)';
            else if (timeRatio < sizeRatio * sizeRatio * 0.5) complexity = 'O(n log n)';
            else if (timeRatio < sizeRatio * sizeRatio * 1.5) complexity = 'O(n²)';
            else complexity = 'O(n³) 或更差';
            
            console.log(`规模 ${prev.inputSize} → ${curr.inputSize}: 时间比率 ${timeRatio.toFixed(2)}, 估算复杂度: ${complexity}`);
        }
    }

    /**
     * 性能基准测试
     */
    benchmark(algorithms, dataGenerator, inputSize, iterations = 100) {
        console.log(`\n=== 性能基准测试 (输入规模: ${inputSize}, 迭代次数: ${iterations}) ===`);
        
        const results = [];
        
        for (const [name, algorithm] of Object.entries(algorithms)) {
            const times = [];
            
            // 预热
            for (let i = 0; i < 10; i++) {
                const data = dataGenerator(inputSize);
                algorithm(data);
            }
            
            // 正式测试
            for (let i = 0; i < iterations; i++) {
                const data = dataGenerator(inputSize);
                const startTime = performance.now();
                algorithm(data);
                const endTime = performance.now();
                times.push(endTime - startTime);
            }
            
            const avgTime = times.reduce((a, b) => a + b) / times.length;
            const minTime = Math.min(...times);
            const maxTime = Math.max(...times);
            const stdDev = Math.sqrt(times.reduce((sq, n) => sq + Math.pow(n - avgTime, 2), 0) / times.length);
            
            results.push({
                algorithm: name,
                avgTime,
                minTime,
                maxTime,
                stdDev,
                times
            });
            
            console.log(`${name}:`);
            console.log(`  平均时间: ${avgTime.toFixed(4)}ms`);
            console.log(`  最小时间: ${minTime.toFixed(4)}ms`);
            console.log(`  最大时间: ${maxTime.toFixed(4)}ms`);
            console.log(`  标准差: ${stdDev.toFixed(4)}ms`);
        }
        
        // 排序并显示排名
        results.sort((a, b) => a.avgTime - b.avgTime);
        console.log('\n性能排名:');
        results.forEach((result, index) => {
            console.log(`${index + 1}. ${result.algorithm}: ${result.avgTime.toFixed(4)}ms`);
        });
        
        return results;
    }
}

/**
 * 金融算法性能测试套件
 */
class FinancialAlgorithmBenchmark {
    constructor() {
        this.analyzer = new AlgorithmComplexityAnalyzer();
    }

    /**
     * 排序算法性能对比
     */
    benchmarkSortingAlgorithms() {
        console.log('\n🔄 排序算法性能对比测试');
        
        const algorithms = {
            '快速排序': this.quickSort.bind(this),
            '归并排序': this.mergeSort.bind(this),
            '堆排序': this.heapSort.bind(this),
            '内置排序': (arr) => [...arr].sort((a, b) => a - b)
        };
        
        const dataGenerator = (size) => {
            return Array.from({ length: size }, () => Math.random() * 1000);
        };
        
        // 不同规模的性能测试
        const inputSizes = [1000, 5000, 10000, 20000];
        
        for (const size of inputSizes) {
            console.log(`\n--- 输入规模: ${size} ---`);
            this.analyzer.benchmark(algorithms, dataGenerator, size, 50);
        }
        
        // 复杂度分析
        for (const [name, algorithm] of Object.entries(algorithms)) {
            this.analyzer.analyzeTimeComplexity(algorithm, dataGenerator, inputSizes, name);
        }
    }

    /**
     * 技术指标计算性能测试
     */
    benchmarkTechnicalIndicators() {
        console.log('\n📊 技术指标计算性能测试');
        
        const algorithms = {
            'SMA计算': this.calculateSMA.bind(this),
            'EMA计算': this.calculateEMA.bind(this),
            'RSI计算': this.calculateRSI.bind(this),
            'MACD计算': this.calculateMACD.bind(this),
            'Bollinger Bands': this.calculateBollingerBands.bind(this)
        };
        
        const priceDataGenerator = (size) => {
            const data = [];
            let price = 100;
            for (let i = 0; i < size; i++) {
                price += (Math.random() - 0.5) * 2;
                data.push({
                    date: new Date(Date.now() - (size - i) * 24 * 60 * 60 * 1000),
                    close: price,
                    high: price + Math.random(),
                    low: price - Math.random(),
                    volume: Math.floor(Math.random() * 1000000)
                });
            }
            return data;
        };
        
        const inputSizes = [252, 1000, 2500, 5000]; // 1年到20年的交易日数据
        
        for (const size of inputSizes) {
            console.log(`\n--- 数据长度: ${size}天 ---`);
            this.analyzer.benchmark(algorithms, priceDataGenerator, size, 100);
        }
    }

    /**
     * 投资组合优化算法测试
     */
    benchmarkPortfolioOptimization() {
        console.log('\n💼 投资组合优化算法性能测试');
        
        const algorithms = {
            '等权重组合': this.equalWeightPortfolio.bind(this),
            '最小方差组合': this.minimumVariancePortfolio.bind(this),
            '风险平价组合': this.riskParityPortfolio.bind(this),
            '最大夏普比率组合': this.maxSharpePortfolio.bind(this)
        };
        
        const returnsDataGenerator = (numAssets) => {
            const returns = [];
            const periods = 252; // 一年的交易日
            
            for (let i = 0; i < periods; i++) {
                const dayReturns = [];
                for (let j = 0; j < numAssets; j++) {
                    dayReturns.push((Math.random() - 0.5) * 0.04); // -2% to 2% daily return
                }
                returns.push(dayReturns);
            }
            return returns;
        };
        
        const assetCounts = [10, 20, 50, 100];
        
        for (const count of assetCounts) {
            console.log(`\n--- 资产数量: ${count} ---`);
            this.analyzer.benchmark(algorithms, returnsDataGenerator, count, 20);
        }
    }

    /**
     * 风险计算算法测试
     */
    benchmarkRiskCalculations() {
        console.log('\n⚠️ 风险计算算法性能测试');
        
        const algorithms = {
            'VaR历史模拟法': this.historicalVaR.bind(this),
            'VaR参数法': this.parametricVaR.bind(this),
            'VaR蒙特卡洛法': this.monteCarloVaR.bind(this),
            'CVaR计算': this.calculateCVaR.bind(this),
            '最大回撤计算': this.calculateMaxDrawdown.bind(this)
        };
        
        const returnsGenerator = (size) => {
            return Array.from({ length: size }, () => (Math.random() - 0.5) * 0.06);
        };
        
        const dataSizes = [252, 1000, 2500, 5000];
        
        for (const size of dataSizes) {
            console.log(`\n--- 数据长度: ${size} ---`);
            this.analyzer.benchmark(algorithms, returnsGenerator, size, 100);
        }
    }

    // ==================== 算法实现 ====================

    /**
     * 快速排序
     */
    quickSort(arr) {
        if (arr.length <= 1) return arr;
        
        const pivot = arr[Math.floor(arr.length / 2)];
        const left = arr.filter(x => x < pivot);
        const middle = arr.filter(x => x === pivot);
        const right = arr.filter(x => x > pivot);
        
        return [...this.quickSort(left), ...middle, ...this.quickSort(right)];
    }

    /**
     * 归并排序
     */
    mergeSort(arr) {
        if (arr.length <= 1) return arr;
        
        const mid = Math.floor(arr.length / 2);
        const left = this.mergeSort(arr.slice(0, mid));
        const right = this.mergeSort(arr.slice(mid));
        
        return this.merge(left, right);
    }

    merge(left, right) {
        const result = [];
        let i = 0, j = 0;
        
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result.push(left[i++]);
            } else {
                result.push(right[j++]);
            }
        }
        
        return result.concat(left.slice(i)).concat(right.slice(j));
    }

    /**
     * 堆排序
     */
    heapSort(arr) {
        const sorted = [...arr];
        const n = sorted.length;
        
        // 构建最大堆
        for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
            this.heapify(sorted, n, i);
        }
        
        // 提取元素
        for (let i = n - 1; i > 0; i--) {
            [sorted[0], sorted[i]] = [sorted[i], sorted[0]];
            this.heapify(sorted, i, 0);
        }
        
        return sorted;
    }

    heapify(arr, n, i) {
        let largest = i;
        const left = 2 * i + 1;
        const right = 2 * i + 2;
        
        if (left < n && arr[left] > arr[largest]) largest = left;
        if (right < n && arr[right] > arr[largest]) largest = right;
        
        if (largest !== i) {
            [arr[i], arr[largest]] = [arr[largest], arr[i]];
            this.heapify(arr, n, largest);
        }
    }

    /**
     * 简单移动平均线
     * 时间复杂度: O(n*m) - n为数据长度，m为窗口大小
     * 空间复杂度: O(n)
     */
    calculateSMA(data, period = 20) {
        const result = [];
        for (let i = period - 1; i < data.length; i++) {
            const sum = data.slice(i - period + 1, i + 1)
                .reduce((acc, item) => acc + item.close, 0);
            result.push(sum / period);
        }
        return result;
    }

    /**
     * 指数移动平均线
     * 时间复杂度: O(n)
     * 空间复杂度: O(n)
     */
    calculateEMA(data, period = 20) {
        const multiplier = 2 / (period + 1);
        const result = [data[0].close];
        
        for (let i = 1; i < data.length; i++) {
            const ema = (data[i].close * multiplier) + (result[i - 1] * (1 - multiplier));
            result.push(ema);
        }
        
        return result;
    }

    /**
     * RSI计算
     * 时间复杂度: O(n)
     * 空间复杂度: O(n)
     */
    calculateRSI(data, period = 14) {
        const gains = [];
        const losses = [];
        const rsi = [];
        
        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);
            
            if (i >= period) {
                const avgGain = gains.slice(-period).reduce((a, b) => a + b) / period;
                const avgLoss = losses.slice(-period).reduce((a, b) => a + b) / period;
                const rs = avgGain / avgLoss;
                rsi.push(100 - (100 / (1 + rs)));
            }
        }
        
        return rsi;
    }

    /**
     * MACD计算
     * 时间复杂度: O(n)
     * 空间复杂度: O(n)
     */
    calculateMACD(data, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) {
        const ema12 = this.calculateEMA(data, fastPeriod);
        const ema26 = this.calculateEMA(data, slowPeriod);
        
        const macdLine = [];
        for (let i = slowPeriod - 1; i < data.length; i++) {
            macdLine.push(ema12[i] - ema26[i]);
        }
        
        // 计算信号线（MACD的EMA）
        const signalLine = this.calculateEMAFromArray(macdLine, signalPeriod);
        
        return { macdLine, signalLine };
    }

    calculateEMAFromArray(data, period) {
        const multiplier = 2 / (period + 1);
        const result = [data[0]];
        
        for (let i = 1; i < data.length; i++) {
            const ema = (data[i] * multiplier) + (result[i - 1] * (1 - multiplier));
            result.push(ema);
        }
        
        return result;
    }

    /**
     * 布林带计算
     * 时间复杂度: O(n*m)
     * 空间复杂度: O(n)
     */
    calculateBollingerBands(data, period = 20, stdDev = 2) {
        const sma = this.calculateSMA(data, period);
        const upperBand = [];
        const lowerBand = [];
        
        for (let i = period - 1; i < data.length; i++) {
            const slice = data.slice(i - period + 1, i + 1);
            const mean = sma[i - period + 1];
            const variance = slice.reduce((acc, item) => 
                acc + Math.pow(item.close - mean, 2), 0) / period;
            const std = Math.sqrt(variance);
            
            upperBand.push(mean + stdDev * std);
            lowerBand.push(mean - stdDev * std);
        }
        
        return { sma, upperBand, lowerBand };
    }

    /**
     * 等权重投资组合
     * 时间复杂度: O(1)
     * 空间复杂度: O(n)
     */
    equalWeightPortfolio(returns) {
        const numAssets = returns[0].length;
        return Array(numAssets).fill(1 / numAssets);
    }

    /**
     * 最小方差投资组合（简化版本）
     * 时间复杂度: O(n³)
     * 空间复杂度: O(n²)
     */
    minimumVariancePortfolio(returns) {
        const numAssets = returns[0].length;
        const covMatrix = this.calculateCovarianceMatrix(returns);
        
        // 简化的最小方差优化（实际应使用二次规划）
        const weights = Array(numAssets).fill(1 / numAssets);
        
        // 迭代优化（简化版本）
        for (let iter = 0; iter < 100; iter++) {
            const newWeights = [...weights];
            for (let i = 0; i < numAssets; i++) {
                // 简化的梯度下降
                let gradient = 0;
                for (let j = 0; j < numAssets; j++) {
                    gradient += covMatrix[i][j] * weights[j];
                }
                newWeights[i] = Math.max(0, weights[i] - 0.01 * gradient);
            }
            
            // 归一化
            const sum = newWeights.reduce((a, b) => a + b);
            for (let i = 0; i < numAssets; i++) {
                weights[i] = newWeights[i] / sum;
            }
        }
        
        return weights;
    }

    /**
     * 风险平价投资组合
     * 时间复杂度: O(n³)
     * 空间复杂度: O(n²)
     */
    riskParityPortfolio(returns) {
        const numAssets = returns[0].length;
        const covMatrix = this.calculateCovarianceMatrix(returns);
        
        // 简化的风险平价实现
        const weights = Array(numAssets).fill(1 / numAssets);
        
        for (let iter = 0; iter < 50; iter++) {
            const riskContributions = this.calculateRiskContributions(weights, covMatrix);
            const targetRisk = riskContributions.reduce((a, b) => a + b) / numAssets;
            
            for (let i = 0; i < numAssets; i++) {
                const adjustment = (targetRisk - riskContributions[i]) / targetRisk;
                weights[i] = Math.max(0.001, weights[i] * (1 + 0.1 * adjustment));
            }
            
            // 归一化
            const sum = weights.reduce((a, b) => a + b);
            for (let i = 0; i < numAssets; i++) {
                weights[i] /= sum;
            }
        }
        
        return weights;
    }

    /**
     * 最大夏普比率投资组合（简化版本）
     */
    maxSharpePortfolio(returns) {
        const numAssets = returns[0].length;
        const expectedReturns = this.calculateExpectedReturns(returns);
        const covMatrix = this.calculateCovarianceMatrix(returns);
        
        // 简化实现：基于期望收益率的权重分配
        const weights = expectedReturns.map(r => Math.max(0, r));
        const sum = weights.reduce((a, b) => a + b);
        
        return weights.map(w => w / sum);
    }

    /**
     * 历史模拟法VaR
     * 时间复杂度: O(n log n)
     * 空间复杂度: O(n)
     */
    historicalVaR(returns, confidence = 0.05) {
        const sortedReturns = [...returns].sort((a, b) => a - b);
        const index = Math.floor(confidence * sortedReturns.length);
        return sortedReturns[index];
    }

    /**
     * 参数法VaR
     * 时间复杂度: O(n)
     * 空间复杂度: O(1)
     */
    parametricVaR(returns, confidence = 0.05) {
        const mean = returns.reduce((a, b) => a + b) / returns.length;
        const variance = returns.reduce((acc, r) => acc + Math.pow(r - mean, 2), 0) / returns.length;
        const stdDev = Math.sqrt(variance);
        
        // 假设正态分布
        const zScore = this.inverseNormalCDF(confidence);
        return mean + zScore * stdDev;
    }

    /**
     * 蒙特卡洛法VaR
     * 时间复杂度: O(m) - m为模拟次数
     * 空间复杂度: O(m)
     */
    monteCarloVaR(returns, confidence = 0.05, simulations = 10000) {
        const mean = returns.reduce((a, b) => a + b) / returns.length;
        const variance = returns.reduce((acc, r) => acc + Math.pow(r - mean, 2), 0) / returns.length;
        const stdDev = Math.sqrt(variance);
        
        const simulatedReturns = [];
        for (let i = 0; i < simulations; i++) {
            // Box-Muller变换生成正态分布随机数
            const u1 = Math.random();
            const u2 = Math.random();
            const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
            simulatedReturns.push(mean + stdDev * z);
        }
        
        return this.historicalVaR(simulatedReturns, confidence);
    }

    /**
     * CVaR计算
     * 时间复杂度: O(n log n)
     * 空间复杂度: O(n)
     */
    calculateCVaR(returns, confidence = 0.05) {
        const var95 = this.historicalVaR(returns, confidence);
        const tailReturns = returns.filter(r => r <= var95);
        return tailReturns.reduce((a, b) => a + b) / tailReturns.length;
    }

    /**
     * 最大回撤计算
     * 时间复杂度: O(n)
     * 空间复杂度: O(1)
     */
    calculateMaxDrawdown(returns) {
        let peak = 0;
        let maxDrawdown = 0;
        let cumReturn = 0;
        
        for (const ret of returns) {
            cumReturn += ret;
            peak = Math.max(peak, cumReturn);
            const drawdown = peak - cumReturn;
            maxDrawdown = Math.max(maxDrawdown, drawdown);
        }
        
        return maxDrawdown;
    }

    // ==================== 辅助函数 ====================

    calculateCovarianceMatrix(returns) {
        const numAssets = returns[0].length;
        const numPeriods = returns.length;
        const means = Array(numAssets).fill(0);
        
        // 计算均值
        for (let i = 0; i < numPeriods; i++) {
            for (let j = 0; j < numAssets; j++) {
                means[j] += returns[i][j];
            }
        }
        for (let j = 0; j < numAssets; j++) {
            means[j] /= numPeriods;
        }
        
        // 计算协方差矩阵
        const covMatrix = Array(numAssets).fill().map(() => Array(numAssets).fill(0));
        for (let i = 0; i < numAssets; i++) {
            for (let j = 0; j < numAssets; j++) {
                let covariance = 0;
                for (let k = 0; k < numPeriods; k++) {
                    covariance += (returns[k][i] - means[i]) * (returns[k][j] - means[j]);
                }
                covMatrix[i][j] = covariance / (numPeriods - 1);
            }
        }
        
        return covMatrix;
    }

    calculateExpectedReturns(returns) {
        const numAssets = returns[0].length;
        const numPeriods = returns.length;
        const expectedReturns = Array(numAssets).fill(0);
        
        for (let i = 0; i < numPeriods; i++) {
            for (let j = 0; j < numAssets; j++) {
                expectedReturns[j] += returns[i][j];
            }
        }
        
        return expectedReturns.map(r => r / numPeriods);
    }

    calculateRiskContributions(weights, covMatrix) {
        const numAssets = weights.length;
        const portfolioVariance = this.calculatePortfolioVariance(weights, covMatrix);
        const riskContributions = [];
        
        for (let i = 0; i < numAssets; i++) {
            let marginalRisk = 0;
            for (let j = 0; j < numAssets; j++) {
                marginalRisk += covMatrix[i][j] * weights[j];
            }
            riskContributions.push(weights[i] * marginalRisk / Math.sqrt(portfolioVariance));
        }
        
        return riskContributions;
    }

    calculatePortfolioVariance(weights, covMatrix) {
        let variance = 0;
        for (let i = 0; i < weights.length; i++) {
            for (let j = 0; j < weights.length; j++) {
                variance += weights[i] * weights[j] * covMatrix[i][j];
            }
        }
        return variance;
    }

    inverseNormalCDF(p) {
        // 简化的反正态分布函数
        if (p === 0.05) return -1.645;
        if (p === 0.01) return -2.326;
        return -1.645; // 默认5%
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AlgorithmComplexityAnalyzer,
        FinancialAlgorithmBenchmark
    };
}

// 全局可用
window.AlgorithmAnalysis = {
    AlgorithmComplexityAnalyzer,
    FinancialAlgorithmBenchmark
};