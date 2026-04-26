from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/news_app?charset=utf8mb4"

async_engine = create_async_engine(ASYNC_DATABASE_URL, 
                                   echo=True, # 可选，用于调试时查看SQL语句执行
                                   pool_size=10, # 连接池大小
                                   max_overflow=20 # 最大溢出连接数
                                   )


# 2. 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, # 绑定数据库引擎
    class_=AsyncSession, # 使用异步会话类
    expire_on_commit=False, #提交后不自动过期会话，不会重新查询数据库
    )


# 依赖项，用于获取数据库会话
async def get_db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session # 返回会话对象
            await session.commit() # 提交事务
        except Exception as e:
            await session.rollback() # 回滚事务
            raise e
        finally:
            await session.close() # 关闭会话
       