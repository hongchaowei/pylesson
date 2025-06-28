// 图片懒加载实现
document.addEventListener('DOMContentLoaded', function() {
    let lazyImages = [].slice.call(document.querySelectorAll('img.lazy'));
    let active = false;

    const lazyLoad = function() {
        if (active === false) {
            active = true;

            setTimeout(function() {
                lazyImages.forEach(function(lazyImage) {
                    if ((lazyImage.getBoundingClientRect().top <= window.innerHeight && lazyImage.getBoundingClientRect().bottom >= 0) && getComputedStyle(lazyImage).display !== 'none') {
                        lazyImage.src = lazyImage.dataset.src;
                        lazyImage.srcset = lazyImage.dataset.srcset || '';
                        lazyImage.classList.remove('lazy');

                        lazyImages = lazyImages.filter(function(image) {
                            return image !== lazyImage;
                        });

                        if (lazyImages.length === 0) {
                            document.removeEventListener('scroll', lazyLoad);
                            window.removeEventListener('resize', lazyLoad);
                            window.removeEventListener('orientationchange', lazyLoad);
                        }
                    }
                });

                active = false;
            }, 200);
        }
    };

    // 添加事件监听
    document.addEventListener('scroll', lazyLoad);
    window.addEventListener('resize', lazyLoad);
    window.addEventListener('orientationchange', lazyLoad);
    
    // 初始加载
    lazyLoad();
});

// 性能监控
const performanceMonitor = {
    init: function() {
        // 监控页面加载性能
        window.addEventListener('load', () => {
            const timing = performance.timing;
            const interactive = timing.domInteractive - timing.navigationStart;
            const dcl = timing.domContentLoadedEventEnd - timing.navigationStart;
            const complete = timing.domComplete - timing.navigationStart;
            
            console.log('Interactive:', interactive + 'ms');
            console.log('DOMContentLoaded:', dcl + 'ms');
            console.log('Complete:', complete + 'ms');
        });

        // 监控资源加载
        if (window.PerformanceObserver) {
            const observer = new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    if (entry.initiatorType === 'img' || entry.initiatorType === 'css' || entry.initiatorType === 'script') {
                        console.log(`Resource ${entry.name} took ${entry.duration}ms to load`);
                    }
                }
            });
            observer.observe({ entryTypes: ['resource'] });
        }
    },

    // 错误监控
    errorHandler: function(error) {
        console.error('Caught error:', error);
        // 这里可以添加错误上报逻辑
    }
};

// 初始化性能监控
performanceMonitor.init();

// 添加全局错误处理
window.onerror = performanceMonitor.errorHandler;