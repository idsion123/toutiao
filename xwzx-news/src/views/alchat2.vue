<template>
  <div class="ai-chat-container">
    <van-nav-bar title="AI问答" fixed>
      <template #left>
        <van-icon name="bars" @click="toggleHistory" />
      </template>
      <template #right>
        <van-badge :content="unreadCount" :show-zero="false" v-if="unreadCount > 0">
          <van-icon name="clock-o" @click="toggleHistory" />
        </van-badge>
      </template>
    </van-nav-bar>
    
    <!-- 历史记录侧边栏 -->
    <transition name="slide">
      <div v-show="showHistory" class="history-sidebar">
        <div class="history-header">
          <h3>聊天历史</h3>
          <div class="header-actions">
            <van-icon name="refresh" @click="loadHistory" title="刷新" />
            <van-icon name="delete-o" @click="showClearConfirm" title="清空全部" />
            <van-icon name="cross" @click="toggleHistory" title="关闭" />
          </div>
        </div>
        
        <div class="history-list" ref="historyListRef">
          <van-empty v-if="!loading && historyList.length === 0" description="暂无聊天记录" />
          
          <van-list
            v-else
            v-model:loading="loading"
            :finished="finished"
            finished-text="没有更多了"
            @load="onLoadHistory"
          >
            <div 
              v-for="item in historyList" 
              :key="item.id" 
              class="history-item"
              :class="{ active: currentRecordId === item.id }"
              @click="loadChatFromHistory(item)"
            >
              <div class="item-content">
                <div class="item-message">{{ truncateText(item.message, 50) }}</div>
                <div class="item-time">{{ formatTime(item.created_at) }}</div>
              </div>
              <van-icon 
                name="delete-o" 
                class="delete-btn" 
                @click="confirmDeleteHistory(item.id)"
              />
            </div>
          </van-list>
        </div>
      </div>
    </transition>
    
    <!-- 遮罩层 -->
    <transition name="fade">
      <div v-show="showHistory" class="overlay" @click="toggleHistory"></div>
    </transition>
    
    <div class="chat-content">
      <div class="messages-container" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index" 
          :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
        >
          <div class="message-content">
            <div v-if="message.role === 'assistant' && message.content === ''" class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <div v-else v-html="formatMessage(message.content)"></div>
          </div>
        </div>
      </div>
      
      <div class="input-container">
        <van-field
          v-model="userInput"
          rows="1"
          autosize
          type="textarea"
          placeholder="请输入问题..."
          class="chat-input"
          @keypress.enter.prevent="sendMessage"
        />
        <van-button 
          type="primary" 
          class="send-button" 
          :disabled="isLoading || !userInput.trim()" 
          @click="sendMessage"
        >
          发送
        </van-button>
      </div>
    </div>
    
    <!-- 删除确认对话框 -->
    <van-dialog
      v-model:show="showDeleteDialog"
      title="确认删除"
      show-cancel-button
      @confirm="handleDeleteHistory"
    >
      确定要删除这条聊天记录吗？
    </van-dialog>
    
    <!-- 清空确认对话框 -->
    <van-dialog
      v-model:show="showClearDialog"
      title="确认清空"
      show-cancel-button
      button-color="#ee0a24"
      @confirm="handleClearAllHistory"
    >
      确定要清空所有聊天记录吗？此操作不可恢复！
    </van-dialog>
    
    <tab-bar />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import TabBar from '../components/TabBar.vue';
import { showToast, showLoadingToast, closeToast } from 'vant';
import * as marked from 'marked';
import DOMPurify from 'dompurify';
import axios from 'axios';
import { apiConfig } from '../config/api';
import { useUserStore } from '../store/user'

// 聊天消息
const messages = ref([
  { role: 'assistant', content: '你好！我是AI助手，有什么可以帮助你的吗？' }
]);
const userInput = ref('');
const messagesContainer = ref(null);
const isLoading = ref(false);
const userStore = useUserStore()

// 历史记录相关
const showHistory = ref(false);
const historyList = ref([]);
const loading = ref(false);
const finished = ref(false);
const currentPage = ref(1);
const pageSize = 20;
const currentRecordId = ref(null);
const historyListRef = ref(null);

// 对话框状态
const showDeleteDialog = ref(false);
const showClearDialog = ref(false);
const deleteRecordId = ref(null);

// 未读数量（可选）
const unreadCount = ref(0);

// 格式化消息内容（支持Markdown）
const formatMessage = (content) => {
  if (!content) return '';
  return DOMPurify.sanitize(marked.parse(content));
};

// 切换历史记录面板
const toggleHistory = () => {
  showHistory.value = !showHistory.value;
  if (showHistory.value && historyList.value.length === 0) {
    loadHistory();
  }
};

// 加载历史记录
const loadHistory = async () => {
  currentPage.value = 1;
  finished.value = false;
  historyList.value = [];
  await onLoadHistory();
};

// 分页加载历史记录
const onLoadHistory = async () => {
  try {
    const token = localStorage.getItem('token');
    const response = await axios.get(`${apiConfig.baseURL}/api/ai/history`, {
      params: {
        limit: pageSize,
        offset: (currentPage.value - 1) * pageSize
      },
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = response.data.data;
    const newRecords = data.records || [];
    
    if (currentPage.value === 1) {
      historyList.value = newRecords;
    } else {
      historyList.value = [...historyList.value, ...newRecords];
    }
    
    // 判断是否还有更多数据
    if (historyList.value.length >= data.total) {
      finished.value = true;
    } else {
      currentPage.value++;
    }
    
    loading.value = false;
    
  } catch (error) {
    console.error('获取历史记录失败:', error);
    showToast('获取历史记录失败');
    loading.value = false;
    finished.value = true;
  }
};

// 从历史记录加载对话
const loadChatFromHistory = (record) => {
  // 设置当前记录 ID
  currentRecordId.value = record.id;
  
  // 加载对话内容
  messages.value = [
    { role: 'user', content: record.message },
    { role: 'assistant', content: record.response }
  ];
  
  // 关闭侧边栏
  showHistory.value = false;
  
  // 滚动到底部
  nextTick(() => {
    scrollToBottom();
  });
  
  showToast('已加载历史对话');
};

// 确认删除单条记录
const confirmDeleteHistory = (id) => {
  deleteRecordId.value = id;
  showDeleteDialog.value = true;
};

// 执行删除
const handleDeleteHistory = async () => {
  if (!deleteRecordId.value) return;
  
  showLoadingToast({
    message: '删除中...',
    forbidClick: true,
    duration: 0
  });
  
  try {
    const token = localStorage.getItem('token');
    await axios.delete(
      `${apiConfig.baseURL}/api/ai/history/${deleteRecordId.value}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    closeToast();
    showToast('删除成功');
    
    // 从列表中移除
    historyList.value = historyList.value.filter(
      item => item.id !== deleteRecordId.value
    );
    
    // 如果删除的是当前正在查看的记录，清空聊天
    if (currentRecordId.value === deleteRecordId.value) {
      messages.value = [
        { role: 'assistant', content: '你好！我是AI助手，有什么可以帮助你的吗？' }
      ];
      currentRecordId.value = null;
    }
    
  } catch (error) {
    closeToast();
    console.error('删除失败:', error);
    showToast(error.response?.data?.detail || '删除失败');
  }
};

// 显示清空确认
const showClearConfirm = () => {
  if (historyList.value.length === 0) {
    showToast('暂无聊天记录');
    return;
  }
  showClearDialog.value = true;
};

// 清空所有记录
const handleClearAllHistory = async () => {
  showLoadingToast({
    message: '清空中...',
    forbidClick: true,
    duration: 0
  });
  
  try {
    const token = localStorage.getItem('token');
    await axios.delete(
      `${apiConfig.baseURL}/api/ai/history/clear`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    
    closeToast();
    showToast('已清空所有记录');
    
    // 重置列表
    historyList.value = [];
    finished.value = true;
    currentPage.value = 1;
    currentRecordId.value = null;
    
    // 清空当前聊天
    messages.value = [
      { role: 'assistant', content: '你好！我是AI助手，有什么可以帮助你的吗？' }
    ];
    
  } catch (error) {
    closeToast();
    console.error('清空失败:', error);
    showToast(error.response?.data?.detail || '清空失败');
  }
};

// 格式化时间
const formatTime = (timeStr) => {
  const date = new Date(timeStr);
  const now = new Date();
  const diff = now - date;
  
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);
  
  if (minutes < 1) return '刚刚';
  if (minutes < 60) return `${minutes}分钟前`;
  if (hours < 24) return `${hours}小时前`;
  if (days < 7) return `${days}天前`;
  
  return date.toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  });
};

// 截断文本
const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

// 发送消息
const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return;
  
  // 添加用户消息
  const userMessage = userInput.value.trim();
  messages.value.push({ role: 'user', content: userMessage });
  userInput.value = '';
  
  // 添加AI消息占位
  messages.value.push({ role: 'assistant', content: '' });
  
  // 清除当前记录 ID（因为是新对话）
  currentRecordId.value = null;
  
  // 滚动到底部
  await nextTick();
  scrollToBottom();
  
  // 发送请求
  isLoading.value = true;
  try {
    await fetchAIResponse(userMessage);
  } catch (error) {
    console.error('Error fetching AI response:', error);
    messages.value[messages.value.length - 1].content = `发生错误: ${error.message || '请检查网络连接和API设置'}`;
  } finally {
    isLoading.value = false;
    await nextTick();
    scrollToBottom();
  }
};

// 获取AI响应（使用SSE）
const fetchAIResponse = async (userMessage) => {
  try {
    const response = await fetch(`${apiConfig.baseURL}/api/ai/chat`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userStore.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage,
        model: 'qwen3-max-preview'
      })
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const text = decoder.decode(value, { stream: true });
      buffer += text;
      
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      
      for (const line of lines) {
        const trimmedLine = line.trim();
        if (!trimmedLine || !trimmedLine.startsWith('data: ')) {
          continue;
        }
        
        const dataStr = trimmedLine.slice(6);
        
        try {
          const data = JSON.parse(dataStr);
          
          if (data.error) {
            messages.value[messages.value.length - 1].content = `发生错误: ${data.error}`;
            showToast(data.error);
            return;
          }
          
          if (data.done) {
            if (data.record_id) {
              currentRecordId.value = data.record_id;
              console.log('聊天记录ID:', data.record_id);
            }
            return;
          }
          
          if (data.content) {
            messages.value[messages.value.length - 1].content += data.content;
            await nextTick();
            scrollToBottom();
          }
          
        } catch (e) {
          console.warn('解析 SSE 数据失败:', e, dataStr);
        }
      }
    }
    
    if (!messages.value[messages.value.length - 1].content) {
      messages.value[messages.value.length - 1].content = '抱歉，我无法生成回复。请稍后再试。';
    }
    
  } catch (error) {
    console.error('Error fetching AI response:', error);
    const errorMsg = error.message || '请检查网络连接';
    messages.value[messages.value.length - 1].content = `发生错误: ${errorMsg}`;
    showToast(errorMsg);
  }
};

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 监听消息变化，自动滚动
watch(messages, () => {
  nextTick(scrollToBottom);
}, { deep: true });

// 组件挂载时滚动到底部
onMounted(() => {
  scrollToBottom();
});
</script>

<style scoped>
.ai-chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  padding-top: 46px;
  padding-bottom: 50px;
  box-sizing: border-box;
  position: relative;
}

/* 历史记录侧边栏 */
.history-sidebar {
  position: fixed;
  left: 0;
  top: 46px;
  bottom: 50px;
  width: 300px;
  background: white;
  z-index: 1000;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.history-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.header-actions .van-icon {
  font-size: 20px;
  color: #666;
  cursor: pointer;
  padding: 4px;
}

.header-actions .van-icon:hover {
  color: #1989fa;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  margin-bottom: 8px;
  background: #f7f8fa;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.history-item:hover {
  background: #e8f4ff;
}

.history-item.active {
  background: #e8f4ff;
  border-left: 3px solid #1989fa;
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-message {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-time {
  font-size: 12px;
  color: #999;
}

.delete-btn {
  font-size: 18px;
  color: #ee0a24;
  padding: 8px;
  flex-shrink: 0;
}

.delete-btn:hover {
  background: #fff1f0;
  border-radius: 4px;
}

/* 遮罩层 */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 999;
}

/* 动画 */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.message {
  margin-bottom: 10px;
  max-width: 80%;
}

.user-message {
  margin-left: auto;
}

.ai-message {
  margin-right: auto;
}

.message-content {
  padding: 10px;
  border-radius: 10px;
  word-break: break-word;
}

.user-message .message-content {
  background-color: #007aff;
  color: white;
}

.ai-message .message-content {
  background-color: #f2f2f2;
  color: #333;
}

.input-container {
  display: flex;
  padding: 10px;
  border-top: 1px solid #eee;
  background-color: #fff;
}

.chat-input {
  flex: 1;
  margin-right: 10px;
}

.send-button {
  align-self: flex-end;
}

.typing-indicator {
  display: flex;
  padding: 5px;
}

.typing-indicator span {
  height: 8px;
  width: 8px;
  background-color: #999;
  border-radius: 50%;
  margin: 0 2px;
  display: inline-block;
  animation: bounce 1.5s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-5px);
  }
}

:deep(pre) {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

:deep(code) {
  font-family: monospace;
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 4px;
}

:deep(p) {
  margin: 8px 0;
}

:deep(ul), :deep(ol) {
  padding-left: 20px;
}

:deep(a) {
  color: #1989fa;
  text-decoration: none;
}
</style>
