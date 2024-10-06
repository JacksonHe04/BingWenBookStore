<!--LayoutHeaderUI.vue-->
<script setup>
// 导入分类存储模块
import { useCategoryStore } from '@/stores/categoryStore'
// 创建分类存储的实例
const categoryStore = useCategoryStore()
</script>

<template>
  <!-- 导航栏列表 -->
  <ul class="app-header-nav">
    <!-- 首页导航项 -->
    <li class="home">
      <RouterLink to="/">首页</RouterLink>
    </li>
    <!-- 分类导航项，通过 v-for 指令遍历分类列表 -->
    <li class="home" v-for="item in categoryStore.categoryList" :key="item.id">
      <RouterLink active-class="active" :to="`/category/${item.id}`">
        {{ item.name }}
      </RouterLink>
    </li>


  </ul>
</template>



<style lang="scss">
.app-header-nav {
  width: 820px;
  display: flex;
  padding-left: 40px;
  position: relative;
  z-index: 998;

  li {
    margin-right: 40px;
    width: 38px;
    text-align: center;

    a {
      font-size: 16px;
      line-height: 32px;
      height: 32px;
      display: inline-block;

      &:hover {
        color: $xtxColor;
        border-bottom: 1px solid $xtxColor;
      }
    }

    .active {
      color: $xtxColor;
      border-bottom: 1px solid $xtxColor;
    }
  }
}
</style>