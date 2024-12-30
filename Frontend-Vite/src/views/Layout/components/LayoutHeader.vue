<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LayoutHeaderUl from './LayoutHeaderUl.vue'
import HeaderCart from './HeaderCart.vue'
import { searchBooksAPI } from '@/apis/home'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = async () => {
  if (searchQuery.value.trim()) {
    try {
      const response = await searchBooksAPI(searchQuery.value)
      router.push({ path: '/search-results', query: { results: encodeURIComponent(JSON.stringify(response)) } })
    } catch (error) {
      console.error('搜索失败:', error)
    }
  } else {
    alert('请输入搜索关键词')
  }
}

</script>


<template>
  <header class='app-header'>
    <div class="container">
      <h1 class="logo">
        <RouterLink to="/">秉文书城</RouterLink>
      </h1>

      <LayoutHeaderUl />
      <div class="search">
        <i class="iconfont icon-search" @click="handleSearch"></i>
        <input type="text" v-model="searchQuery" placeholder="搜一搜">
      </div>
      <!-- 头部购物车 -->
      <HeaderCart />
    </div>
  </header>
</template>

<style scoped lang='scss'>
.app-header {
  background: #fff;

  .container {
    display: flex;
    align-items: center;
  }

  .logo {
    width: 200px;

    a {
      display: block;
      height: 110px;
      width: 100%;
      text-indent: -9999px;
      background: url('@/assets/images/logo.png') no-repeat center 18px / contain;
    }
  }

  .search {
    width: 180px;
    height: 32px;
    margin-left: 30px;
    position: relative;
    border-bottom: 1px solid #e7e7e7;
    line-height: 32px;

    .icon-search {
      font-size: 18px;
      margin-left: 5px;
      cursor: pointer; /* 添加鼠标指针样式 */
    }

    input {
      width: 140px;
      padding-left: 5px;
      color: #666;
    }
  }

  .cart {
    width: 50px;

    .curr {
      height: 32px;
      line-height: 32px;
      text-align: center;
      position: relative;
      display: block;

      .icon-cart {
        font-size: 22px;
      }

      em {
        font-style: normal;
        position: absolute;
        right: 0;
        top: 0;
        padding: 1px 6px;
        line-height: 1;
        background: $helpColor;
        color: #fff;
        font-size: 12px;
        border-radius: 10px;
        font-family: Arial;
      }
    }
  }
}
</style>
