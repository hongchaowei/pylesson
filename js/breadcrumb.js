/**
 * 面包屑导航生成器
 * 根据当前页面路径自动生成面包屑导航
 */

// 路径映射配置
const pathMapping = {
    'index.html': { name: '首页', icon: '🏠' },
    'part1_python_basics': { name: 'Python基础', icon: '🐍' },
    'part2_data_analysis': { name: '数据分析', icon: '📊' },
    'part3_financial_modeling': { name: '金融建模', icon: '💰' },
    'part4_advanced_topics': { name: '高级主题', icon: '🚀' },
    'module1': { name: '模块1', icon: '📚' },
    'module2': { name: '模块2', icon: '📚' },
    'module3': { name: '模块3', icon: '📚' },
    'module4': { name: '模块4', icon: '📚' },
    'module5': { name: '模块5', icon: '📚' },
    'module6': { name: '模块6', icon: '📚' },
    'module7': { name: '模块7', icon: '📚' },
    'module8': { name: '模块8', icon: '📚' },
    'module9': { name: '模块9', icon: '📚' },
    'module10': { name: '模块10', icon: '📚' },
    'module11': { name: '模块11', icon: '📚' },
    'module12': { name: '模块12', icon: '📚' },
    'module13': { name: '模块13', icon: '📚' },
    'module14': { name: '模块14', icon: '📚' },
    'module15': { name: '模块15', icon: '📚' },
    'module16': { name: '模块16', icon: '📚' },
    'lesson1.html': { name: '课程1', icon: '📖' },
    'lesson2.html': { name: '课程2', icon: '📖' },
    'lesson3.html': { name: '课程3', icon: '📖' },
    'lesson4.html': { name: '课程4', icon: '📖' },
    'lesson5.html': { name: '课程5', icon: '📖' },
    'lesson6.html': { name: '课程6', icon: '📖' },
    'lesson7.html': { name: '课程7', icon: '📖' },
    'lesson8.html': { name: '课程8', icon: '📖' },
    'lesson9.html': { name: '课程9', icon: '📖' },
    'lesson10.html': { name: '课程10', icon: '📖' }
};

// 详细的课程标题映射
const lessonTitles = {
    'part1_python_basics/module1/lesson1.html': 'Python简介与环境设置',
    'part1_python_basics/module1/lesson2.html': 'Python基础语法',
    'part1_python_basics/module1/lesson3.html': '数据类型与变量',
    'part1_python_basics/module1/lesson4.html': '控制流程',
    'part1_python_basics/module2/lesson1.html': '函数定义与调用',
    'part1_python_basics/module2/lesson2.html': '模块与包',
    'part1_python_basics/module2/lesson3.html': '异常处理',
    'part1_python_basics/module2/lesson4.html': '文件操作',
    'part2_data_analysis/module3/lesson1.html': 'NumPy基础',
    'part2_data_analysis/module3/lesson2.html': 'NumPy数组操作',
    'part2_data_analysis/module3/lesson3.html': 'NumPy数学函数',
    'part2_data_analysis/module3/lesson4.html': 'NumPy线性代数',
    'part2_data_analysis/module4/lesson1.html': 'Pandas基础',
    'part2_data_analysis/module4/lesson2.html': 'Pandas数据操作',
    'part2_data_analysis/module4/lesson3.html': 'Pandas数据清洗',
    'part2_data_analysis/module4/lesson4.html': 'Pandas数据分析',
    'part2_data_analysis/module5/lesson1.html': 'Matplotlib基础',
    'part2_data_analysis/module5/lesson2.html': 'Matplotlib高级绘图',
    'part2_data_analysis/module5/lesson3.html': 'Seaborn数据可视化',
    'part2_data_analysis/module5/lesson4.html': 'Plotly交互式图表',
    'part2_data_analysis/module6/lesson1.html': '金融数据获取',
    'part2_data_analysis/module6/lesson2.html': '股票数据分析',
    'part2_data_analysis/module6/lesson3.html': '技术指标计算',
    'part2_data_analysis/module6/lesson4.html': '金融数据可视化',
    'part3_financial_modeling/module7/lesson1.html': '投资组合理论',
    'part3_financial_modeling/module7/lesson2.html': '资本资产定价模型',
    'part3_financial_modeling/module7/lesson3.html': '有效前沿',
    'part3_financial_modeling/module7/lesson4.html': '风险度量',
    'part3_financial_modeling/module8/lesson1.html': '期权定价基础',
    'part3_financial_modeling/module8/lesson2.html': 'Black-Scholes模型',
    'part3_financial_modeling/module8/lesson3.html': '二项式期权定价',
    'part3_financial_modeling/module8/lesson4.html': '期权希腊字母',
    'part3_financial_modeling/module9/lesson1.html': '固定收益证券',
    'part3_financial_modeling/module9/lesson2.html': '债券定价',
    'part3_financial_modeling/module9/lesson3.html': '久期与凸性',
    'part3_financial_modeling/module9/lesson4.html': '收益率曲线',
    'part3_financial_modeling/module10/lesson1.html': 'VaR计算',
    'part3_financial_modeling/module10/lesson2.html': '压力测试',
    'part3_financial_modeling/module10/lesson3.html': '信用风险建模',
    'part3_financial_modeling/module10/lesson4.html': '市场风险管理',
    'part4_advanced_topics/module11/lesson1.html': '回测框架',
    'part4_advanced_topics/module11/lesson2.html': '策略开发',
    'part4_advanced_topics/module11/lesson3.html': '性能评估',
    'part4_advanced_topics/module11/lesson4.html': '实盘交易',
    'part4_advanced_topics/module12/lesson1.html': '机器学习基础',
    'part4_advanced_topics/module12/lesson2.html': '特征工程',
    'part4_advanced_topics/module12/lesson3.html': '模型训练',
    'part4_advanced_topics/module12/lesson4.html': '模型评估',
    'part4_advanced_topics/module13/lesson1.html': '时间序列分析',
    'part4_advanced_topics/module13/lesson2.html': 'ARIMA模型',
    'part4_advanced_topics/module13/lesson3.html': 'GARCH模型',
    'part4_advanced_topics/module13/lesson4.html': '预测与验证',
    'part4_advanced_topics/module14/lesson1.html': 'API接口',
    'part4_advanced_topics/module14/lesson2.html': '实时数据',
    'part4_advanced_topics/module14/lesson3.html': '数据存储',
    'part4_advanced_topics/module14/lesson4.html': '系统架构',
    'part4_advanced_topics/module15/lesson1.html': '区块链基础',
    'part4_advanced_topics/module15/lesson2.html': '加密货币分析',
    'part4_advanced_topics/module15/lesson3.html': 'DeFi协议',
    'part4_advanced_topics/module15/lesson4.html': 'NFT与数字资产',
    'part4_advanced_topics/module16/lesson1.html': '项目规划',
    'part4_advanced_topics/module16/lesson2.html': '系统设计',
    'part4_advanced_topics/module16/lesson3.html': '代码实现',
    'part4_advanced_topics/module16/lesson4.html': '部署与维护'
};

/**
 * 生成面包屑导航
 */
function generateBreadcrumb() {
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/').filter(part => part !== '');
    
    // 如果是根目录，不显示面包屑
    if (pathParts.length === 0 || (pathParts.length === 1 && pathParts[0] === 'index.html')) {
        return;
    }
    
    // 创建面包屑容器
    const breadcrumbContainer = document.createElement('div');
    breadcrumbContainer.className = 'breadcrumb';
    
    const breadcrumbNav = document.createElement('div');
    breadcrumbNav.className = 'container';
    
    const breadcrumbList = document.createElement('div');
    breadcrumbList.className = 'breadcrumb-nav';
    
    // 添加首页链接
    const homeItem = createBreadcrumbItem('首页', getRelativePath('index.html'), '🏠');
    breadcrumbList.appendChild(homeItem);
    
    // 构建路径
    let currentRelativePath = '';
    const pathSegments = [];
    
    // 分析路径结构
    for (let i = 0; i < pathParts.length; i++) {
        const part = pathParts[i];
        pathSegments.push(part);
        
        if (i < pathParts.length - 1) {
            // 不是最后一个元素，添加分隔符和链接
            breadcrumbList.appendChild(createSeparator());
            
            const mapping = pathMapping[part];
            if (mapping) {
                const linkPath = getRelativePathToSegment(pathSegments.slice(0, i + 1));
                const item = createBreadcrumbItem(mapping.name, linkPath, mapping.icon);
                breadcrumbList.appendChild(item);
            }
        } else {
            // 最后一个元素，显示为当前页面
            breadcrumbList.appendChild(createSeparator());
            
            // 获取当前页面的标题
            const fullPath = pathSegments.join('/');
            const pageTitle = lessonTitles[fullPath] || getPageTitleFromMapping(part);
            
            const currentItem = createBreadcrumbItem(pageTitle, null, '📖', true);
            breadcrumbList.appendChild(currentItem);
        }
    }
    
    breadcrumbNav.appendChild(breadcrumbList);
    breadcrumbContainer.appendChild(breadcrumbNav);
    
    // 插入到页面中（在header之后）
    const header = document.querySelector('header');
    if (header && header.nextSibling) {
        header.parentNode.insertBefore(breadcrumbContainer, header.nextSibling);
    } else if (header) {
        header.parentNode.appendChild(breadcrumbContainer);
    }
}

/**
 * 创建面包屑项目
 */
function createBreadcrumbItem(text, href, icon, isActive = false) {
    const item = document.createElement('div');
    item.className = `breadcrumb-item ${isActive ? 'active' : ''}`;
    
    if (href && !isActive) {
        const link = document.createElement('a');
        link.href = href;
        link.innerHTML = `<span class="breadcrumb-icon">${icon}</span>${text}`;
        item.appendChild(link);
    } else {
        item.innerHTML = `<span class="breadcrumb-icon">${icon}</span>${text}`;
    }
    
    return item;
}

/**
 * 创建分隔符
 */
function createSeparator() {
    const separator = document.createElement('span');
    separator.className = 'breadcrumb-separator';
    separator.textContent = '>';
    return separator;
}

/**
 * 获取相对路径
 */
function getRelativePath(targetFile) {
    const currentPath = window.location.pathname;
    const currentDir = currentPath.substring(0, currentPath.lastIndexOf('/'));
    const depth = currentDir.split('/').filter(part => part !== '').length;
    
    return '../'.repeat(depth) + targetFile;
}

/**
 * 获取到指定路径段的相对路径
 */
function getRelativePathToSegment(segments) {
    const currentPath = window.location.pathname;
    const currentSegments = currentPath.split('/').filter(part => part !== '');
    const currentDepth = currentSegments.length - 1; // 减去文件名
    const targetDepth = segments.length;
    
    if (targetDepth >= currentDepth) {
        return '#'; // 无法向上导航
    }
    
    const upLevels = currentDepth - targetDepth;
    return '../'.repeat(upLevels);
}

/**
 * 从映射中获取页面标题
 */
function getPageTitleFromMapping(filename) {
    const mapping = pathMapping[filename];
    return mapping ? mapping.name : filename;
}

// 页面加载完成后生成面包屑
document.addEventListener('DOMContentLoaded', generateBreadcrumb);