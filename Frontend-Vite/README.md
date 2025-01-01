## Frontend-Vite 目录 README

### 项目简介

`Frontend-Vite` 是秉文书城项目的前端部分，采用 **Vue 3** 框架与 **Vite** 构建工具开发，旨在提供高性能、模块化和现代化的用户界面。

---

### 技术栈

- **Vue 3**：基于组件的前端框架，支持响应式和声明式编程。
- **Pinia**：轻量级状态管理库，用于管理全局状态。
- **Vite**：极速构建工具，支持现代化前端开发体验。
- **SCSS**：为样式编写提供更强大的功能与可维护性。
- **Axios**：轻量级 HTTP 客户端，用于前后端数据交互。

---

### 目录结构

```plaintext
Frontend-Vite/
├── public/                # 静态资源目录
├── src/                   # 核心源码
│   ├── assets/            # 静态文件（CSS、图片等）
│   ├── apis/              # API 接口管理
│   ├── components/        # 通用组件
│   ├── composables/       # 组合式函数
│   ├── directives/        # 自定义指令
│   ├── router/            # 路由配置
│   ├── stores/            # 状态管理
│   ├── styles/            # 全局样式
│   ├── utils/             # 工具函数
│   └── views/             # 页面组件
├── vite.config.js         # Vite 配置
└── package.json           # 项目依赖
```

---

### 环境配置

1. 安装依赖：

    ```bash
    npm install
    ```

2. 启动开发服务器：

    ```bash
    npm run dev
    ```

3. 构建生产环境：

    ```bash
    npm run build
    ```

---

### 项目亮点

- **响应式布局**：兼容不同屏幕设备的用户界面设计。
- **模块化开发**：组件化设计提升代码可维护性。
- **性能优化**：通过 Vite 实现极速冷启动和高效模块热更新。
- **友好交互**：提供直观流畅的用户体验。

---

### 致谢

感谢所有团队成员对前端开发的支持，如需了解更多信息，请参考项目根目录下的 [README.md](../README.md)。