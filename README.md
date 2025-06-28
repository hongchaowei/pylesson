# Python金融应用课程网站

## 项目说明
这是一个基于HTML、CSS和JavaScript开发的静态网站，用于展示Python金融应用课程的教学内容。网站采用模块化设计，包含完整的课程大纲、学习路径和教学资源。

## 部署说明

### 腾讯云对象存储（COS）部署步骤

1. **准备工作**
   - 注册腾讯云账号
   - 开通对象存储服务
   - 创建存储桶（Bucket）
   - 设置存储桶为静态网站托管模式

2. **配置存储桶**
   - 进入存储桶配置页面
   - 开启"静态网站"功能
   - 设置默认首页为"index.html"
   - 配置错误页面（可选）

3. **上传文件**
   - 保持目录结构完整上传所有文件
   - 确保文件权限设置为公有读

4. **域名配置**
   - 可使用存储桶默认域名访问
   - 也可绑定自定义域名（需备案）
   - 如需https访问，需配置SSL证书

### 目录结构
```
/
├── css/
│   └── style.css
├── js/
│   └── load-nav.js
├── images/
├── part1_python_basics/
├── part2_data_analysis/
├── part3_finance_applications/
├── part4_advanced_topics/
├── index.html
├── syllabus.html
└── README.md
```

### 性能优化
1. 使用字节跳动静态资源CDN加速
2. 实现图片懒加载
3. 使用defer加载JavaScript
4. 添加页面预加载
5. DNS预解析配置

### 注意事项
1. 所有资源链接使用相对路径
2. 确保字体图标可以正常加载
3. 检查所有页面的跳转链接
4. 定期更新课程内容
5. 备份重要文件

## 维护更新
1. 定期检查链接有效性
2. 更新课程内容
3. 优化用户体验
4. 响应用户反馈

## 技术栈
- HTML5
- CSS3
- JavaScript
- Font Awesome 图标
- 响应式设计

## 浏览器支持
- Chrome (推荐)
- Firefox
- Safari
- Edge
- IE11+

## 联系方式
如有问题或建议，请通过以下方式联系：
- 邮箱：[your-email@example.com]
- 网站：[your-website.com]

## 版权信息
© 2023 Python金融应用课程. 保留所有权利。