# 项目开发说明

## 郑宇榕、刘睿哲，欢迎加入本项目！

test为了确保项目的顺利进行，我们希望后端开发者能够使用Django框架来构建后端服务。请将所有后端相关的工作集中在`Backend`目录下，并尽量避免对目录之外的前端代码进行修改。  

**我的意思是，当你把项目克隆到本地后，再用编辑器（如PyCharm、VSCode等）打开 `Backend`目录，而不是打开你克隆的根目录 !!!**。

### Django基础教程

- **官方文档**: [Django 官方文档](https://docs.djangoproject.com/)
- **快速入门**: 请参考`Backend/README.md`中的详细指南。

### 前后端通信

为了保证前后端之间能够有效地进行数据交换，我们采用了以下技术和配置：

- **Django REST Framework**: 用于构建RESTful API。
- **CORS Headers**: 用于处理跨域请求。

请参考`Backend/README.md`中的详细说明和示例代码。我们将采用RESTful API的方式进行数据交互，请确保API设计符合以下要求：
- 使用标准HTTP状态码
- 返回JSON格式的数据
- 提供清晰的API文档

感谢您的贡献！如有任何问题或建议，请随时与我（何锦诚）联系。
