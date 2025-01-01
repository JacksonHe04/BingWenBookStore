# 秉文书城项目 README

## 项目简介

**秉文书城**是一个在线书店项目，作为东南大学计算机科学与工程学院数据库原理课程的课程项目。项目名称旨在致敬东南大学创始人 **郭秉文先生**。

### 团队成员

- **何锦诚**：前端开发与UI设计
- **郑宇榕**：后端开发
- **刘睿哲**：产品管理与运维

该项目通过友好的前端界面和高效的后端逻辑，为用户提供流畅的电子商务体验。

## 项目特色

- 全面的书籍管理系统
- 用户友好的购物车与订单系统
- 安全的用户认证与支付功能
- 现代化的响应式设计界面

## 项目结构

```
BingWenBookStore/
├── BookStoreBackend/       # 基于Django的后端
├── Documents/              # 设计文档与项目报告
├── Frontend-Vite/          # 基于Vite的Vue.js前端
├── Resources/              # 数据来源与分析
└── README.md               # 本README文件
```

项目的完整英文版README请参见：[Documents/README_EN.md](Documents/README_EN.md)。

## 安装与运行指南

### 环境依赖

在开始之前，请确保安装以下工具：

- **Node.js**：v16及以上
- **Python**：v3.10及以上
- **MySQL**：最新稳定版

### 后端配置

1. 进入 `BookStoreBackend` 目录：

    ```bash
    cd BookStoreBackend
    ```

2. 安装后端依赖：

    ```bash
    pip install -r requirements.txt
    ```

3. 配置数据库：

   - 打开 `BookStoreBackend/settings.py` 文件，在 `DATABASES` 配置项中填写你的 MySQL 数据库信息。

4. 执行数据库迁移：

    ```bash
    python manage.py migrate
    ```

5. （可选）生成测试数据并导入数据库：

    ```bash
    python import_books.py
    ```

6. 启动Django后端服务：

    ```bash
    python manage.py runserver
    ```

   后端服务将运行在 `http://127.0.0.1:8000`。

### 前端配置

1. 进入 `Frontend-Vite` 目录：

    ```bash
    cd Frontend-Vite
    ```

2. 安装前端依赖：

    ```bash
    npm install
    ```

3. 启动开发服务器：

    ```bash
    npm run dev
    ```

   前端服务将运行在 `http://127.0.0.1:5173`。

4. （可选）构建生产环境版本：

    ```bash
    npm run build
    ```

   构建输出将在 `dist` 文件夹中生成。

## 使用说明

- 在浏览器中访问 `http://127.0.0.1:5173` 使用前端页面。
- 后端API服务可通过 `http://127.0.0.1:8000` 进行调用。

## 项目资源与文档

- **Documents/**: 包含项目报告和设计文档。
- **Resources/**: 包含数据来源说明和清洗后的数据文件。

## 许可证

本项目采用 MIT 开源许可证，详情请参见 [LICENSE](LICENSE) 文件。

## 致谢

我们感谢数据库原理课程的老师给予的指导，以及东南大学提供的学习平台。特别向 **郭秉文先生** 致敬，他的远见卓识不断激励着我们前行。

---

如有疑问或想要参与贡献，请随时联系团队成员。祝您使用愉快！🎉