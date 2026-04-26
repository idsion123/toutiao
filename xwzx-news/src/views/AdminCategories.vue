<template>
  <div class="admin-categories">
    <van-nav-bar title="分类管理" left-arrow @click-left="$router.back()">
      <template #right>
        <van-button size="small" type="primary" @click="showAddDialog">
          <van-icon name="plus" /> 添加
        </van-button>
      </template>
    </van-nav-bar>
    
    <!-- 分类列表 -->
    <van-pull-refresh v-model="refreshing" @refresh="onRefresh">
      <van-list :finished="true">
        <van-swipe-cell v-for="category in categoryList" :key="category.id">
          <van-cell :title="category.name" :label="`排序: ${category.sort_order}`">
            <template #icon>
              <van-icon name="apps-o" size="20" style="margin-right: 10px; color: #1989fa;" />
            </template>
            <template #right-icon>
              <van-tag type="primary">{{ category.id }}</van-tag>
            </template>
          </van-cell>
          
          <template #right>
            <van-button square type="primary" text="编辑" @click="handleEdit(category)" />
            <van-button square type="danger" text="删除" @click="handleDelete(category.id)" />
          </template>
        </van-swipe-cell>
        
        <van-empty v-if="categoryList.length === 0" description="暂无分类数据" />
      </van-list>
    </van-pull-refresh>
    
    <!-- 添加/编辑对话框 -->
    <van-dialog
      v-model:show="dialogVisible"
      :title="isEdit ? '编辑分类' : '添加分类'"
      show-cancel-button
      @confirm="handleSubmit"
    >
      <van-form @submit="handleSubmit">
        <van-cell-group inset>
          <van-field
            v-model="formData.name"
            name="name"
            label="分类名称"
            placeholder="请输入分类名称"
            :rules="[{ required: true, message: '请输入分类名称' }]"
          />
          <van-field
            v-model.number="formData.sort_order"
            name="sort_order"
            type="number"
            label="排序"
            placeholder="数字越小越靠前"
          />
        </van-cell-group>
      </van-form>
    </van-dialog>
    
    <!-- 加载状态 -->
    <van-loading v-if="loading" type="spinner" size="24px" class="loading-overlay" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast, showConfirmDialog } from 'vant'
import { categoryApi } from '../api/admin'

const router = useRouter()
const loading = ref(false)
const refreshing = ref(false)
const categoryList = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const currentCategory = ref(null)
const formData = ref({
  name: '',
  sort_order: 0
})

// 获取分类列表
const fetchCategories = async () => {
  loading.value = true
  try {
    const res = await categoryApi.getList()
    if (res.code === 200) {
      categoryList.value = res.data.categories
    } else {
      showToast(res.message || '获取分类列表失败')
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
    showToast('网络错误，请稍后重试')
  } finally {
    loading.value = false
    refreshing.value = false
  }
}

// 下拉刷新
const onRefresh = async () => {
  await fetchCategories()
}

// 显示添加对话框
const showAddDialog = () => {
  isEdit.value = false
  currentCategory.value = null
  formData.value = {
    name: '',
    sort_order: 0
  }
  dialogVisible.value = true
}

// 编辑分类
const handleEdit = (category) => {
  isEdit.value = true
  currentCategory.value = category
  formData.value = {
    name: category.name,
    sort_order: category.sort_order
  }
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formData.value.name) {
    showToast('请输入分类名称')
    return false
  }
  
  try {
    let res
    if (isEdit.value) {
      // 更新分类
      res = await categoryApi.update(
        currentCategory.value.id,
        formData.value.name,
        formData.value.sort_order
      )
    } else {
      // 创建分类
      res = await categoryApi.create(
        formData.value.name,
        formData.value.sort_order
      )
    }
    
    if (res.code === 200) {
      showToast(isEdit.value ? '更新成功' : '添加成功')
      dialogVisible.value = false
      fetchCategories()
    } else {
      showToast(res.message || '操作失败')
    }
  } catch (error) {
    console.error('操作失败:', error)
    showToast('操作失败')
  }
  
  return false // 阻止默认关闭
}

// 删除分类
const handleDelete = async (categoryId) => {
  try {
    await showConfirmDialog({
      title: '确认删除',
      message: '确定要删除该分类吗？如果分类下有新闻则无法删除。'
    })
    
    const res = await categoryApi.delete(categoryId)
    if (res.code === 200) {
      showToast('删除成功')
      fetchCategories()
    } else {
      showToast(res.message || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除分类失败:', error)
      if (error.response?.data?.detail) {
        showToast(error.response.data.detail)
      } else {
        showToast('删除失败')
      }
    }
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.admin-categories {
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
