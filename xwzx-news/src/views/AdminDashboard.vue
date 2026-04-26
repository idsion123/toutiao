<template>
  <div class="admin-dashboard">
    <van-nav-bar title="后台管理" left-arrow @click-left="$router.back()" />
    
    <!-- 统计卡片 -->
    <div class="stats-container">
      <van-row gutter="10">
        <van-col span="12">
          <div class="stat-card user-card">
            <div class="stat-icon">
              <van-icon name="friends-o" size="40" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.users_count }}</div>
              <div class="stat-label">总用户数</div>
            </div>
          </div>
        </van-col>
        <van-col span="12">
          <div class="stat-card news-card">
            <div class="stat-icon">
              <van-icon name="newspaper-o" size="40" />
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.news_count }}</div>
              <div class="stat-label">总新闻数</div>
            </div>
          </div>
        </van-col>
      </van-row>
    </div>

    <!-- 最近新闻 -->
    <div class="recent-news">
      <van-cell-group title="最近发布的新闻" inset>
        <van-empty v-if="!stats.recent_news || stats.recent_news.length === 0" description="暂无新闻数据" />
        <van-cell
          v-for="news in stats.recent_news"
          :key="news.id"
          :title="news.title"
          :label="`作者: ${news.author} | 浏览: ${news.views}`"
          :value="formatTime(news.publish_time)"
          is-link
          @click="viewNewsDetail(news.id)"
        />
      </van-cell-group>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <van-grid :column-num="3" square>
        <van-grid-item icon="friends-o" text="用户管理" @click="goToUsers" />
        <van-grid-item icon="newspaper-o" text="新闻管理" @click="goToNews" />
        <van-grid-item icon="apps-o" text="分类管理" @click="goToCategories" />
      </van-grid>
    </div>

    <!-- 加载状态 -->
    <van-loading v-if="loading" type="spinner" size="24px" class="loading-overlay" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { dashboardApi } from '../api/admin'

const router = useRouter()
const loading = ref(false)
const stats = ref({
  users_count: 0,
  news_count: 0,
  recent_news: []
})

// 获取统计数据
const fetchStats = async () => {
  loading.value = true
  try {
    const res = await dashboardApi.getStats()
    if (res.code === 200) {
      stats.value = res.data
    } else {
      showToast(res.message || '获取数据失败')
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
    showToast('网络错误，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  return `${date.getMonth() + 1}/${date.getDate()} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 查看新闻详情
const viewNewsDetail = (newsId) => {
  router.push(`/news/detail/${newsId}`)
}

// 跳转到用户管理
const goToUsers = () => {
  router.push('/admin/users')
}

// 跳转到新闻管理
const goToNews = () => {
  router.push('/admin/news')
}

// 跳转到分类管理
const goToCategories = () => {
  router.push('/admin/categories')
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background-color: #f7f8fa;
  padding-bottom: 20px;
}

.stats-container {
  padding: 15px 10px;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.user-card {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

.news-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
}

.stat-icon {
  margin-right: 15px;
  opacity: 0.9;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.recent-news {
  margin-top: 15px;
}

.quick-actions {
  margin-top: 15px;
  padding: 0 10px;
}

.loading-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
}
</style>
