<template>
  <div class="search-results">
    <h2>搜索结果</h2>
    <div v-if="books.length === 0">没有找到相关书籍</div>
    <ul class="book-list">
      <li v-for="book in books" :key="book.id" class="book-item">
        <RouterLink :to="`/detail/${book.id}`">
          <img :src="book.picture" :alt="book.name" class="book-image" />
          <div class="book-info">
            <h3>{{ book.name }}</h3>
          </div>
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const books = ref([])

onMounted(() => {
  const searchResults = route.query.results
  console.log("searchResults: ", searchResults)
  if (searchResults) {
    try {
      books.value = JSON.parse(decodeURIComponent(searchResults))
    } catch (error) {
      console.error('解析搜索结果失败:', error)
      books.value = []
    }
  } else {
    console.warn('没有找到搜索结果')
    books.value = []
  }
})
</script>

<style scoped>
.search-results {
  padding: 20px 60px;
}

.book-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.book-item {
  display: flex;
  align-items: center;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 10px;
  transition: transform 0.2s;
  width: 250px; /* 固定宽度 */
}

.book-item:hover {
  transform: translateY(-5px);
}

.book-image {
  width: 100px;
  height: 150px;
  margin-right: 20px;
}

.book-info {
  flex: 1; /* 使书名区域占据剩余空间 */
}

.book-info h3 {
  margin: 0;
  white-space: nowrap; /* 防止文本换行 */
  overflow: hidden; /* 隐藏超出部分 */
  text-overflow: ellipsis; /* 显示省略号 */
}
</style>
