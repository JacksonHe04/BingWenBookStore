<script setup>
import HomePanel from './HomePanel.vue'
import { getAuthorAPI } from '@/apis/home'
import { onMounted, ref } from 'vue'
const authorList = ref([])
const getHotList = async () => {
  const res = await getAuthorAPI()
  authorList.value = res.result
}
onMounted(() => getHotList())


</script>

<template>
  <HomePanel title="热门作家" sub-title="文星璀璨 名家经典">
    <ul class="goods-list">
      <li v-for="item in authorList.slice(0, 4)" :key="item.id">
        <RouterLink to="/">
          <img v-img-lazy="item.picture" alt="">
          <p class="name">{{ item.author_name }}</p>
        </RouterLink>
      </li>
    </ul>
  </HomePanel>
</template>


<style scoped lang='scss'>
.goods-list {
  display: flex;
  justify-content: space-between;
  height: 426px;
  overflow-x: auto; // 添加水平滚动
  white-space: nowrap; // 防止子元素换行

  li {
    width: 306px;
    height: 406px;
    transition: all .5s;

    &:hover {
      transform: translate3d(0, -3px, 0);
      box-shadow: 0 3px 8px rgb(0 0 0 / 20%);
    }

    img {
      width: 306px;
      height: 306px;
    }

    p {
      font-size: 22px;
      padding-top: 12px;
      text-align: center;
    }

    .desc {
      color: #999;
      font-size: 18px;
    }
  }
}
</style>