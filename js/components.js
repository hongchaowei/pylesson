// 可复用HTML组件库

/**
 * 创建返回首页按钮
 * @param {string} homePath - 首页路径
 * @param {string} text - 按钮文本
 */
function createHomeButton(homePath = 'index.html', text = '返回首页') {
    const btn = document.createElement('a');
    btn.textContent = text;
    btn.href = homePath;
    btn.style.position = 'fixed';
    btn.style.top = '10px';
    btn.style.right = '10px';
    btn.style.zIndex = '9999';
    btn.style.padding = '8px 16px';
    btn.style.background = '#0078d7';
    btn.style.color = 'white';
    btn.style.textDecoration = 'none';
    btn.style.borderRadius = '4px';
    btn.style.fontSize = '14px';
    btn.style.fontWeight = '500';
    btn.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    btn.style.transition = 'all 0.3s ease';
    
    // 悬停效果
    btn.addEventListener('mouseenter', function() {
        this.style.background = '#106ebe';
        this.style.transform = 'translateY(-1px)';
        this.style.boxShadow = '0 4px 8px rgba(0,0,0,0.15)';
    });
    
    btn.addEventListener('mouseleave', function() {
        this.style.background = '#0078d7';
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
    });
    
    document.body.appendChild(btn);
    return btn;
}

/**
 * 创建面包屑导航
 * @param {Array} breadcrumbs - 面包屑数据 [{text: '首页', href: 'index.html'}, ...]
 * @param {string} containerId - 容器ID
 */
function createBreadcrumb(breadcrumbs, containerId = 'breadcrumb-container') {
    let container = document.getElementById(containerId);
    if (!container) {
        container = document.createElement('nav');
        container.id = containerId;
        container.className = 'breadcrumb-nav';
        
        // 插入到header后面
        const header = document.querySelector('header');
        if (header) {
            header.insertAdjacentElement('afterend', container);
        } else {
            document.body.insertBefore(container, document.body.firstChild);
        }
    }
    
    const breadcrumbHTML = breadcrumbs.map((item, index) => {
        if (index === breadcrumbs.length - 1) {
            return `<span class="breadcrumb-current">${item.text}</span>`;
        } else {
            return `<a href="${item.href}" class="breadcrumb-link">${item.text}</a>`;
        }
    }).join('<span class="breadcrumb-separator"> > </span>');
    
    container.innerHTML = `<div class="container">${breadcrumbHTML}</div>`;
    
    // 添加样式
    if (!document.getElementById('breadcrumb-styles')) {
        const style = document.createElement('style');
        style.id = 'breadcrumb-styles';
        style.textContent = `
            .breadcrumb-nav {
                background: #f8f9fa;
                padding: 10px 0;
                border-bottom: 1px solid #e9ecef;
                font-size: 14px;
            }
            .breadcrumb-link {
                color: #0078d7;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            .breadcrumb-link:hover {
                color: #106ebe;
                text-decoration: underline;
            }
            .breadcrumb-current {
                color: #6c757d;
                font-weight: 500;
            }
            .breadcrumb-separator {
                color: #6c757d;
                margin: 0 8px;
            }
        `;
        document.head.appendChild(style);
    }
    
    return container;
}

/**
 * 创建进度指示器
 * @param {number} current - 当前步骤
 * @param {number} total - 总步骤数
 * @param {Array} labels - 步骤标签
 */
function createProgressIndicator(current, total, labels = []) {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'progress-indicator';
    
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    
    const progressFill = document.createElement('div');
    progressFill.className = 'progress-fill';
    progressFill.style.width = `${(current / total) * 100}%`;
    
    progressBar.appendChild(progressFill);
    progressContainer.appendChild(progressBar);
    
    // 添加步骤点
    const stepsContainer = document.createElement('div');
    stepsContainer.className = 'progress-steps';
    
    for (let i = 1; i <= total; i++) {
        const step = document.createElement('div');
        step.className = `progress-step ${i <= current ? 'completed' : ''} ${i === current ? 'current' : ''}`;
        step.textContent = i;
        
        if (labels[i - 1]) {
            step.title = labels[i - 1];
        }
        
        stepsContainer.appendChild(step);
    }
    
    progressContainer.appendChild(stepsContainer);
    
    // 添加样式
    if (!document.getElementById('progress-styles')) {
        const style = document.createElement('style');
        style.id = 'progress-styles';
        style.textContent = `
            .progress-indicator {
                margin: 20px 0;
                position: relative;
            }
            .progress-bar {
                height: 4px;
                background: #e9ecef;
                border-radius: 2px;
                overflow: hidden;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #0078d7, #106ebe);
                transition: width 0.3s ease;
            }
            .progress-steps {
                display: flex;
                justify-content: space-between;
                margin-top: 10px;
            }
            .progress-step {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: #e9ecef;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: bold;
                color: #6c757d;
                transition: all 0.3s ease;
            }
            .progress-step.completed {
                background: #0078d7;
                color: white;
            }
            .progress-step.current {
                background: #106ebe;
                color: white;
                transform: scale(1.1);
                box-shadow: 0 2px 8px rgba(16, 110, 190, 0.3);
            }
        `;
        document.head.appendChild(style);
    }
    
    return progressContainer;
}

/**
 * 创建学习时间估算器
 * @param {number} estimatedMinutes - 预计学习时间（分钟）
 * @param {string} difficulty - 难度级别 (beginner, intermediate, advanced)
 */
function createTimeEstimator(estimatedMinutes, difficulty = 'intermediate') {
    const container = document.createElement('div');
    container.className = 'time-estimator';
    
    const difficultyColors = {
        beginner: '#28a745',
        intermediate: '#ffc107',
        advanced: '#dc3545'
    };
    
    const difficultyLabels = {
        beginner: '初级',
        intermediate: '中级',
        advanced: '高级'
    };
    
    const hours = Math.floor(estimatedMinutes / 60);
    const minutes = estimatedMinutes % 60;
    
    let timeText = '';
    if (hours > 0) {
        timeText = `${hours}小时${minutes > 0 ? minutes + '分钟' : ''}`;
    } else {
        timeText = `${minutes}分钟`;
    }
    
    container.innerHTML = `
        <div class="time-info">
            <span class="time-icon">⏱️</span>
            <span class="time-text">预计学习时间：${timeText}</span>
            <span class="difficulty-badge" style="background-color: ${difficultyColors[difficulty]}">
                ${difficultyLabels[difficulty]}
            </span>
        </div>
    `;
    
    // 添加样式
    if (!document.getElementById('time-estimator-styles')) {
        const style = document.createElement('style');
        style.id = 'time-estimator-styles';
        style.textContent = `
            .time-estimator {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 12px 16px;
                margin: 16px 0;
            }
            .time-info {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 14px;
            }
            .time-icon {
                font-size: 16px;
            }
            .time-text {
                color: #495057;
                font-weight: 500;
            }
            .difficulty-badge {
                color: white;
                padding: 2px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
            }
        `;
        document.head.appendChild(style);
    }
    
    return container;
}

/**
 * 创建知识点标签
 * @param {Array} tags - 标签数组
 */
function createKnowledgeTags(tags) {
    const container = document.createElement('div');
    container.className = 'knowledge-tags';
    
    const tagsHTML = tags.map(tag => 
        `<span class="knowledge-tag">${tag}</span>`
    ).join('');
    
    container.innerHTML = `
        <div class="tags-label">知识点：</div>
        <div class="tags-list">${tagsHTML}</div>
    `;
    
    // 添加样式
    if (!document.getElementById('knowledge-tags-styles')) {
        const style = document.createElement('style');
        style.id = 'knowledge-tags-styles';
        style.textContent = `
            .knowledge-tags {
                margin: 16px 0;
                display: flex;
                align-items: flex-start;
                gap: 8px;
                flex-wrap: wrap;
            }
            .tags-label {
                font-weight: 600;
                color: #495057;
                font-size: 14px;
                margin-top: 4px;
            }
            .tags-list {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
            }
            .knowledge-tag {
                background: #e3f2fd;
                color: #1976d2;
                padding: 4px 8px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
                border: 1px solid #bbdefb;
            }
        `;
        document.head.appendChild(style);
    }
    
    return container;
}

/**
 * 初始化页面组件
 * @param {Object} config - 配置对象
 */
function initPageComponents(config = {}) {
    // 默认配置
    const defaultConfig = {
        showHomeButton: true,
        homePath: 'index.html',
        homeButtonText: '返回首页',
        breadcrumbs: null,
        progress: null,
        timeEstimate: null,
        knowledgeTags: null
    };
    
    const finalConfig = { ...defaultConfig, ...config };
    
    // 创建返回首页按钮
    if (finalConfig.showHomeButton) {
        createHomeButton(finalConfig.homePath, finalConfig.homeButtonText);
    }
    
    // 创建面包屑导航
    if (finalConfig.breadcrumbs) {
        createBreadcrumb(finalConfig.breadcrumbs);
    }
    
    // 创建进度指示器
    if (finalConfig.progress) {
        const progressElement = createProgressIndicator(
            finalConfig.progress.current,
            finalConfig.progress.total,
            finalConfig.progress.labels
        );
        
        // 插入到适当位置
        const target = document.querySelector('.lesson-content') || document.querySelector('main');
        if (target) {
            target.insertBefore(progressElement, target.firstChild);
        }
    }
    
    // 创建时间估算器
    if (finalConfig.timeEstimate) {
        const timeElement = createTimeEstimator(
            finalConfig.timeEstimate.minutes,
            finalConfig.timeEstimate.difficulty
        );
        
        // 插入到header后面
        const header = document.querySelector('header');
        if (header) {
            header.insertAdjacentElement('afterend', timeElement);
        }
    }
    
    // 创建知识点标签
    if (finalConfig.knowledgeTags) {
        const tagsElement = createKnowledgeTags(finalConfig.knowledgeTags);
        
        // 插入到lesson-content开始处
        const lessonContent = document.querySelector('.lesson-content');
        if (lessonContent) {
            lessonContent.insertBefore(tagsElement, lessonContent.firstChild);
        }
    }
}

// 导出函数（如果使用模块系统）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        createHomeButton,
        createBreadcrumb,
        createProgressIndicator,
        createTimeEstimator,
        createKnowledgeTags,
        initPageComponents
    };
}