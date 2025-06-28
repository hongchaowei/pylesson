/**
 * 导航栏加载和管理模块
 * 负责动态加载导航栏内容和处理导航交互
 */

// 导航栏配置
const NAV_CONFIG = {
    // 主导航菜单项
    mainNav: [
        {
            title: 'Python基础',
            path: '/part1_python_basics/index.html',
            modules: [
                { title: '模块1: Python环境与基础语法', path: '/part1_python_basics/module1/index.html' },
                { title: '模块2: 数据结构与控制流', path: '/part1_python_basics/module2/index.html' },
                { title: '模块3: 函数与面向对象', path: '/part1_python_basics/module3/index.html' },
                { title: '模块4: 文件操作与异常处理', path: '/part1_python_basics/module4/index.html' }
            ]
        },
        {
            title: '数据分析基础',
            path: '/part2_data_analysis/index.html',
            modules: [
                { title: '模块5: NumPy数值计算', path: '/part2_data_analysis/module5/index.html' },
                { title: '模块6: Pandas数据处理', path: '/part2_data_analysis/module6/index.html' },
                { title: '模块7: Matplotlib可视化', path: '/part2_data_analysis/module7/index.html' },
                { title: '模块8: 统计分析基础', path: '/part2_data_analysis/module8/index.html' }
            ]
        },
        {
            title: '金融专业应用',
            path: '/part3_finance_applications/index.html',
            modules: [
                { title: '模块9: 金融数据获取', path: '/part3_finance_applications/module9/index.html' },
                { title: '模块10: 技术分析指标', path: '/part3_finance_applications/module10/index.html' },
                { title: '模块11: 投资组合分析', path: '/part3_finance_applications/module11/index.html' },
                { title: '模块12: 风险管理', path: '/part3_finance_applications/module12/index.html' }
            ]
        },
        {
            title: '高级主题',
            path: '/part4_advanced_topics/index.html',
            modules: [
                { title: '模块13: 时间序列分析', path: '/part4_advanced_topics/module13/index.html' },
                { title: '模块14: 衍生品定价', path: '/part4_advanced_topics/module14/index.html' },
                { title: '模块15: 机器学习应用', path: '/part4_advanced_topics/module15/index.html' },
                { title: '模块16: 综合项目', path: '/part4_advanced_topics/module16/index.html' }
            ]
        },
        {
            title: '深度学习金融应用',
            path: '/deep_learning_finance.html',
            isNew: true
        },
        {
            title: '区块链金融应用',
            path: '/blockchain_finance.html',
            isNew: true
        },
        {
            title: '知识图谱',
            path: '/knowledge_graph.html',
            isNew: true
        },
        {
            title: '行业案例',
            path: '/case_studies.html',
            isNew: true
        },
        {
            title: '高级案例',
            path: '/advanced_case_studies.html',
            isNew: true
        },
        {
            title: '数据下载',
            path: '/datasets.html',
            isNew: true
        }
    ]
};

/**
 * 加载导航栏
 */
function loadNavigation() {
    const navContainer = document.querySelector('.nav-container');
    if (!navContainer) return;

    const navHTML = generateNavigationHTML();
    navContainer.innerHTML = navHTML;
    
    // 初始化导航事件
    initNavigationEvents();
    
    // 设置当前页面高亮
    highlightCurrentPage();
}

/**
 * 生成导航栏HTML
 */
function generateNavigationHTML() {
    return `
        <nav class="main-nav">
            <div class="nav-brand">
                <a href="/index.html">Python金融编程</a>
            </div>
            <div class="nav-menu">
                <ul class="nav-list">
                    ${NAV_CONFIG.mainNav.map(item => generateNavItem(item)).join('')}
                </ul>
            </div>
            <div class="nav-toggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>
    `;
}

/**
 * 生成单个导航项
 */
function generateNavItem(item) {
    const hasSubmenu = item.modules && item.modules.length > 0;
    const newBadge = item.isNew ? '<span class="new-badge">新</span>' : '';
    
    if (hasSubmenu) {
        return `
            <li class="nav-item has-submenu">
                <a href="${item.path}" class="nav-link">
                    ${item.title}${newBadge}
                    <i class="dropdown-icon">▼</i>
                </a>
                <ul class="submenu">
                    ${item.modules.map(module => `
                        <li><a href="${module.path}">${module.title}</a></li>
                    `).join('')}
                </ul>
            </li>
        `;
    } else {
        return `
            <li class="nav-item">
                <a href="${item.path}" class="nav-link">
                    ${item.title}${newBadge}
                </a>
            </li>
        `;
    }
}

/**
 * 初始化导航事件
 */
function initNavigationEvents() {
    // 移动端菜单切换
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }
    
    // 下拉菜单事件
    const submenuItems = document.querySelectorAll('.has-submenu');
    submenuItems.forEach(item => {
        const link = item.querySelector('.nav-link');
        const submenu = item.querySelector('.submenu');
        
        if (link && submenu) {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                item.classList.toggle('active');
            });
            
            // 点击外部关闭下拉菜单
            document.addEventListener('click', (e) => {
                if (!item.contains(e.target)) {
                    item.classList.remove('active');
                }
            });
        }
    });
}

/**
 * 高亮当前页面
 */
function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentPath.includes(linkPath.replace('/', ''))) {
            link.classList.add('active');
            // 如果是子菜单项，也高亮父菜单
            const parentItem = link.closest('.has-submenu');
            if (parentItem) {
                parentItem.querySelector('.nav-link').classList.add('active');
            }
        }
    });
}

/**
 * 面包屑导航
 */
function generateBreadcrumb() {
    const breadcrumbContainer = document.querySelector('.breadcrumb');
    if (!breadcrumbContainer) return;
    
    const currentPath = window.location.pathname;
    const pathSegments = currentPath.split('/').filter(segment => segment);
    
    let breadcrumbHTML = '<a href="/index.html">首页</a>';
    let currentUrl = '';
    
    pathSegments.forEach((segment, index) => {
        currentUrl += '/' + segment;
        const isLast = index === pathSegments.length - 1;
        const title = getBreadcrumbTitle(segment, currentUrl);
        
        if (isLast) {
            breadcrumbHTML += ` > <span class="current">${title}</span>`;
        } else {
            breadcrumbHTML += ` > <a href="${currentUrl}">${title}</a>`;
        }
    });
    
    breadcrumbContainer.innerHTML = breadcrumbHTML;
}

/**
 * 获取面包屑标题
 */
function getBreadcrumbTitle(segment, fullPath) {
    // 根据路径段返回相应的中文标题
    const titleMap = {
        'part1_python_basics': 'Python基础',
        'part2_data_analysis': '数据分析基础',
        'part3_finance_applications': '金融专业应用',
        'part4_advanced_topics': '高级主题',
        'module1': '模块1',
        'module2': '模块2',
        'module3': '模块3',
        'module4': '模块4',
        'module5': '模块5',
        'module6': '模块6',
        'module7': '模块7',
        'module8': '模块8',
        'module9': '模块9',
        'module10': '模块10',
        'module11': '模块11',
        'module12': '模块12',
        'module13': '模块13',
        'module14': '模块14',
        'module15': '模块15',
        'module16': '模块16',
        'lesson1.html': '课时1',
        'lesson2.html': '课时2',
        'lesson3.html': '课时3',
        'lesson4.html': '课时4',
        'index.html': '概览',
        'exercises.html': '练习',
        'project.html': '项目'
    };
    
    return titleMap[segment] || segment.replace(/[-_]/g, ' ').replace(/\.html$/, '');
}

// 页面加载完成后初始化导航
document.addEventListener('DOMContentLoaded', () => {
    loadNavigation();
    generateBreadcrumb();
});

// 导出函数供其他模块使用
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadNavigation,
        generateBreadcrumb,
        NAV_CONFIG
    };
}