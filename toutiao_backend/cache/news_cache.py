# 新闻相关的缓存方法：新闻分类的读取和写入
from typing import Optional

from typing_extensions import Any

from config.cache_config import get_json_cache, set_cache

CATEGORIES_KEY = 'news:categories'
NEWS_LIST_PREFIX = 'news_list'

#获取新闻分类缓存
async def get_cache_categories():
    return await get_json_cache(CATEGORIES_KEY)


# 写入新闻分类缓存
# 分类、配置 7200；列表 600； 详情 1800; 验证码: 120 数据越持久，缓存越稳定
# 避免缓存雪崩，设置缓存的过期时间
async def set_cache_categories(data: list[dict[str: Any]], expire: int = 7200):
    return await set_cache(CATEGORIES_KEY, data, expire)

# 写入缓存 - 新闻列表 key = news_list:category_id:page_num:page_size
async def set_cache_news_list(category_id: Optional[int], page_num: int, page_size: int, data: list[dict[str: Any]], expire: int = 1800):
    # 调用封装的 Redis 的设置方法，存新闻列表到缓存中
    category_part = category_id if category_id else 'all'
    key = f'{NEWS_LIST_PREFIX}:{category_part}:{page_num}:{page_size}'
    return await set_cache(key, data, expire)

# 读取缓存-新闻列表
async def get_cache_news_list(category_id: Optional[int], page_num: int, page_size: int):
    category_part = category_id if category_id else 'all'
    return await get_json_cache(f'{NEWS_LIST_PREFIX}:{category_part}:{page_num}:{page_size}')