<template>
  <div class="admin-news">
    <van-nav-bar title="新闻管理" left-arrow @click-left="$router.back()" />
    
    <!-- 搜索和筛选 -->
    <div class="filter-bar">
      <van-search
        v-model="searchKeyword"
        placeholder="搜索标题或作者"
        shape="round"
        @search="handleSearch"
      />
      <van-dropdown-menu style="padding: 0 16px;">
        <van-dropdown-item v-model="selectedCategory" :options="categoryOptions" @change="handleCategoryChange" />
      </van-dropdown-menu>
    </div>
    
    <!-- 新闻列表 -->
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
      >
        <van-card
          v-for="news in newsList"
          :key="news.id"
          :title="news.title"
          :desc="news.description || '暂无简介'"
          :thumb="getFullImageUrl(news.image)"
          class="news-card"
        >
          <template #tags>
            <van-tag plain type="primary" style="margin-right: 5px;">{{ getCategoryName(news.category_id) }}</van-tag>
            <van-tag type="success">{{ news.views }} 浏览</van-tag>
          </template>
          <template #footer>
            <div class="news-footer">
              <span class="news-author">作者: {{ news.author || '未知' }}</span>
              <span class="news-time">{{ formatTime(news.publish_time) }}</span>
            </div>
            <div class="news-actions">
              <van-button size="small" type="primary" @click="handleEdit(news.id)">编辑</van-button>
              <van-button size="small" type="danger" @click="handleDelete(news.id)">删除</van-button>
            </div>
          </template>
        </van-card>
      </van-list>
      
      <!-- 空状态 - 移到 van-list 外部 -->
      <van-empty v-if="!loading && newsList.length === 0" description="暂无新闻数据" />
    </van-pull-refresh>
    
    <!-- 加载状态 -->
    <van-loading v-if="initialLoading" type="spinner" size="24px" class="loading-overlay" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { newsApi, categoryApi } from '../api/admin'
import { apiConfig } from '../config/api'

const router = useRouter()
const loading = ref(false)
const refreshing = ref(false)
const initialLoading = ref(false)
const finished = ref(false)
const searchKeyword = ref('')
const selectedCategory = ref('')
const newsList = ref([])
const categories = ref([])
const currentPage = ref(1)
const pageSize = 20

// 获取完整的图片 URL
const getFullImageUrl = (imagePath) => {
  if (!imagePath) return 'https://fastly.jsdelivr.net/npm/@vant/assets/ipad.jpeg'
  // 如果已经是完整 URL，直接返回
  if (imagePath.startsWith('http')) return imagePath
  // 否则拼接后端地址
  return `${apiConfig.baseURL}${imagePath}`
}

// 分类选项
const categoryOptions = ref([{ text: '全部分类', value: '' }])

// 获取分类列表
const fetchCategories = async () => {
  try {
    const res = await categoryApi.getList()
    if (res.code === 200) {
      categories.value = res.data.categories
      categoryOptions.value = [
        { text: '全部分类', value: '' },
        ...res.data.categories.map(cat => ({
          text: cat.name,
          value: cat.id
        }))
      ]
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
  }
}

// 获取新闻列表
const fetchNews = async (isRefresh = false) => {
  if (isRefresh) {
    currentPage.value = 1
    newsList.value = []
    finished.value = false
  }
  
  
  try {
    const categoryId = selectedCategory.value || null
    
    const res = await newsApi.getList(
      currentPage.value,
      pageSize,
      searchKeyword.value || null,
      categoryId
    )
    
    if (res.code === 200) {
      const newNews = res.data.news
      console.log(newNews)
      
      // 追加或替换数据
      newsList.value = isRefresh ? newNews : [...newsList.value, ...newNews]
      
      // 判断是否还有更多数据
      if (newsList.value.length >= res.data.total || newNews.length < pageSize) {
        finished.value = true
      } else {
        currentPage.value++
      }
    } else {
      showToast(res.message || '获取新闻列表失败')
      finished.value = true
    }
  } catch (error) {
    console.error('获取新闻列表失败:', error)
    showToast('网络错误，请稍后重试')
    finished.value = true
  } finally {
    // ✅ 关键：无论成功还是失败，都要关闭 loading 状态
    loading.value = false
  }
}

// 下拉加载（由 van-list 自动触发）
const onLoad = async () => {
  if (!finished.value && !refreshing.value) {
    await fetchNews()
  }
}

// 下拉刷新
const onRefresh = async () => {
    await fetchNews(true)
    refreshing.value = false
}

// 搜索
const handleSearch = () => {
  fetchNews(true)
}

// 分类变化
const handleCategoryChange = () => {
  fetchNews(true)
}

// 编辑新闻
const handleEdit = (newsId) => {
  showToast('编辑功能开发中...')
  // router.push(`/admin/news/edit/${newsId}`)
}

// 删除新闻
const handleDelete = async (newsId) => {
  try {
    await showConfirmDialog({
      title: '确认删除',
      message: '确定要删除该新闻吗？此操作不可恢复！'
    })
    
    const res = await newsApi.delete(newsId)
    if (res.code === 200) {
      showToast('删除成功')
      fetchNews(true)
    } else {
      showToast(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除新闻失败:', error)
      showToast('删除失败')
    }
  }
}

// 获取分类名称
const getCategoryName = (categoryId) => {
  const category = categories.value.find(cat => cat.id === categoryId)
  return category ? category.name : `分类${categoryId}`
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

onMounted(async () => {
  // van-list 会在挂载后自动触发 onLoad，所以不需要手动调用
  // 只需要设置 initialLoading 为 true，等第一次加载完成后关闭
  initialLoading.value = true
  
  // ✅ 获取分类列表
  await fetchCategories()
  
  // 等待一小段时间，让 van-list 完成初始化
  setTimeout(() => {
    initialLoading.value = false
  }, 500)
})
</script>

<style scoped>
.admin-news {
  min-height: 100vh;
  background-color: #f7f8fa;
  padding-bottom: 20px;
}

.filter-bar {
  background: white;
  padding: 10px 0;
}

.news-card {
  margin: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.news-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 12px;
  color: #969799;
}

.news-author {
  flex: 1;
}

.news-time {
  flex-shrink: 0;
}

.news-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.loading-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
}
</style>
