### README.md - **BingWenBookStore**

# 项目简介

**BingWenBookStore** 是一个基于 Django 后端和 Vue.js 前端的网上书店项目，提供商品浏览、购物车、订单管理、用户账户等功能。项目使用 MySQL 数据库来存储商品信息、用户数据和订单记录，并通过 RESTful API 实现前后端的分离。

## 目录结构

```plaintext
.
├── Backend                # 后端代码 (Django)
│   └── BookStoreBackend   # 后端核心模块
│       ├── cart           # 购物车模块
│       ├── category       # 商品分类模块
│       ├── media          # 媒体文件（如图片）
│       ├── order          # 订单模块
│       ├── product        # 商品模块
│       ├── user           # 用户模块
│       └── manage.py      # Django 管理脚本
├── Docs                   # 数据分析文档
│   ├── Book Analysis Data.csv
│   └── Book Analysis Clean Data.csv
├── Frontend-Vite          # 前端代码 (Vue.js + Vite)
│   ├── dist               # 构建后的文件
│   ├── public             # 公共资源
│   ├── src                # 源代码
│   │   ├── apis           # API 请求
│   │   ├── assets         # 静态资源
│   │   ├── components     # Vue 组件
│   │   ├── composables    # 组合式函数
│   │   ├── router         # 路由管理
│   │   ├── stores         # 状态管理 (Pinia)
│   │   ├── styles         # 样式文件
│   │   ├── utils          # 工具函数
│   │   └── views          # 页面组件
├── help_notes             # 帮助文档
└── help_pdf               # 帮助 PDF 文件
```

## 功能模块

### 1. **后端 (Django)**

- **用户模块 (`user`)**：处理用户注册、登录、权限管理、用户信息。
- **购物车模块 (`cart`)**：用户可以将商品添加到购物车，管理购物车项。
- **商品分类模块 (`category`)**：展示和管理商品分类，支持多级分类。
- **商品模块 (`product`)**：展示商品详情，支持商品的增、删、改、查操作。
- **订单模块 (`order`)**：管理用户订单，支持下单、支付、订单状态更新等操作。

### 2. **前端 (Vue.js + Vite)**

- **首页 (`Home`)**：展示推荐商品、热门商品和分类信息。
- **商品详情页 (`Detail`)**：展示商品的详细信息和购买选项。
- **购物车页 (`CartList`)**：用户查看和编辑购物车内的商品。
- **结算页 (`Checkout`)**：用户完成订单结算、支付。
- **支付页 (`Pay`)**：处理支付过程并显示支付结果。
- **用户中心 (`Member`)**：查看和修改用户信息，查看订单历史。
- **商品分类页 (`Category`)**：展示商品分类，支持分类浏览。
- **登录页 (`Login`)**：用户登录系统。

### 3. **数据库 (MySQL)**

- 使用 MySQL 数据库存储用户信息、商品数据、订单数据等。
- 后端提供 API 接口，前端通过 API 获取和提交数据。

---

## 环境配置

### 1. **安装前提**

确保你已经安装了以下软件：

- **Python 3.x**：用于后端 Django 项目。
- **Node.js**：用于前端开发，推荐使用 LTS 版本。
- **MySQL**：用于数据库管理。

### 2. **后端环境搭建**

1. 克隆后端项目：

   ```bash
   git clone https://github.com/your-repository/BingWenBookStore.git
   cd Backend/BookStoreBackend
   ```

2. 创建虚拟环境并安装依赖：

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. 配置数据库连接：在 `settings.py` 中配置 MySQL 数据库连接。

4. 运行数据库迁移：

   ```bash
   python manage.py migrate
   ```

5. 启动开发服务器：

   ```bash
   python manage.py runserver
   ```

   后端 API 将在 `http://localhost:8000` 上运行。

### 3. **前端环境搭建**

1. 克隆前端项目：

   ```bash
   git clone https://github.com/your-repository/BingWenBookStore.git
   cd Frontend-Vite
   ```

2. 安装依赖：

   ```bash
   npm install
   ```

3. 启动开发服务器：

   ```bash
   npm run dev
   ```

   前端应用将在 `http://localhost:3000` 上运行。

---

## 功能介绍

### 1. **用户系统**

- 用户可以通过注册、登录、登出等功能管理自己的账户。
- 支持查看个人信息、修改密码、查看历史订单。

### 2. **商品管理**

- 浏览商品分类、查看商品详细信息。
- 支持商品加入购物车，编辑购物车中的商品。

### 3. **购物车与结算**

- 用户可以将商品添加到购物车，查看购物车中的商品，编辑数量。
- 在结算页面，用户可以选择支付方式，并确认订单。

### 4. **订单管理**

- 用户可以查看订单的状态（未支付、已支付、已发货、已完成等）。
- 支持订单的查询、支付。

---

## 技术栈

- **后端**：Django, Django REST Framework, MySQL
- **前端**：Vue.js, Vite, Pinia (状态管理), Axios (数据请求)
- **数据库**：MySQL
- **工具**：Docker (可选)，Git，Nginx (部署)

---

## 部署

### 1. **后端部署**

1. 将后端项目部署到服务器。
2. 配置数据库连接，迁移数据库。
3. 配置 Nginx 或 Gunicorn 来运行 Django 项目。

### 2. **前端部署**

1. 使用 Vite 构建生产版本：

   ```bash
   npm run build
   ```

2. 部署构建后的文件到服务器，使用 Nginx 或其他静态文件服务进行托管。

---

## 贡献

欢迎提出问题、报告 bug、提交功能请求或进行贡献！我们欢迎你的 Pull Requests。

### 如何贡献

1. Fork 本仓库。
2. 创建你的功能分支 (`git checkout -b feature-branch`)。
3. 提交你的更改 (`git commit -am 'Add new feature'`)。
4. 推送到分支 (`git push origin feature-branch`)。
5. 创建 Pull Request。

---

## 许可

该项目采用 [MIT 许可证](LICENSE)。
