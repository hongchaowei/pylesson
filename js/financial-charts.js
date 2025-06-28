// 交互式金融图表库 - 基于D3.js和Plotly

/**
 * K线图组件
 */
class CandlestickChart {
    constructor(containerId, options = {}) {
        this.container = d3.select(`#${containerId}`);
        this.options = {
            width: 800,
            height: 400,
            margin: { top: 20, right: 50, bottom: 50, left: 50 },
            ...options
        };
        this.data = [];
        this.init();
    }

    init() {
        this.svg = this.container.append('svg')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        this.g = this.svg.append('g')
            .attr('transform', `translate(${this.options.margin.left},${this.options.margin.top})`);

        this.width = this.options.width - this.options.margin.left - this.options.margin.right;
        this.height = this.options.height - this.options.margin.top - this.options.margin.bottom;

        // 创建比例尺
        this.xScale = d3.scaleTime().range([0, this.width]);
        this.yScale = d3.scaleLinear().range([this.height, 0]);

        // 创建坐标轴
        this.xAxis = d3.axisBottom(this.xScale).tickFormat(d3.timeFormat('%m/%d'));
        this.yAxis = d3.axisLeft(this.yScale).tickFormat(d3.format('.2f'));

        this.g.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${this.height})`);

        this.g.append('g')
            .attr('class', 'y-axis');

        // 添加网格线
        this.addGridlines();

        // 添加工具提示
        this.tooltip = d3.select('body').append('div')
            .attr('class', 'tooltip')
            .style('opacity', 0)
            .style('position', 'absolute')
            .style('background', 'rgba(0,0,0,0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('font-size', '12px');
    }

    addGridlines() {
        // 水平网格线
        this.g.append('g')
            .attr('class', 'grid')
            .attr('transform', `translate(0,${this.height})`)
            .style('stroke-dasharray', '3,3')
            .style('opacity', 0.3);

        // 垂直网格线
        this.g.append('g')
            .attr('class', 'grid')
            .style('stroke-dasharray', '3,3')
            .style('opacity', 0.3);
    }

    updateData(data) {
        this.data = data.map(d => ({
            date: new Date(d.date),
            open: +d.open,
            high: +d.high,
            low: +d.low,
            close: +d.close,
            volume: +d.volume
        }));

        // 更新比例尺域
        this.xScale.domain(d3.extent(this.data, d => d.date));
        this.yScale.domain(d3.extent(this.data, d => Math.max(d.high, d.low)));

        // 更新坐标轴
        this.g.select('.x-axis').call(this.xAxis);
        this.g.select('.y-axis').call(this.yAxis);

        // 更新网格线
        this.updateGridlines();

        // 绘制K线
        this.drawCandles();

        // 添加移动平均线
        this.drawMovingAverages();
    }

    updateGridlines() {
        this.g.select('.grid')
            .call(d3.axisBottom(this.xScale)
                .tickSize(-this.height)
                .tickFormat('')
            );

        this.g.selectAll('.grid').selectAll('line')
            .style('stroke', '#e0e0e0')
            .style('stroke-width', 1);
    }

    drawCandles() {
        const candleWidth = this.width / this.data.length * 0.8;

        // 绑定数据
        const candles = this.g.selectAll('.candle')
            .data(this.data);

        // 移除旧元素
        candles.exit().remove();

        // 创建新的蜡烛组
        const candleEnter = candles.enter().append('g')
            .attr('class', 'candle');

        // 添加影线
        candleEnter.append('line')
            .attr('class', 'wick');

        // 添加实体
        candleEnter.append('rect')
            .attr('class', 'body');

        // 合并新旧元素
        const candleMerge = candleEnter.merge(candles);

        // 更新影线
        candleMerge.select('.wick')
            .attr('x1', d => this.xScale(d.date))
            .attr('x2', d => this.xScale(d.date))
            .attr('y1', d => this.yScale(d.high))
            .attr('y2', d => this.yScale(d.low))
            .style('stroke', d => d.close >= d.open ? '#26a69a' : '#ef5350')
            .style('stroke-width', 1);

        // 更新实体
        candleMerge.select('.body')
            .attr('x', d => this.xScale(d.date) - candleWidth / 2)
            .attr('y', d => this.yScale(Math.max(d.open, d.close)))
            .attr('width', candleWidth)
            .attr('height', d => Math.abs(this.yScale(d.open) - this.yScale(d.close)) || 1)
            .style('fill', d => d.close >= d.open ? '#26a69a' : '#ef5350')
            .style('stroke', d => d.close >= d.open ? '#26a69a' : '#ef5350');

        // 添加交互
        candleMerge
            .on('mouseover', (event, d) => {
                this.tooltip.transition().duration(200).style('opacity', .9);
                this.tooltip.html(`
                    <strong>日期:</strong> ${d3.timeFormat('%Y-%m-%d')(d.date)}<br/>
                    <strong>开盘:</strong> ${d.open.toFixed(2)}<br/>
                    <strong>最高:</strong> ${d.high.toFixed(2)}<br/>
                    <strong>最低:</strong> ${d.low.toFixed(2)}<br/>
                    <strong>收盘:</strong> ${d.close.toFixed(2)}<br/>
                    <strong>成交量:</strong> ${d.volume.toLocaleString()}
                `)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
            })
            .on('mouseout', () => {
                this.tooltip.transition().duration(500).style('opacity', 0);
            });
    }

    drawMovingAverages() {
        // 计算移动平均线
        const ma5 = this.calculateMA(this.data, 5);
        const ma20 = this.calculateMA(this.data, 20);

        // 创建线条生成器
        const line = d3.line()
            .x(d => this.xScale(d.date))
            .y(d => this.yScale(d.value))
            .curve(d3.curveMonotoneX);

        // 绘制MA5
        this.g.selectAll('.ma5-line').remove();
        this.g.append('path')
            .datum(ma5)
            .attr('class', 'ma5-line')
            .attr('d', line)
            .style('fill', 'none')
            .style('stroke', '#ff9800')
            .style('stroke-width', 2);

        // 绘制MA20
        this.g.selectAll('.ma20-line').remove();
        this.g.append('path')
            .datum(ma20)
            .attr('class', 'ma20-line')
            .attr('d', line)
            .style('fill', 'none')
            .style('stroke', '#9c27b0')
            .style('stroke-width', 2);
    }

    calculateMA(data, period) {
        const result = [];
        for (let i = period - 1; i < data.length; i++) {
            const sum = data.slice(i - period + 1, i + 1)
                .reduce((acc, d) => acc + d.close, 0);
            result.push({
                date: data[i].date,
                value: sum / period
            });
        }
        return result;
    }
}

/**
 * 成交量图组件
 */
class VolumeChart {
    constructor(containerId, options = {}) {
        this.container = d3.select(`#${containerId}`);
        this.options = {
            width: 800,
            height: 150,
            margin: { top: 10, right: 50, bottom: 30, left: 50 },
            ...options
        };
        this.init();
    }

    init() {
        this.svg = this.container.append('svg')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        this.g = this.svg.append('g')
            .attr('transform', `translate(${this.options.margin.left},${this.options.margin.top})`);

        this.width = this.options.width - this.options.margin.left - this.options.margin.right;
        this.height = this.options.height - this.options.margin.top - this.options.margin.bottom;

        this.xScale = d3.scaleTime().range([0, this.width]);
        this.yScale = d3.scaleLinear().range([this.height, 0]);

        this.xAxis = d3.axisBottom(this.xScale).tickFormat(d3.timeFormat('%m/%d'));
        this.yAxis = d3.axisLeft(this.yScale).tickFormat(d3.format('.2s'));

        this.g.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${this.height})`);

        this.g.append('g')
            .attr('class', 'y-axis');
    }

    updateData(data) {
        this.data = data.map(d => ({
            date: new Date(d.date),
            volume: +d.volume,
            close: +d.close,
            open: +d.open
        }));

        this.xScale.domain(d3.extent(this.data, d => d.date));
        this.yScale.domain([0, d3.max(this.data, d => d.volume)]);

        this.g.select('.x-axis').call(this.xAxis);
        this.g.select('.y-axis').call(this.yAxis);

        this.drawVolumeBars();
    }

    drawVolumeBars() {
        const barWidth = this.width / this.data.length * 0.8;

        const bars = this.g.selectAll('.volume-bar')
            .data(this.data);

        bars.exit().remove();

        bars.enter().append('rect')
            .attr('class', 'volume-bar')
            .merge(bars)
            .attr('x', d => this.xScale(d.date) - barWidth / 2)
            .attr('y', d => this.yScale(d.volume))
            .attr('width', barWidth)
            .attr('height', d => this.height - this.yScale(d.volume))
            .style('fill', d => d.close >= d.open ? '#26a69a' : '#ef5350')
            .style('opacity', 0.7);
    }
}

/**
 * 技术指标图表组件
 */
class TechnicalIndicatorChart {
    constructor(containerId, options = {}) {
        this.container = d3.select(`#${containerId}`);
        this.options = {
            width: 800,
            height: 200,
            margin: { top: 20, right: 50, bottom: 30, left: 50 },
            indicator: 'RSI', // RSI, MACD, KDJ
            ...options
        };
        this.init();
    }

    init() {
        this.svg = this.container.append('svg')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        this.g = this.svg.append('g')
            .attr('transform', `translate(${this.options.margin.left},${this.options.margin.top})`);

        this.width = this.options.width - this.options.margin.left - this.options.margin.right;
        this.height = this.options.height - this.options.margin.top - this.options.margin.bottom;

        this.xScale = d3.scaleTime().range([0, this.width]);
        this.yScale = d3.scaleLinear().range([this.height, 0]);

        this.xAxis = d3.axisBottom(this.xScale).tickFormat(d3.timeFormat('%m/%d'));
        this.yAxis = d3.axisLeft(this.yScale);

        this.g.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${this.height})`);

        this.g.append('g')
            .attr('class', 'y-axis');
    }

    updateData(data) {
        this.data = data.map(d => ({
            date: new Date(d.date),
            close: +d.close,
            high: +d.high,
            low: +d.low
        }));

        this.xScale.domain(d3.extent(this.data, d => d.date));

        switch (this.options.indicator) {
            case 'RSI':
                this.drawRSI();
                break;
            case 'MACD':
                this.drawMACD();
                break;
            case 'KDJ':
                this.drawKDJ();
                break;
        }
    }

    drawRSI() {
        const rsiData = this.calculateRSI(this.data, 14);
        this.yScale.domain([0, 100]);

        this.g.select('.x-axis').call(this.xAxis);
        this.g.select('.y-axis').call(this.yAxis);

        // 添加超买超卖线
        this.g.selectAll('.reference-line').remove();
        [30, 70].forEach(level => {
            this.g.append('line')
                .attr('class', 'reference-line')
                .attr('x1', 0)
                .attr('x2', this.width)
                .attr('y1', this.yScale(level))
                .attr('y2', this.yScale(level))
                .style('stroke', '#ff9800')
                .style('stroke-dasharray', '5,5')
                .style('opacity', 0.7);
        });

        // 绘制RSI线
        const line = d3.line()
            .x(d => this.xScale(d.date))
            .y(d => this.yScale(d.rsi))
            .curve(d3.curveMonotoneX);

        this.g.selectAll('.rsi-line').remove();
        this.g.append('path')
            .datum(rsiData)
            .attr('class', 'rsi-line')
            .attr('d', line)
            .style('fill', 'none')
            .style('stroke', '#2196f3')
            .style('stroke-width', 2);
    }

    calculateRSI(data, period = 14) {
        const result = [];
        const gains = [];
        const losses = [];

        for (let i = 1; i < data.length; i++) {
            const change = data[i].close - data[i - 1].close;
            gains.push(change > 0 ? change : 0);
            losses.push(change < 0 ? Math.abs(change) : 0);

            if (i >= period) {
                const avgGain = gains.slice(-period).reduce((a, b) => a + b) / period;
                const avgLoss = losses.slice(-period).reduce((a, b) => a + b) / period;
                const rs = avgGain / avgLoss;
                const rsi = 100 - (100 / (1 + rs));

                result.push({
                    date: data[i].date,
                    rsi: rsi
                });
            }
        }

        return result;
    }

    drawMACD() {
        const macdData = this.calculateMACD(this.data);
        const values = macdData.map(d => [d.macd, d.signal, d.histogram]).flat();
        this.yScale.domain(d3.extent(values));

        this.g.select('.x-axis').call(this.xAxis);
        this.g.select('.y-axis').call(this.yAxis);

        // 绘制零轴线
        this.g.selectAll('.zero-line').remove();
        this.g.append('line')
            .attr('class', 'zero-line')
            .attr('x1', 0)
            .attr('x2', this.width)
            .attr('y1', this.yScale(0))
            .attr('y2', this.yScale(0))
            .style('stroke', '#666')
            .style('stroke-width', 1);

        // 绘制MACD线
        const line = d3.line()
            .x(d => this.xScale(d.date))
            .curve(d3.curveMonotoneX);

        this.g.selectAll('.macd-line').remove();
        this.g.append('path')
            .datum(macdData)
            .attr('class', 'macd-line')
            .attr('d', line.y(d => this.yScale(d.macd)))
            .style('fill', 'none')
            .style('stroke', '#2196f3')
            .style('stroke-width', 2);

        // 绘制信号线
        this.g.selectAll('.signal-line').remove();
        this.g.append('path')
            .datum(macdData)
            .attr('class', 'signal-line')
            .attr('d', line.y(d => this.yScale(d.signal)))
            .style('fill', 'none')
            .style('stroke', '#ff9800')
            .style('stroke-width', 2);

        // 绘制柱状图
        const barWidth = this.width / macdData.length * 0.6;
        this.g.selectAll('.histogram-bar').remove();
        this.g.selectAll('.histogram-bar')
            .data(macdData)
            .enter().append('rect')
            .attr('class', 'histogram-bar')
            .attr('x', d => this.xScale(d.date) - barWidth / 2)
            .attr('y', d => d.histogram >= 0 ? this.yScale(d.histogram) : this.yScale(0))
            .attr('width', barWidth)
            .attr('height', d => Math.abs(this.yScale(d.histogram) - this.yScale(0)))
            .style('fill', d => d.histogram >= 0 ? '#26a69a' : '#ef5350')
            .style('opacity', 0.7);
    }

    calculateMACD(data, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) {
        const ema12 = this.calculateEMA(data, fastPeriod);
        const ema26 = this.calculateEMA(data, slowPeriod);
        const macdLine = [];

        // 计算MACD线
        for (let i = slowPeriod - 1; i < data.length; i++) {
            macdLine.push({
                date: data[i].date,
                macd: ema12[i - (slowPeriod - fastPeriod)] - ema26[i - (slowPeriod - 1)]
            });
        }

        // 计算信号线
        const signalLine = this.calculateEMAFromValues(macdLine.map(d => d.macd), signalPeriod);

        // 组合结果
        const result = [];
        for (let i = signalPeriod - 1; i < macdLine.length; i++) {
            const macd = macdLine[i].macd;
            const signal = signalLine[i - (signalPeriod - 1)];
            result.push({
                date: macdLine[i].date,
                macd: macd,
                signal: signal,
                histogram: macd - signal
            });
        }

        return result;
    }

    calculateEMA(data, period) {
        const multiplier = 2 / (period + 1);
        const ema = [data[0].close];

        for (let i = 1; i < data.length; i++) {
            ema.push((data[i].close * multiplier) + (ema[i - 1] * (1 - multiplier)));
        }

        return ema;
    }

    calculateEMAFromValues(values, period) {
        const multiplier = 2 / (period + 1);
        const ema = [values[0]];

        for (let i = 1; i < values.length; i++) {
            ema.push((values[i] * multiplier) + (ema[i - 1] * (1 - multiplier)));
        }

        return ema;
    }
}

/**
 * 投资组合饼图组件
 */
class PortfolioPieChart {
    constructor(containerId, options = {}) {
        this.container = d3.select(`#${containerId}`);
        this.options = {
            width: 400,
            height: 400,
            margin: 40,
            ...options
        };
        this.init();
    }

    init() {
        this.svg = this.container.append('svg')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        this.radius = Math.min(this.options.width, this.options.height) / 2 - this.options.margin;

        this.g = this.svg.append('g')
            .attr('transform', `translate(${this.options.width / 2},${this.options.height / 2})`);

        this.color = d3.scaleOrdinal(d3.schemeCategory10);

        this.pie = d3.pie()
            .value(d => d.value)
            .sort(null);

        this.arc = d3.arc()
            .innerRadius(0)
            .outerRadius(this.radius);

        this.labelArc = d3.arc()
            .innerRadius(this.radius * 0.8)
            .outerRadius(this.radius * 0.8);

        // 添加工具提示
        this.tooltip = d3.select('body').append('div')
            .attr('class', 'pie-tooltip')
            .style('opacity', 0)
            .style('position', 'absolute')
            .style('background', 'rgba(0,0,0,0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('font-size', '12px');
    }

    updateData(data) {
        this.data = data;

        const arcs = this.g.selectAll('.arc')
            .data(this.pie(data));

        arcs.exit().remove();

        const arcEnter = arcs.enter().append('g')
            .attr('class', 'arc');

        arcEnter.append('path');
        arcEnter.append('text');

        const arcMerge = arcEnter.merge(arcs);

        // 更新路径
        arcMerge.select('path')
            .attr('d', this.arc)
            .style('fill', (d, i) => this.color(i))
            .style('stroke', 'white')
            .style('stroke-width', 2)
            .on('mouseover', (event, d) => {
                this.tooltip.transition().duration(200).style('opacity', .9);
                this.tooltip.html(`
                    <strong>${d.data.name}</strong><br/>
                    数量: ${d.data.value.toLocaleString()}<br/>
                    占比: ${((d.endAngle - d.startAngle) / (2 * Math.PI) * 100).toFixed(1)}%
                `)
                    .style('left', (event.pageX + 10) + 'px')
                    .style('top', (event.pageY - 28) + 'px');
            })
            .on('mouseout', () => {
                this.tooltip.transition().duration(500).style('opacity', 0);
            });

        // 更新标签
        arcMerge.select('text')
            .attr('transform', d => `translate(${this.labelArc.centroid(d)})`)
            .attr('dy', '0.35em')
            .style('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('font-weight', 'bold')
            .text(d => {
                const percent = (d.endAngle - d.startAngle) / (2 * Math.PI) * 100;
                return percent > 5 ? `${percent.toFixed(1)}%` : '';
            });
    }
}

/**
 * 相关性热力图组件
 */
class CorrelationHeatmap {
    constructor(containerId, options = {}) {
        this.container = d3.select(`#${containerId}`);
        this.options = {
            width: 500,
            height: 500,
            margin: { top: 50, right: 50, bottom: 50, left: 100 },
            ...options
        };
        this.init();
    }

    init() {
        this.svg = this.container.append('svg')
            .attr('width', this.options.width)
            .attr('height', this.options.height);

        this.g = this.svg.append('g')
            .attr('transform', `translate(${this.options.margin.left},${this.options.margin.top})`);

        this.width = this.options.width - this.options.margin.left - this.options.margin.right;
        this.height = this.options.height - this.options.margin.top - this.options.margin.bottom;

        // 颜色比例尺
        this.colorScale = d3.scaleSequential(d3.interpolateRdYlBu)
            .domain([1, -1]);

        // 添加工具提示
        this.tooltip = d3.select('body').append('div')
            .attr('class', 'heatmap-tooltip')
            .style('opacity', 0)
            .style('position', 'absolute')
            .style('background', 'rgba(0,0,0,0.8)')
            .style('color', 'white')
            .style('padding', '8px')
            .style('border-radius', '4px')
            .style('font-size', '12px');
    }

    updateData(correlationMatrix, labels) {
        this.matrix = correlationMatrix;
        this.labels = labels;
        this.size = labels.length;

        // 创建比例尺
        this.xScale = d3.scaleBand()
            .domain(d3.range(this.size))
            .range([0, this.width])
            .padding(0.1);

        this.yScale = d3.scaleBand()
            .domain(d3.range(this.size))
            .range([0, this.height])
            .padding(0.1);

        // 清除旧内容
        this.g.selectAll('*').remove();

        // 绘制热力图
        for (let i = 0; i < this.size; i++) {
            for (let j = 0; j < this.size; j++) {
                this.g.append('rect')
                    .attr('x', this.xScale(j))
                    .attr('y', this.yScale(i))
                    .attr('width', this.xScale.bandwidth())
                    .attr('height', this.yScale.bandwidth())
                    .style('fill', this.colorScale(this.matrix[i][j]))
                    .style('stroke', 'white')
                    .style('stroke-width', 1)
                    .on('mouseover', (event) => {
                        this.tooltip.transition().duration(200).style('opacity', .9);
                        this.tooltip.html(`
                            <strong>${this.labels[i]} vs ${this.labels[j]}</strong><br/>
                            相关系数: ${this.matrix[i][j].toFixed(3)}
                        `)
                            .style('left', (event.pageX + 10) + 'px')
                            .style('top', (event.pageY - 28) + 'px');
                    })
                    .on('mouseout', () => {
                        this.tooltip.transition().duration(500).style('opacity', 0);
                    });

                // 添加数值标签
                if (Math.abs(this.matrix[i][j]) > 0.1) {
                    this.g.append('text')
                        .attr('x', this.xScale(j) + this.xScale.bandwidth() / 2)
                        .attr('y', this.yScale(i) + this.yScale.bandwidth() / 2)
                        .attr('dy', '0.35em')
                        .style('text-anchor', 'middle')
                        .style('font-size', '10px')
                        .style('font-weight', 'bold')
                        .style('fill', Math.abs(this.matrix[i][j]) > 0.5 ? 'white' : 'black')
                        .text(this.matrix[i][j].toFixed(2));
                }
            }
        }

        // 添加坐标轴标签
        this.g.selectAll('.x-label')
            .data(this.labels)
            .enter().append('text')
            .attr('class', 'x-label')
            .attr('x', (d, i) => this.xScale(i) + this.xScale.bandwidth() / 2)
            .attr('y', this.height + 20)
            .style('text-anchor', 'middle')
            .style('font-size', '12px')
            .text(d => d);

        this.g.selectAll('.y-label')
            .data(this.labels)
            .enter().append('text')
            .attr('class', 'y-label')
            .attr('x', -10)
            .attr('y', (d, i) => this.yScale(i) + this.yScale.bandwidth() / 2)
            .attr('dy', '0.35em')
            .style('text-anchor', 'end')
            .style('font-size', '12px')
            .text(d => d);
    }
}

// 导出组件
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        CandlestickChart,
        VolumeChart,
        TechnicalIndicatorChart,
        PortfolioPieChart,
        CorrelationHeatmap
    };
}

// 全局可用
window.FinancialCharts = {
    CandlestickChart,
    VolumeChart,
    TechnicalIndicatorChart,
    PortfolioPieChart,
    CorrelationHeatmap
};