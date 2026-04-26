<template>
  <div class="admin-users">
    <van-nav-bar title="用户管理" left-arrow @click-left="$router.back()" />
    
    <!-- 搜索栏 -->
    <van-search
      v-model="searchKeyword"
      placeholder="搜索用户名、昵称或手机号"
      @search="handleSearch"
      @clear="handleClear"
    />
    
    <!-- 用户列表 -->
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="onLoad"
      >
        <van-cell-group inset v-for="user in userList" :key="user.id">
          <van-cell :title="user.nickname || user.username" :label="`ID: ${user.id} | ${user.phone}`">
            <template #icon>
              <van-image
                round
                width="40"
                height="40"
                :src="getFullAvatarUrl(user.avatar)"
                style="margin-right: 10px;"
              />
            </template>
            <template #right-icon>
              <van-tag :type="getGenderType(user.gender)" size="medium" style="margin-right: 8px;">
                性别：{{ getGenderText(user.gender) }}
              </van-tag>
              <van-button
                type="danger"
                size="mini"
                @click="handleDelete(user.id)"
              >
                删除
              </van-button>
            </template>
          </van-cell>
          <van-cell title="个人简介" :label="user.bio" />
          <van-cell title="注册时间" :label="user.created_at" />
        </van-cell-group>
        
        <van-empty v-if="!loading && userList.length === 0" description="暂无用户数据" />
      </van-list>
    </van-pull-refresh>
    
    <!-- 加载状态 -->
    <van-loading v-if="initialLoading" type="spinner" size="24px" class="loading-overlay" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { userApi } from '../api/admin'
import { apiConfig } from '../config/api'

const router = useRouter()
const loading = ref(false)
const refreshing = ref(false)
const initialLoading = ref(false)
const finished = ref(false)
const searchKeyword = ref('')
const userList = ref([])
const currentPage = ref(1)
const pageSize = 20

// 获取完整的头像 URL
const getFullAvatarUrl = (avatarPath) => {
  if (!avatarPath) return 'https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg'
  // 如果已经是完整 URL，直接返回
  if (avatarPath.startsWith('http')) return avatarPath
  // 否则拼接后端地址
  return `${apiConfig.baseURL}${avatarPath}`
}



// 获取用户列表
const fetchUsers = async (isRefresh = false) => {
  if (isRefresh) {
    currentPage.value = 1
    userList.value = []
    finished.value = false
  }
  
  try {
    console.log('请求参数:', { page: currentPage.value, limit: pageSize, keyword: searchKeyword.value })
    
    const res = await userApi.getList(currentPage.value, pageSize, searchKeyword.value || null)
    
    console.log('响应数据:', res)
    
    if (res.code === 200) {
      const newUsers = res.data.users
      console.log('用户数量:', newUsers.length, '总数:', res.data.total)
      
      userList.value = isRefresh ? newUsers : [...userList.value, ...newUsers]
      
      // 判断是否还有更多数据
      if (userList.value.length >= res.data.total) {
        finished.value = true
        console.log('已加载全部数据')
      } else {
        currentPage.value++
        console.log('下一页:', currentPage.value)
      }
    } else {
      showToast(res.message || '获取用户列表失败')
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
    showToast('网络错误，请稍后重试')
  } finally {
    // ✅ 关键：无论成功还是失败，都要关闭 loading 状态
    loading.value = false
    console.log('loading 状态:', loading.value, 'finished 状态:', finished.value, '列表长度:', userList.value.length)
  }
}

// 下拉加载（由 van-list 自动触发）
const onLoad = async () => {
  if (!finished.value && !refreshing.value) {
    await fetchUsers()
  }
}

// 下拉刷新
const onRefresh = async () => {
  await fetchUsers(true)
  refreshing.value = false
}

// 搜索
const handleSearch = () => {
  fetchUsers(true)
}

// 清除搜索
const handleClear = () => {
  searchKeyword.value = ''
  fetchUsers(true)
}

// 删除用户
const handleDelete = async (userId) => {
  try {
    await showConfirmDialog({
      title: '确认删除',
      message: '确定要删除该用户吗？此操作不可恢复！'
    })
    
    const res = await userApi.delete(userId)
    if (res.code === 200) {
      showToast('删除成功')
      fetchUsers(true)
    } else {
      showToast(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      showToast('删除失败')
    }
  }
}

// 获取性别文本
const getGenderText = (gender) => {
  const map = {
    'male': '男',
    'female': '女',
    'unknown': '未知'
  }
  return map[gender] || '未知'
}

// 获取性别标签类型
const getGenderType = (gender) => {
  const map = {
    'male': 'primary',
    'female': 'danger',
    'unknown': 'default'
  }
  return map[gender] || 'default'
}

onMounted(() => {
  // van-list 会在挂载后自动触发 onLoad，所以不需要手动调用
  // 只需要设置 initialLoading 为 true，等第一次加载完成后关闭
  initialLoading.value = true
  // 等待一小段时间，让 van-list 完成初始化
  setTimeout(() => {
    initialLoading.value = false
  }, 500)
})
</script>

<style scoped>
.admin-users {
  min-height: 100vh;
  background-color: #f7f8fa;
  padding-bottom: 20px;
}

.loading-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
}
</style>
