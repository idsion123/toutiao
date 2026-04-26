# 📰 头条新闻管理系统

一个基于 **FastAPI + Vue 3** 的全栈新闻管理系统，采用前后端分离架构，支持新闻浏览、用户管理、收藏、历史记录、AI 对话和后台管理等功能。

---

## 🌟 项目亮点

- 🚀 **前后端分离**: FastAPI 后端 + Vue 3 前端，独立部署
- ⚡ **高性能**: 全异步架构，Redis 缓存优化
- 📱 **移动端优先**: Vant UI 组件库，完美的移动端体验
- 🔐 **安全可靠**: JWT Token 认证，密码加密存储
- 🤖 **AI 集成**: 内置 AI 智能对话功能
- 🎨 **国际化**: 支持中英文切换
- 🌙 **主题切换**: 浅色/深色主题支持

---

## 🏗️ 项目结构

### 整体架构

```
toutiao_project/
├── toutiao_backend/              # 后端项目 (FastAPI)
│   ├── cache/                    # Redis 缓存层
│   ├── config/                   # 配置文件
│   ├── crud/                     # 数据库操作层
│   ├── models/                   # SQLAlchemy 数据模型
│   ├── routers/                  # API 路由
│   ├── schemas/                  # Pydantic 数据验证
│   ├── utils/                    # 工具类
│   ├── media/                    # 静态文件
│   ├── main.py                   # FastAPI 应用入口
│   └── requirements.txt          # Python 依赖
│
└── xwzx-news/                    # 前端项目 (Vue 3)
    ├── public/                   # 静态资源
    ├── src/
    │   ├── api/                  # API 请求封装
    │   ├── components/           # 公共组件
    │   ├── config/               # 配置文件
    │   ├── i18n/                 # 国际化
    │   ├── router/               # 路由配置
    │   ├── store/                # Pinia 状态管理
    │   ├── views/                # 页面组件
    │   └── main.js               # Vue 应用入口
    └── package.json              # Node 依赖
```

### 后端详细结构

```
toutiao_backend/
├── cache/                    # Redis 缓存层
│   ├── __init__.py
│   └── news_cache.py         # 新闻缓存逻辑
├── config/                   # 配置文件
│   ├── __init__.py
│   ├── cache_config.py       # Redis 配置
│   └── db_config.py          # 数据库配置
├── crud/                     # 数据库操作层
│   ├── __init__.py
│   ├── admin_curd.py         # 后台管理 CRUD
│   ├── ai_chat.py            # AI 对话 CRUD
│   ├── favorites.py          # 收藏 CRUD
│   ├── history.py            # 历史记录 CRUD
│   ├── news.py               # 新闻 CRUD
│   ├── news_cache.py         # 新闻缓存 CRUD
│   └── users.py              # 用户 CRUD
├── models/                   # SQLAlchemy 数据模型
│   ├── __init__.py
│   ├── ai_chat.py
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── user.py
├── routers/                  # API 路由
│   ├── __init__.py
│   ├── admin.py              # 后台管理接口
│   ├── ai_chat.py            # AI 对话接口
│   ├── favorites.py          # 收藏接口
│   ├── history.py            # 历史记录接口
│   ├── news.py               # 新闻接口
│   └── users.py              # 用户接口
├── schemas/                  # Pydantic 数据验证模型
│   ├── __init__.py
│   ├── ai_chat.py
│   ├── favorites.py
│   ├── history.py
│   ├── news.py
│   └── users.py
├── utils/                    # 工具类
│   ├── __init__.py
│   ├── admin_auth.py         # 后台认证
│   ├── auth.py               # 用户认证 (JWT)
│   ├── exception.py          # 自定义异常
│   ├── exception_handlers.py # 异常处理器
│   ├── response.py           # 统一响应格式
│   ├── security.py           # 安全工具 (密码加密)
│   └── upload.py             # 文件上传
├── media/                    # 静态文件
│   └── avatars/              # 用户头像
├── main.py                   # FastAPI 应用入口
├── requirements.txt          # Python 依赖
└── toutiao.session.sql       # 数据库 SQL 文件
```

### 前端详细结构

```
xwzx-news/
├── src/
│   ├── api/                      # API 请求封装
│   │   ├── admin.js              # 后台管理 API
│   │   └── index.js              # 通用 API
│   ├── components/               # 公共组件
│   │   ├── NavBar.vue            # 导航栏
│   │   └── TabBar.vue            # 底部导航
│   ├── config/                   # 配置文件
│   │   └── api.js                # API 地址配置
│   ├── i18n/                     # 国际化
│   │   ├── index.js              # i18n 配置
│   │   └── locales/              # 语言包
│   ├── router/                   # 路由配置
│   │   └── index.js              # 路由定义
│   ├── store/                    # Pinia 状态管理
│   │   ├── index.js              # Store 入口
│   │   ├── user.js               # 用户状态
│   │   └── theme.js              # 主题状态
│   ├── views/                    # 页面组件
│   │   ├── Home.vue              # 首页
│   │   ├── Login.vue             # 登录页
│   │   ├── Register.vue          # 注册页
│   │   ├── NewsDetail.vue        # 新闻详情
│   │   ├── Profile.vue           # 个人中心
│   │   ├── Favorite.vue          # 我的收藏
│   │   ├── History.vue           # 浏览历史
│   │   ├── AIChat.vue            # AI 对话
│   │   ├── AdminDashboard.vue    # 后台仪表盘
│   │   ├── AdminUsers.vue        # 用户管理
│   │   ├── AdminNews.vue         # 新闻管理
│   │   └── AdminCategories.vue   # 分类管理
│   └── main.js                   # Vue 应用入口
├── index.html                    # HTML 模板
├── package.json                  # Node 依赖
└── vite.config.js                # Vite 配置
```

---

## 🚀 技术栈

### 后端技术栈
- **Web 框架**: FastAPI 0.136.1
- **ORM**: SQLAlchemy 2.0.45 (异步)
- **数据库**: MySQL (aiomysql 0.3.2)
- **缓存**: Redis (aioredis 2.0.1)
- **异步服务器**: Uvicorn 0.46.0
- **数据验证**: Pydantic 2.13.3
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt 3.2.2
- **模板引擎**: Jinja2 3.1.6

### 前端技术栈
- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite 7.3.1
- **UI 组件库**: Vant 4.9.21 (移动端)
- **状态管理**: Pinia 3.0.3
- **路由**: Vue Router 4.5.1
- **HTTP 客户端**: Axios 1.12.2
- **国际化**: Vue I18n 9.8.0
- **Markdown 渲染**: Marked 16.3.0
- **HTML 净化**: DOMPurify 3.2.7

---

## ✨ 功能特性

### 核心功能
- ✅ **新闻管理**: 分类浏览、分页加载、详情查看、浏览量统计
- ✅ **用户系统**: 注册、登录、JWT 认证、个人信息管理、头像上传
- ✅ **收藏系统**: 收藏新闻、收藏列表、取消收藏
- ✅ **浏览历史**: 自动记录、历史列表、删除记录
- ✅ **AI 对话**: 智能对话接口
- ✅ **缓存优化**: Redis 缓存新闻列表，提升性能

### 后台管理
- ✅ **仪表盘**: 用户总数、新闻总数、最近新闻统计
- ✅ **用户管理**: 查看、搜索、删除用户
- ✅ **新闻管理**: 查看、搜索、分类筛选、删除新闻
- ✅ **分类管理**: 查看、添加、编辑、删除分类
- ✅ **权限控制**: 基于 JWT Token 的认证机制

### 技术特性
- ✅ **异步处理**: 全异步架构，高并发支持
- ✅ **CORS 支持**: 跨域请求配置
- ✅ **统一响应**: 标准化的 API 响应格式
- ✅ **异常处理**: 全局异常捕获和处理
- ✅ **静态文件**: 支持头像等静态资源服务

---

## 📦 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+
- Redis 6+

### 后端部署

1. **进入后端目录**
```bash
cd toutiao_backend
```

2. **创建虚拟环境**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置数据库**

编辑 `config/db_config.py`:
```python
DATABASE_URL = "mysql+aiomysql://用户名:密码@localhost:3306/数据库名"
```

5. **配置 Redis**

编辑 `config/cache_config.py`:
```python
REDIS_URL = "redis://localhost:6379/0"
```

6. **创建数据库**
```sql
CREATE DATABASE 数据库名 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

7. **导入数据表结构**
```bash
mysql -u root -p 数据库名 < database.sql
```

8. **启动后端服务**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

后端服务将运行在: **http://localhost:8000**

### 前端部署

1. **进入前端目录**
```bash
cd xwzx-news
```

2. **安装依赖**
```bash
npm install
```

3. **配置 API 地址**

编辑 `src/config/api.js`:
```javascript
export const apiConfig = {
  baseURL: 'http://localhost:8000'  // 后端 API 地址
}
```

4. **启动开发服务器**
```bash
npm run dev
```

前端服务将运行在: **http://localhost:5173**

5. **生产构建**
```bash
npm run build
npm run preview  # 预览生产版本
```

---

## 🗺️ 前端路由

### 用户端路由

| 路径 | 组件 | 说明 | KeepAlive |
|------|------|------|-----------|
| `/` | - | 重定向到首页 | - |
| `/login` | Login | 登录页 | ❌ |
| `/register` | Register | 注册页 | ❌ |
| `/home` | Home | 首页（新闻列表） | ✅ |
| `/news/detail/:id` | NewsDetail | 新闻详情 | ❌ |
| `/history` | History | 浏览历史 | ❌ |
| `/favorite` | Favorite | 我的收藏 | ❌ |
| `/category` | Category | 分类页 | ✅ |
| `/aichat` | AIChat | AI 对话 | ✅ |
| `/my` | My | 我的 | ✅ |
| `/profile` | Profile | 个人信息 | ❌ |
| `/settings` | Settings | 设置页 | ❌ |

### 后台管理路由

| 路径 | 组件 | 说明 | 认证 |
|------|------|------|------|
| `/admin/dashboard` | AdminDashboard | 后台仪表盘 | ✅ |
| `/admin/users` | AdminUsers | 用户管理 | ✅ |
| `/admin/news` | AdminNews | 新闻管理 | ✅ |
| `/admin/categories` | AdminCategories | 分类管理 | ✅ |

---

## 🔗 前后端联调

### 数据交互流程

1. **用户登录**
```javascript
// 前端 (Login.vue)
const response = await axios.post('/api/users/login', {
  account: 'username',
  password: 'password123'
})

// 保存 token
localStorage.setItem('token', response.data.data.token)
```

2. **携带 Token 请求**
```javascript
// 前端 (axios 拦截器)
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

3. **后端验证**
```python
# 后端 (utils/auth.py)
async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="未提供认证令牌")
    
    token = authorization.replace("Bearer ", "")
    user = await verify_token(token)
    return user
```

### 跨域配置

后端已配置 CORS，允许前端跨域请求：

```python
# main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # 允许的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 开发工作流

1. **启动后端服务**
```bash
cd toutiao_backend
uvicorn main:app --reload --port 8000
```

2. **启动前端服务**
```bash
cd xwzx-news
npm run dev
```

3. **访问前端**
打开浏览器访问: http://localhost:5173

4. **调试 API**
- 前端: 浏览器开发者工具 Network 标签
- 后端: 终端日志输出
- API 文档: http://localhost:8000/docs (Swagger UI)

### 生产部署

#### 方案一：Nginx 反向代理

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /path/to/xwzx-news/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源
    location /media/ {
        proxy_pass http://localhost:8000;
    }
}
```

#### 方案二：Docker 部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  mysql:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: toutiao
    ports:
      - "3306:3306"

  redis:
    image: redis:6
    ports:
      - "6379:6379"

  backend:
    build: ./toutiao_backend
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - redis
    environment:
      DATABASE_URL: mysql+aiomysql://root:password@mysql:3306/toutiao
      REDIS_URL: redis://redis:6379/0

  frontend:
    build: ./xwzx-news
    ports:
      - "80:80"
    depends_on:
      - backend
```

---

### 新闻接口 `/api/news`

| 方法 | 路径 | 说明 | 参数 |
|------|------|------|------|
| GET | `/categories` | 获取分类列表 | skip, limit |
| GET | `/list` | 获取新闻列表 | page, categoryId, pageSize |
| GET | `/detail` | 获取新闻详情 | id |

**示例:**
```bash
# 获取新闻列表
GET /api/news/list?page=1&categoryId=1&pageSize=10

# 响应
{
  "code": 200,
  "message": "获取新闻列表成功",
  "data": {
    "list": [...],
    "total": 100,
    "hasMore": true
  }
}
```

### 用户接口 `/api/users`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/register` | 用户注册 | ❌ |
| POST | `/login` | 用户登录 | ❌ |
| GET | `/profile` | 获取用户信息 | ✅ |
| PUT | `/profile` | 更新用户信息 | ✅ |
| POST | `/upload-avatar` | 上传头像 | ✅ |

**示例:**
```bash
# 用户登录
POST /api/users/login
{
  "account": "username",
  "password": "password123"
}

# 响应
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {...}
  }
}
```

### 收藏接口 `/api/favorites`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/` | 获取收藏列表 | ✅ |
| POST | `/` | 添加收藏 | ✅ |
| DELETE | `/{news_id}` | 取消收藏 | ✅ |

### 历史记录接口 `/api/history`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| GET | `/` | 获取浏览历史 | ✅ |
| POST | `/` | 添加浏览记录 | ✅ |
| DELETE | `/{news_id}` | 删除记录 | ✅ |

### AI 对话接口 `/api/ai`

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/chat` | AI 对话 | ✅ |

### 后台管理接口 `/api/admin`

所有后台接口都需要认证 (Authorization: Bearer <token>)

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/dashboard/stats` | 获取统计数据 |
| GET | `/users` | 获取用户列表 |
| DELETE | `/users/{user_id}` | 删除用户 |
| GET | `/news` | 获取新闻列表 |
| DELETE | `/news/{news_id}` | 删除新闻 |
| GET | `/categories` | 获取分类列表 |
| POST | `/categories` | 添加分类 |
| PUT | `/categories/{category_id}` | 更新分类 |
| DELETE | `/categories/{category_id}` | 删除分类 |

**示例:**
```bash
# 获取仪表盘统计
GET /api/admin/dashboard/stats
Authorization: Bearer <your-token>

# 响应
{
  "code": 200,
  "message": "获取统计数据成功",
  "data": {
    "users_count": 150,
    "news_count": 403,
    "recent_news": [...]
  }
}
```

---

## 🔐 认证机制

### JWT Token 认证

1. **获取 Token**
   - 用户登录或注册后，后端返回 JWT Token
   - Token 有效期: 7 天

2. **使用 Token**
   ```http
   Authorization: Bearer <your-jwt-token>
   ```

3. **Token 验证**
   - 所有需要认证的接口都会验证 Token
   - Token 无效或过期会返回 401 错误

---

## 💾 数据库设计

### 主要数据表

**users (用户表)**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100),
    avatar VARCHAR(255),
    bio TEXT,
    gender ENUM('male', 'female', 'unknown') DEFAULT 'unknown',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**news (新闻表)**
```sql
CREATE TABLE news (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    image VARCHAR(255),
    author VARCHAR(50),
    category_id INT NOT NULL,
    views INT DEFAULT 0,
    publish_time DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

**categories (分类表)**
```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**favorites (收藏表)**
```sql
CREATE TABLE favorites (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    news_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (news_id) REFERENCES news(id),
    UNIQUE KEY unique_favorite (user_id, news_id)
);
```

**history (浏览历史表)**
```sql
CREATE TABLE history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    news_id INT NOT NULL,
    viewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (news_id) REFERENCES news(id)
);
```

---

## 🔧 开发指南

### 添加新接口

1. **定义数据模型** (`models/`)
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
```

2. **创建 CRUD 操作** (`crud/`)
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import NewModel

async def get_new_list(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(NewModel).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()
```

3. **定义 Schema** (`schemas/`)
```python
from pydantic import BaseModel

class NewItem(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True
```

4. **创建路由** (`routers/`)
```python
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db_session
from crud import new_curd
from utils.response import success_response

router = APIRouter(prefix="/api/new", tags=["new"])

@router.get("/list")
async def get_new_list(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db_session)
):
    data = await new_curd.get_new_list(db, skip, limit)
    return success_response(message="获取成功", data=data)
```

5. **注册路由** (`main.py`)
```python
from routers import new
app.include_router(new.router)
```

---

## 🐛 常见问题

### 1. 数据库连接失败
```python
# 检查 config/db_config.py 中的数据库连接字符串
DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/dbname"
```

### 2. Redis 连接失败
```python
# 检查 Redis 是否运行
redis-cli ping  # 应返回 PONG

# 检查 config/cache_config.py
REDIS_URL = "redis://localhost:6379/0"
```

### 3. CORS 跨域问题
```python
# main.py 中已配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. 静态文件无法访问
```python
# 确保 media 目录存在
# 检查 main.py 中的静态文件挂载
app.mount("/media", StaticFiles(directory="media"), name="media")
```

### 5. 异步数据库操作报错
```python
# 确保使用 AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db_session

async def your_function(db: AsyncSession = Depends(get_db_session)):
    # 使用 await 执行异步操作
    result = await db.execute(stmt)
```

---

## 📈 性能优化

### 1. Redis 缓存
- 新闻列表缓存: 减少数据库查询
- 分类列表缓存: 频繁访问的分类数据
- 缓存过期策略: 自动更新过期数据

### 2. 数据库优化
- 索引优化: 为常用查询字段添加索引
- 分页查询: 使用 offset/limit 分页
- 连接池: SQLAlchemy 异步连接池

### 3. 异步处理
- 全异步架构: FastAPI + SQLAlchemy Async
- 高并发支持: Uvicorn 异步服务器
- 非阻塞 I/O: 提升响应速度

---

## 📝 更新日志

### v1.0.0 (2026-04-26)
- ✨ 初始版本发布
- ✨ 前后端分离架构 (FastAPI + Vue 3)
- ✨ 实现新闻、用户、收藏、历史记录功能
- ✨ 集成 AI 对话功能
- ✨ 后台管理系统 (仪表盘、用户管理、新闻管理、分类管理)
- ✨ Redis 缓存优化
- ✨ JWT 认证机制
- ✨ 移动端适配 (Vant UI)
- ✨ 国际化支持
- ✨ 主题切换 (浅色/深色)

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证。

---

## 🙏 致谢

### 后端技术
- [FastAPI](https://fastapi.tiangolo.com/) - 优秀的 Python Web 框架
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL 工具包
- [Redis](https://redis.io/) - 高性能缓存数据库
- [Uvicorn](https://www.uvicorn.org/) - ASGI 服务器

### 前端技术
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Vant](https://vant-contrib.gitee.io/vant/) - 移动端 Vue 组件库
- [Vite](https://vitejs.dev/) - 下一代前端构建工具
- [Pinia](https://pinia.vuejs.org/) - Vue 状态管理库
- [Vue Router](https://router.vuejs.org/) - Vue 官方路由
- [Axios](https://axios-http.com/) - HTTP 客户端

---

**⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！**
