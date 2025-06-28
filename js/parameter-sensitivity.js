// 参数敏感性分析模块

/**
 * 参数敏感性分析器
 */
class ParameterSensitivityAnalyzer {
    constructor() {
        this.results = new Map();
        this.charts = new Map();
    }

    /**
     * 分析单参数敏感性
     * @param {Function} algorithm - 算法函数
     * @param {Object} baseParams - 基础参数
     * @param {string} paramName - 要分析的参数名
     * @param {Array} paramValues - 参数值范围
     * @param {Array} data - 输入数据
     * @param {Function} evaluator - 评估函数
     */
    analyzeSingleParameter(algorithm, baseParams, paramName, paramValues, data, evaluator) {
        console.log(`\n=== ${paramName} 敏感性分析 ===`);
        
        const results = [];
        const baseResult = evaluator(algorithm(data, baseParams));
        
        console.log(`基准值 (${paramName}=${baseParams[paramName]}): ${baseResult.toFixed(6)}`);
        
        for (const value of paramValues) {
            const params = { ...baseParams, [paramName]: value };
            const result = algorithm(data, params);
            const evaluation = evaluator(result);
            
            const sensitivity = ((evaluation - baseResult) / baseResult) * 100;
            
            results.push({
                paramValue: value,
                result: evaluation,
                sensitivity: sensitivity,
                relativeChange: ((value - baseParams[paramName]) / baseParams[paramName]) * 100
            });
            
            console.log(`${paramName}=${value}: 结果=${evaluation.toFixed(6)}, 敏感性=${sensitivity.toFixed(2)}%`);
        }
        
        this.results.set(paramName, results);
        return results;
    }

    /**
     * 分析多参数敏感性（网格搜索）
     * @param {Function} algorithm - 算法函数
     * @param {Object} baseParams - 基础参数
     * @param {Object} paramRanges - 参数范围 {param1: [values], param2: [values]}
     * @param {Array} data - 输入数据
     * @param {Function} evaluator - 评估函数
     */
    analyzeMultipleParameters(algorithm, baseParams, paramRanges, data, evaluator) {
        console.log('\n=== 多参数敏感性分析 ===');
        
        const paramNames = Object.keys(paramRanges);
        const results = [];
        
        // 生成参数组合
        const combinations = this.generateParameterCombinations(paramRanges);
        
        console.log(`总共 ${combinations.length} 种参数组合`);
        
        for (let i = 0; i < combinations.length; i++) {
            const params = { ...baseParams, ...combinations[i] };
            const result = algorithm(data, params);
            const evaluation = evaluator(result);
            
            results.push({
                params: combinations[i],
                result: evaluation,
                index: i
            });
            
            if (i % Math.floor(combinations.length / 10) === 0) {
                console.log(`进度: ${((i / combinations.length) * 100).toFixed(1)}%`);
            }
        }
        
        // 找出最优和最差结果
        const sortedResults = [...results].sort((a, b) => b.result - a.result);
        const best = sortedResults[0];
        const worst = sortedResults[sortedResults.length - 1];
        
        console.log('\n最优参数组合:');
        console.log(JSON.stringify(best.params, null, 2));
        console.log(`结果: ${best.result.toFixed(6)}`);
        
        console.log('\n最差参数组合:');
        console.log(JSON.stringify(worst.params, null, 2));
        console.log(`结果: ${worst.result.toFixed(6)}`);
        
        this.results.set('multiParam', results);
        return results;
    }

    /**
     * 分析参数交互效应
     * @param {Function} algorithm - 算法函数
     * @param {Object} baseParams - 基础参数
     * @param {string} param1 - 第一个参数
     * @param {string} param2 - 第二个参数
     * @param {Array} values1 - 第一个参数的值
     * @param {Array} values2 - 第二个参数的值
     * @param {Array} data - 输入数据
     * @param {Function} evaluator - 评估函数
     */
    analyzeParameterInteraction(algorithm, baseParams, param1, param2, values1, values2, data, evaluator) {
        console.log(`\n=== ${param1} 与 ${param2} 交互效应分析 ===`);
        
        const results = [];
        
        for (const val1 of values1) {
            for (const val2 of values2) {
                const params = { 
                    ...baseParams, 
                    [param1]: val1, 
                    [param2]: val2 
                };
                
                const result = algorithm(data, params);
                const evaluation = evaluator(result);
                
                results.push({
                    [param1]: val1,
                    [param2]: val2,
                    result: evaluation
                });
            }
        }
        
        // 分析交互效应
        this.analyzeInteractionEffects(results, param1, param2);
        
        this.results.set(`${param1}_${param2}_interaction`, results);
        return results;
    }

    /**
     * 生成参数组合
     */
    generateParameterCombinations(paramRanges) {
        const paramNames = Object.keys(paramRanges);
        const combinations = [];
        
        function generateCombos(index, current) {
            if (index === paramNames.length) {
                combinations.push({ ...current });
                return;
            }
            
            const paramName = paramNames[index];
            const values = paramRanges[paramName];
            
            for (const value of values) {
                current[paramName] = value;
                generateCombos(index + 1, current);
            }
        }
        
        generateCombos(0, {});
        return combinations;
    }

    /**
     * 分析交互效应
     */
    analyzeInteractionEffects(results, param1, param2) {
        // 计算主效应
        const param1Effects = this.calculateMainEffect(results, param1);
        const param2Effects = this.calculateMainEffect(results, param2);
        
        console.log(`\n${param1} 主效应:`);
        param1Effects.forEach(effect => {
            console.log(`  ${param1}=${effect.value}: 平均结果=${effect.avgResult.toFixed(6)}`);
        });
        
        console.log(`\n${param2} 主效应:`);
        param2Effects.forEach(effect => {
            console.log(`  ${param2}=${effect.value}: 平均结果=${effect.avgResult.toFixed(6)}`);
        });
        
        // 计算交互效应
        const interactionEffect = this.calculateInteractionEffect(results, param1, param2);
        console.log(`\n交互效应强度: ${interactionEffect.toFixed(6)}`);
        
        if (Math.abs(interactionEffect) > 0.1) {
            console.log('⚠️ 检测到显著的参数交互效应！');
        } else {
            console.log('✅ 参数间交互效应较弱，可独立优化');
        }
    }

    /**
     * 计算主效应
     */
    calculateMainEffect(results, paramName) {
        const groups = new Map();
        
        results.forEach(result => {
            const value = result[paramName];
            if (!groups.has(value)) {
                groups.set(value, []);
            }
            groups.get(value).push(result.result);
        });
        
        const effects = [];
        groups.forEach((values, paramValue) => {
            const avgResult = values.reduce((a, b) => a + b) / values.length;
            effects.push({ value: paramValue, avgResult });
        });
        
        return effects.sort((a, b) => a.value - b.value);
    }

    /**
     * 计算交互效应
     */
    calculateInteractionEffect(results, param1, param2) {
        const overallMean = results.reduce((sum, r) => sum + r.result, 0) / results.length;
        
        // 计算每个组合的偏差
        let interactionSum = 0;
        const param1Values = [...new Set(results.map(r => r[param1]))];
        const param2Values = [...new Set(results.map(r => r[param2]))];
        
        for (const val1 of param1Values) {
            for (const val2 of param2Values) {
                const cellResults = results.filter(r => 
                    r[param1] === val1 && r[param2] === val2
                );
                
                if (cellResults.length > 0) {
                    const cellMean = cellResults.reduce((sum, r) => sum + r.result, 0) / cellResults.length;
                    
                    // 计算该组合相对于整体均值的偏差
                    const deviation = Math.abs(cellMean - overallMean);
                    interactionSum += deviation;
                }
            }
        }
        
        return interactionSum / (param1Values.length * param2Values.length);
    }

    /**
     * 创建敏感性分析图表
     */
    createSensitivityChart(paramName, containerId) {
        const results = this.results.get(paramName);
        if (!results) {
            console.error(`未找到参数 ${paramName} 的分析结果`);
            return;
        }
        
        const trace1 = {
            x: results.map(r => r.paramValue),
            y: results.map(r => r.result),
            type: 'scatter',
            mode: 'lines+markers',
            name: '结果值',
            line: { color: '#1f77b4', width: 3 },
            marker: { size: 8 }
        };
        
        const trace2 = {
            x: results.map(r => r.paramValue),
            y: results.map(r => r.sensitivity),
            type: 'scatter',
            mode: 'lines+markers',
            name: '敏感性 (%)',
            yaxis: 'y2',
            line: { color: '#ff7f0e', width: 3 },
            marker: { size: 8 }
        };
        
        const layout = {
            title: {
                text: `${paramName} 敏感性分析`,
                font: { size: 16, family: 'Arial, sans-serif' }
            },
            xaxis: {
                title: paramName,
                gridcolor: '#e6e6e6'
            },
            yaxis: {
                title: '结果值',
                side: 'left',
                gridcolor: '#e6e6e6'
            },
            yaxis2: {
                title: '敏感性 (%)',
                side: 'right',
                overlaying: 'y',
                gridcolor: '#f0f0f0'
            },
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.8)'
            },
            margin: { l: 60, r: 60, t: 60, b: 60 },
            plot_bgcolor: '#fafafa'
        };
        
        Plotly.newPlot(containerId, [trace1, trace2], layout, {
            responsive: true,
            displayModeBar: true
        });
        
        this.charts.set(paramName, containerId);
    }

    /**
     * 创建参数交互热力图
     */
    createInteractionHeatmap(param1, param2, containerId) {
        const results = this.results.get(`${param1}_${param2}_interaction`);
        if (!results) {
            console.error(`未找到 ${param1} 与 ${param2} 的交互分析结果`);
            return;
        }
        
        // 准备热力图数据
        const param1Values = [...new Set(results.map(r => r[param1]))].sort((a, b) => a - b);
        const param2Values = [...new Set(results.map(r => r[param2]))].sort((a, b) => a - b);
        
        const zData = [];
        for (let i = 0; i < param2Values.length; i++) {
            const row = [];
            for (let j = 0; j < param1Values.length; j++) {
                const result = results.find(r => 
                    r[param1] === param1Values[j] && r[param2] === param2Values[i]
                );
                row.push(result ? result.result : null);
            }
            zData.push(row);
        }
        
        const trace = {
            z: zData,
            x: param1Values,
            y: param2Values,
            type: 'heatmap',
            colorscale: 'Viridis',
            showscale: true,
            colorbar: {
                title: '结果值',
                titleside: 'right'
            }
        };
        
        const layout = {
            title: {
                text: `${param1} vs ${param2} 交互效应热力图`,
                font: { size: 16, family: 'Arial, sans-serif' }
            },
            xaxis: {
                title: param1,
                side: 'bottom'
            },
            yaxis: {
                title: param2,
                side: 'left'
            },
            margin: { l: 80, r: 80, t: 80, b: 80 }
        };
        
        Plotly.newPlot(containerId, [trace], layout, {
            responsive: true,
            displayModeBar: true
        });
        
        this.charts.set(`${param1}_${param2}_heatmap`, containerId);
    }

    /**
     * 创建多参数优化结果图
     */
    createOptimizationChart(containerId, topN = 20) {
        const results = this.results.get('multiParam');
        if (!results) {
            console.error('未找到多参数分析结果');
            return;
        }
        
        // 取前N个最优结果
        const sortedResults = [...results].sort((a, b) => b.result - a.result);
        const topResults = sortedResults.slice(0, topN);
        
        const trace = {
            x: topResults.map((_, index) => index + 1),
            y: topResults.map(r => r.result),
            type: 'bar',
            marker: {
                color: topResults.map(r => r.result),
                colorscale: 'Viridis',
                showscale: true,
                colorbar: {
                    title: '结果值',
                    titleside: 'right'
                }
            },
            text: topResults.map(r => {
                const paramStr = Object.entries(r.params)
                    .map(([key, value]) => `${key}:${value}`)
                    .join('<br>');
                return paramStr;
            }),
            textposition: 'none',
            hovertemplate: '<b>排名:</b> %{x}<br>' +
                          '<b>结果:</b> %{y:.6f}<br>' +
                          '<b>参数:</b><br>%{text}<br>' +
                          '<extra></extra>'
        };
        
        const layout = {
            title: {
                text: `前${topN}个最优参数组合`,
                font: { size: 16, family: 'Arial, sans-serif' }
            },
            xaxis: {
                title: '排名',
                gridcolor: '#e6e6e6'
            },
            yaxis: {
                title: '结果值',
                gridcolor: '#e6e6e6'
            },
            margin: { l: 60, r: 60, t: 60, b: 60 },
            plot_bgcolor: '#fafafa'
        };
        
        Plotly.newPlot(containerId, [trace], layout, {
            responsive: true,
            displayModeBar: true
        });
        
        this.charts.set('optimization', containerId);
    }

    /**
     * 生成敏感性分析报告
     */
    generateReport() {
        console.log('\n' + '='.repeat(50));
        console.log('           敏感性分析报告');
        console.log('='.repeat(50));
        
        this.results.forEach((results, key) => {
            if (key === 'multiParam') {
                this.generateMultiParamReport(results);
            } else if (key.includes('_interaction')) {
                this.generateInteractionReport(results, key);
            } else {
                this.generateSingleParamReport(results, key);
            }
        });
    }

    generateSingleParamReport(results, paramName) {
        console.log(`\n📊 ${paramName} 单参数分析:`);
        
        // 找出最敏感的参数值
        const maxSensitivity = Math.max(...results.map(r => Math.abs(r.sensitivity)));
        const mostSensitive = results.find(r => Math.abs(r.sensitivity) === maxSensitivity);
        
        console.log(`  最大敏感性: ${maxSensitivity.toFixed(2)}% (参数值: ${mostSensitive.paramValue})`);
        
        // 计算敏感性统计
        const sensitivities = results.map(r => Math.abs(r.sensitivity));
        const avgSensitivity = sensitivities.reduce((a, b) => a + b) / sensitivities.length;
        const stdSensitivity = Math.sqrt(
            sensitivities.reduce((acc, s) => acc + Math.pow(s - avgSensitivity, 2), 0) / sensitivities.length
        );
        
        console.log(`  平均敏感性: ${avgSensitivity.toFixed(2)}%`);
        console.log(`  敏感性标准差: ${stdSensitivity.toFixed(2)}%`);
        
        // 敏感性等级
        let sensitivityLevel;
        if (maxSensitivity < 5) sensitivityLevel = '低敏感性';
        else if (maxSensitivity < 20) sensitivityLevel = '中等敏感性';
        else sensitivityLevel = '高敏感性';
        
        console.log(`  敏感性等级: ${sensitivityLevel}`);
    }

    generateMultiParamReport(results) {
        console.log('\n🎯 多参数优化分析:');
        
        const sortedResults = [...results].sort((a, b) => b.result - a.result);
        const best = sortedResults[0];
        const worst = sortedResults[sortedResults.length - 1];
        const median = sortedResults[Math.floor(sortedResults.length / 2)];
        
        console.log(`  最优结果: ${best.result.toFixed(6)}`);
        console.log(`  最差结果: ${worst.result.toFixed(6)}`);
        console.log(`  中位数结果: ${median.result.toFixed(6)}`);
        console.log(`  结果范围: ${(best.result - worst.result).toFixed(6)}`);
        console.log(`  改进潜力: ${(((best.result - worst.result) / worst.result) * 100).toFixed(2)}%`);
    }

    generateInteractionReport(results, key) {
        const [param1, param2] = key.split('_').slice(0, 2);
        console.log(`\n🔄 ${param1} × ${param2} 交互分析:`);
        
        const interactionEffect = this.calculateInteractionEffect(results, param1, param2);
        console.log(`  交互效应强度: ${interactionEffect.toFixed(6)}`);
        
        if (Math.abs(interactionEffect) > 0.1) {
            console.log(`  ⚠️ 强交互效应 - 需要同时优化这两个参数`);
        } else {
            console.log(`  ✅ 弱交互效应 - 可以独立优化参数`);
        }
    }

    /**
     * 导出分析结果
     */
    exportResults(format = 'json') {
        const exportData = {
            timestamp: new Date().toISOString(),
            results: Object.fromEntries(this.results),
            summary: this.generateSummary()
        };
        
        if (format === 'json') {
            return JSON.stringify(exportData, null, 2);
        } else if (format === 'csv') {
            return this.convertToCSV(exportData);
        }
        
        return exportData;
    }

    generateSummary() {
        const summary = {
            totalAnalyses: this.results.size,
            parameters: [],
            recommendations: []
        };
        
        this.results.forEach((results, key) => {
            if (!key.includes('_interaction') && key !== 'multiParam') {
                const sensitivities = results.map(r => Math.abs(r.sensitivity));
                const maxSensitivity = Math.max(...sensitivities);
                
                summary.parameters.push({
                    name: key,
                    maxSensitivity: maxSensitivity,
                    level: maxSensitivity < 5 ? 'low' : maxSensitivity < 20 ? 'medium' : 'high'
                });
                
                if (maxSensitivity > 20) {
                    summary.recommendations.push(`${key} 参数高度敏感，需要精确调优`);
                } else if (maxSensitivity < 5) {
                    summary.recommendations.push(`${key} 参数敏感性较低，可以使用默认值`);
                }
            }
        });
        
        return summary;
    }

    convertToCSV(data) {
        // 简化的CSV转换
        let csv = 'Parameter,Value,Result,Sensitivity\n';
        
        Object.entries(data.results).forEach(([paramName, results]) => {
            if (Array.isArray(results) && results[0] && 'paramValue' in results[0]) {
                results.forEach(result => {
                    csv += `${paramName},${result.paramValue},${result.result},${result.sensitivity}\n`;
                });
            }
        });
        
        return csv;
    }
}

// 金融算法参数敏感性测试套件
class FinancialParameterSensitivity {
    constructor() {
        this.analyzer = new ParameterSensitivityAnalyzer();
    }

    /**
     * 移动平均线参数敏感性测试
     */
    testMovingAverageParameters(priceData) {
        console.log('\n📈 移动平均线参数敏感性测试');
        
        const algorithm = (data, params) => {
            return this.calculateSMA(data, params.period);
        };
        
        const evaluator = (smaValues) => {
            // 评估指标：信号质量（减少噪音程度）
            if (smaValues.length < 2) return 0;
            
            let smoothness = 0;
            for (let i = 1; i < smaValues.length; i++) {
                smoothness += Math.abs(smaValues[i] - smaValues[i-1]);
            }
            return 1 / (smoothness / smaValues.length); // 平滑度越高，值越大
        };
        
        const baseParams = { period: 20 };
        const periodValues = [5, 10, 15, 20, 25, 30, 40, 50, 60];
        
        return this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'period', periodValues, priceData, evaluator
        );
    }

    /**
     * RSI参数敏感性测试
     */
    testRSIParameters(priceData) {
        console.log('\n📊 RSI参数敏感性测试');
        
        const algorithm = (data, params) => {
            return this.calculateRSI(data, params.period);
        };
        
        const evaluator = (rsiValues) => {
            // 评估指标：信号有效性（超买超卖信号的准确性）
            let validSignals = 0;
            let totalSignals = 0;
            
            for (let i = 1; i < rsiValues.length; i++) {
                if (rsiValues[i-1] > 70 && rsiValues[i] <= 70) {
                    totalSignals++;
                    // 简化：假设卖出信号后价格下跌为有效
                    if (Math.random() > 0.4) validSignals++; // 模拟60%准确率
                }
                if (rsiValues[i-1] < 30 && rsiValues[i] >= 30) {
                    totalSignals++;
                    if (Math.random() > 0.4) validSignals++;
                }
            }
            
            return totalSignals > 0 ? validSignals / totalSignals : 0;
        };
        
        const baseParams = { period: 14 };
        const periodValues = [7, 9, 11, 14, 17, 21, 25, 30];
        
        return this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'period', periodValues, priceData, evaluator
        );
    }

    /**
     * 布林带参数敏感性测试
     */
    testBollingerBandsParameters(priceData) {
        console.log('\n📏 布林带参数敏感性测试');
        
        const algorithm = (data, params) => {
            return this.calculateBollingerBands(data, params.period, params.stdDev);
        };
        
        const evaluator = (bands) => {
            // 评估指标：带宽适中性（不能太宽也不能太窄）
            if (!bands.upperBand || bands.upperBand.length === 0) return 0;
            
            let avgBandwidth = 0;
            for (let i = 0; i < bands.upperBand.length; i++) {
                const bandwidth = (bands.upperBand[i] - bands.lowerBand[i]) / bands.sma[i];
                avgBandwidth += bandwidth;
            }
            avgBandwidth /= bands.upperBand.length;
            
            // 理想带宽在0.1-0.3之间
            const ideal = 0.2;
            return 1 / (1 + Math.abs(avgBandwidth - ideal));
        };
        
        const baseParams = { period: 20, stdDev: 2 };
        
        // 测试周期参数
        const periodValues = [10, 15, 20, 25, 30];
        const periodResults = this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'period', periodValues, priceData, evaluator
        );
        
        // 测试标准差参数
        const stdDevValues = [1.5, 1.8, 2.0, 2.2, 2.5, 3.0];
        const stdDevResults = this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'stdDev', stdDevValues, priceData, evaluator
        );
        
        // 测试参数交互效应
        const interactionResults = this.analyzer.analyzeParameterInteraction(
            algorithm, baseParams, 'period', 'stdDev', 
            [15, 20, 25], [1.5, 2.0, 2.5], priceData, evaluator
        );
        
        return { periodResults, stdDevResults, interactionResults };
    }

    /**
     * 投资组合优化参数敏感性测试
     */
    testPortfolioOptimizationParameters(returnsData) {
        console.log('\n💼 投资组合优化参数敏感性测试');
        
        const algorithm = (data, params) => {
            return this.optimizePortfolio(data, params.riskAversion, params.lookbackPeriod);
        };
        
        const evaluator = (portfolio) => {
            // 评估指标：夏普比率
            if (!portfolio.expectedReturn || !portfolio.volatility) return 0;
            const riskFreeRate = 0.02; // 2%无风险利率
            return (portfolio.expectedReturn - riskFreeRate) / portfolio.volatility;
        };
        
        const baseParams = { riskAversion: 3, lookbackPeriod: 252 };
        
        // 测试风险厌恶参数
        const riskAversionValues = [1, 2, 3, 4, 5, 7, 10];
        const riskResults = this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'riskAversion', riskAversionValues, returnsData, evaluator
        );
        
        // 测试回望期参数
        const lookbackValues = [63, 126, 189, 252, 378, 504]; // 3个月到2年
        const lookbackResults = this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'lookbackPeriod', lookbackValues, returnsData, evaluator
        );
        
        return { riskResults, lookbackResults };
    }

    /**
     * VaR模型参数敏感性测试
     */
    testVaRParameters(returnsData) {
        console.log('\n⚠️ VaR模型参数敏感性测试');
        
        const algorithm = (data, params) => {
            return this.calculateVaR(data, params.confidence, params.holdingPeriod);
        };
        
        const evaluator = (var95) => {
            // 评估指标：VaR的稳定性（负值，绝对值越小越好）
            return -Math.abs(var95);
        };
        
        const baseParams = { confidence: 0.05, holdingPeriod: 1 };
        
        // 测试置信水平
        const confidenceValues = [0.01, 0.025, 0.05, 0.075, 0.1];
        const confidenceResults = this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'confidence', confidenceValues, returnsData, evaluator
        );
        
        // 测试持有期
        const holdingPeriodValues = [1, 5, 10, 20, 30];
        const holdingResults = this.analyzer.analyzeSingleParameter(
            algorithm, baseParams, 'holdingPeriod', holdingPeriodValues, returnsData, evaluator
        );
        
        return { confidenceResults, holdingResults };
    }

    /**
     * GARCH模型参数敏感性测试
     */
    testGARCHParameters(returnsData) {
        console.log('\n📈 GARCH模型参数敏感性测试');
        
        const algorithm = (data, params) => {
            return this.fitGARCH(data, params.p, params.q);
        };
        
        const evaluator = (garchResult) => {
            // 评估指标：模型拟合优度（AIC或BIC）
            return garchResult.logLikelihood - garchResult.numParams; // 简化的AIC
        };
        
        const baseParams = { p: 1, q: 1 };
        
        // 测试不同的GARCH(p,q)组合
        const paramRanges = {
            p: [1, 2, 3],
            q: [1, 2, 3]
        };
        
        return this.analyzer.analyzeMultipleParameters(
            algorithm, baseParams, paramRanges, returnsData, evaluator
        );
    }

    // ==================== 算法实现 ====================

    calculateSMA(data, period) {
        const result = [];
        for (let i = period - 1; i < data.length; i++) {
            const sum = data.slice(i - period + 1, i + 1)
                .reduce((acc, item) => acc + item.close, 0);
            result.push(sum / period);
        }
        return result;
    }

    calculateRSI(data, period) {
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
                const rs = avgGain / (avgLoss || 0.0001);
                rsi.push(100 - (100 / (1 + rs)));
            }
        }
        
        return rsi;
    }

    calculateBollingerBands(data, period, stdDev) {
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

    optimizePortfolio(returnsData, riskAversion, lookbackPeriod) {
        // 简化的投资组合优化
        const recentReturns = returnsData.slice(-lookbackPeriod);
        const numAssets = recentReturns[0].length;
        
        // 计算期望收益和协方差矩阵
        const expectedReturns = Array(numAssets).fill(0);
        for (let i = 0; i < recentReturns.length; i++) {
            for (let j = 0; j < numAssets; j++) {
                expectedReturns[j] += recentReturns[i][j];
            }
        }
        expectedReturns.forEach((ret, i) => {
            expectedReturns[i] = ret / recentReturns.length;
        });
        
        // 简化的权重分配（基于风险厌恶调整）
        const weights = expectedReturns.map(ret => Math.max(0, ret / riskAversion));
        const sum = weights.reduce((a, b) => a + b) || 1;
        const normalizedWeights = weights.map(w => w / sum);
        
        // 计算组合期望收益和波动率
        const portfolioReturn = normalizedWeights.reduce((acc, w, i) => acc + w * expectedReturns[i], 0);
        const portfolioVolatility = Math.sqrt(normalizedWeights.reduce((acc, w) => acc + w * w * 0.01, 0)); // 简化
        
        return {
            weights: normalizedWeights,
            expectedReturn: portfolioReturn,
            volatility: portfolioVolatility
        };
    }

    calculateVaR(returnsData, confidence, holdingPeriod) {
        // 历史模拟法VaR
        const sortedReturns = [...returnsData].sort((a, b) => a - b);
        const index = Math.floor(confidence * sortedReturns.length);
        const dailyVaR = sortedReturns[index];
        
        // 调整持有期
        return dailyVaR * Math.sqrt(holdingPeriod);
    }

    fitGARCH(returnsData, p, q) {
        // 简化的GARCH模型拟合
        const n = returnsData.length;
        const mean = returnsData.reduce((a, b) => a + b) / n;
        const residuals = returnsData.map(r => r - mean);
        
        // 简化的参数估计
        let logLikelihood = 0;
        let variance = 0.01; // 初始方差
        
        for (let i = Math.max(p, q); i < n; i++) {
            // GARCH(1,1)简化版本
            const alpha0 = 0.0001;
            const alpha1 = 0.1;
            const beta1 = 0.8;
            
            variance = alpha0 + alpha1 * Math.pow(residuals[i-1], 2) + beta1 * variance;
            logLikelihood -= 0.5 * (Math.log(2 * Math.PI * variance) + Math.pow(residuals[i], 2) / variance);
        }
        
        return {
            logLikelihood: logLikelihood,
            numParams: p + q + 1,
            variance: variance
        };
    }
}

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ParameterSensitivityAnalyzer,
        FinancialParameterSensitivity
    };
}

// 全局可用
window.ParameterSensitivity = {
    ParameterSensitivityAnalyzer,
    FinancialParameterSensitivity
};