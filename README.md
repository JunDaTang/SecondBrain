# SecondBrain - VS Code 第二大脑系统

这是一个基于 VS Code 构建的 PARA + Zettelkasten 混合知识管理系统，集成了强大的网页剪辑功能。

## 🗂️ 目录结构

```
SecondBrain/
├── PARA/                    # PARA 方法论系统
│   ├── 01_Projects/        # 项目：有明确结果和截止日期的工作
│   ├── 02_Areas/           # 领域：需要持续维护的生活领域
│   ├── 03_Resources/       # 资源：未来可能有用的参考材料
│   └── 04_Archive/         # 归档：来自其他三个类别的不活跃项目
├── ZK/                     # Zettelkasten 卢曼笔记法
│   ├── 01_Fleeting/        # 速记：临时想法和待整理内容
│   ├── 02_Literature/      # 文献笔记：书籍、文章等的读书笔记
│   └── 03_Permanent/       # 永久笔记：经过思考的知识卡片
└── Inbox/                  # 统一收集箱
    ├── web-clips/          # 网页剪辑内容（自动分类）
    ├── quick-notes/        # 快速记录
    └── daily/              # 每日收集
```

## 🚀 快速开始

### 1. 安装推荐扩展

VS Code 会自动提示安装推荐扩展，包括：
- **Markdown All in One** - Markdown 编辑增强
- **Foam** - 知识网络可视化和双向链接
- **Paste Image** - 快速粘贴截图
- **Todo Tree** - 任务管理
- **Draw.io Integration** - 绘图工具

### 2. 配置网页剪辑

安装 **Obsidian Web Clipper** 浏览器扩展：
- **Chrome**: 在 Chrome 应用商店搜索 "Obsidian Web Clipper"
- **Firefox**: 在 Firefox 扩展商店搜索 "Obsidian Web Clipper" 
- **Safari/Edge**: 支持 Chrome 扩展或直接下载

**配置步骤**：
1. 安装扩展后点击浏览器工具栏的剪辑图标
2. 选择 VS Code 工作区路径：`F:\github\SecondBrain`
3. 设置默认保存位置：`Inbox/web-clips/` 文件夹
4. 选择合适的剪辑模板（文章、参考资料等）

### 3. 使用代码片段

在 Markdown 文件中输入：

**PARA 系统模板**：
- `/para-project` + Tab → 创建项目模板
- `/para-project-dev` + Tab → 软件开发项目
- `/para-project-ai` + Tab → AI/大模型项目
- `/para-area` + Tab → 创建领域模板
- `/para-area-tech` + Tab → 技术领域管理
- `/para-resource` + Tab → 创建资源模板
- `/para-resource-tech` + Tab → 技术资源
- `/para-resource-code` + Tab → 代码片段

**ZK 系统模板**：
- `/zk-fleeting` + Tab → 速记笔记
- `/zk-literature` + Tab → 文献笔记
- `/zk-literature-tech` + Tab → 技术学习笔记
- `/zk-permanent` + Tab → 永久笔记
- `/zk-permanent-tech` + Tab → 技术概念笔记
- `/zk-daily` + Tab → 日记模板
- `/zk-daily-dev` + Tab → 开发日志

**快捷模板**：
- `/quick` + Tab → 快速笔记

### 4. 快捷键

- `Ctrl+Alt+D` → 打开今日笔记
- `Ctrl+Alt+G` → 显示知识图谱
- `Ctrl+Alt+R` → 打开随机笔记
- `Ctrl+Alt+P` → 快速打开文件

## 📝 使用方法

### 网页剪辑工作流

**1. 快速剪辑**：
- 浏览网页时点击 Obsidian Web Clipper 图标
- 选择剪辑类型：完整文章、高亮内容、或自定义选择
- 自动保存到 `Inbox/web-clips/` 文件夹

**2. 统一收集**：
- 所有剪辑内容统一进入 Inbox 收集箱
- 定期查看 `Inbox/` 文件夹进行分类整理
- 使用双向链接 `[[]]` 连接相关内容

**3. 知识转化**：
- 技术文章 → 移至 `PARA/03_Resources/` 或转为 `ZK/02_Literature/`
- 项目参考 → 关联到相关项目文件夹
- 灵感想法 → 发展为 `ZK/01_Fleeting/` 或 `ZK/03_Permanent/` 笔记

### PARA 工作流

1. **项目 (Projects)**: 为每个项目创建文件夹，包含 `index.md` 主页
2. **领域 (Areas)**: 按生活/工作领域组织，如健康、财务、技能等
3. **资源 (Resources)**: 存放参考资料、模板、清单等
4. **归档 (Archive)**: 使用任务自动归档已完成项目

### Zettelkasten 工作流

1. **收集想法**: 在 `Inbox/` 和 `01_Fleeting/` 中快速记录想法和剪辑内容
2. **整理文献**: 将读书笔记和网页剪辑整理到 `02_Literature/`
3. **提炼知识**: 在 `03_Permanent/` 中创建原子化知识卡片
4. **建立连接**: 使用 `[[链接]]` 语法连接相关笔记

### 链接语法

- **PARA 内部链接**: `[文档名](../Resources/文档.md)`
- **Zettelkasten 链接**: `[[UID-标题]]` 或 `[[标题]]`
- **Inbox 内容链接**: `[[Inbox/web-clips/文章标题]]`
- **反向链接**: Foam 扩展会自动显示哪些笔记链接到当前笔记

## 🛠️ 实用任务

在命令面板 (`Ctrl+Shift+P`) 中运行：
- **🔍 创建日记** - 自动创建今天的日记文件
- **🚀 快速创建PARA项目** - 交互式项目创建
- **💾 备份到Git** - 快速提交所有更改

详细说明请查看：[快速开始指南](快速开始指南.md)

## 📱 移动端同步

建议配合以下方案：
1. **Git 版本控制**: 所有内容同步到 GitHub/GitLab
2. **Obsidian Mobile**: 作为移动端查看和轻量编辑工具
3. **Working Copy** (iOS) 或 **MGit** (Android): 直接编辑 Git 仓库

移动端也可以使用 Obsidian Web Clipper，剪辑的内容会自动同步到桌面端的 Inbox。

## 🎯 最佳实践

1. **每日 Inbox 清理**: 定期查看 `Inbox/` 文件夹，将内容分类到合适位置
2. **剪辑即时标记**: 为剪辑内容添加临时标签，便于后续整理
3. **及时转化**: 将有价值的剪辑内容及时转化为项目资源或知识卡片
4. **建立连接**: 新建笔记时主动寻找与现有笔记的联系
5. **版本控制**: 定期提交 Git，记录知识演进过程

## 🌐 Inbox 管理策略

### 剪辑内容分类
- **技术文章**: 开发相关的技术博客、文档
- **学习资源**: 教程、课程、最佳实践
- **项目参考**: 设计案例、解决方案、工具推荐
- **新闻资讯**: 行业动态、技术趋势

### 定期整理规则
- **每日**: 快速浏览新剪辑，标记重要内容
- **每周**: 将有价值剪辑移动到对应的 PARA/ZK 位置
- **每月**: 清理过期或价值不高的剪辑
- **每季**: 回顾剪辑转化效果，优化收集策略

## 🔧 自定义配置

所有配置文件位于 `.vscode/` 目录：
- `settings.json` - 工作区设置
- `keybindings.json` - 自定义快捷键
- `markdown.code-snippets` - 代码片段和模板
- `tasks.json` - 自动化任务

随时根据个人习惯调整这些配置！

---

💡 **提示**: Inbox 作为统一的收集箱，让网页剪辑与其他输入内容一起进行集中管理，避免了多个入口的复杂性。通过定期清理 Inbox，你可以将有价值的网页内容转化为个人知识资产。 