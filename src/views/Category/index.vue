<script setup>
import GoodsItem from "../Home/components/GoodsItem.vue";
import { computed } from "vue";
import { useBanner } from "./composables/useBanner";
import { useCategory } from "./composables/useCategory";

const { bannerList } = useBanner();
const { categoryData } = useCategory();

// 计算属性，筛选出 categoryName 和 categoryData.name 相同的 banner
const filteredBannerList = computed(() => {
  return bannerList.value.filter(
    (banner) => banner.categoryName === categoryData.value.name,
  );
});
</script>

<template>
  <div class="top-category">
    <div class="container m-top-20">
      <!-- 面包屑 -->
      <div class="bread-container">
        <el-breadcrumb separator=">">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item>{{ categoryData.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </div>
      <!-- 轮播图 -->
      <div class="home-banner">
        <el-carousel height="500px">
          <el-carousel-item v-for="item in filteredBannerList" :key="item.id">
            <RouterLink :to="`/detail/${item.id}`">
              <img :src="item.imgUrl" alt="" />
            </RouterLink>
          </el-carousel-item>
        </el-carousel>
      </div>
      <!-- 二级分类 -->
      <div class="sub-list">
        <h3>全部分类</h3>
        <ul>
          <li v-for="i in categoryData.children" :key="i.id">
            <RouterLink :to="`/category/sub/${i.id}`">
              <img :src="i.picture" />
              <p>{{ i.name }}</p>
            </RouterLink>
          </li>
        </ul>
      </div>
      <!-- 二级分类的商品 -->
      <div
        class="ref-goods"
        v-for="item in categoryData.children"
        :key="item.id"
      >
        <div class="head">
          <h3>- {{ item.name }}-</h3>
        </div>
        <div class="body">
          <GoodsItem v-for="good in item.goods" :goods="good" :key="good.id" />
        </div>
      </div>
      <!-- 当前分类所有二级分类的商品汇总 -->
      <div class="ref-goods">
        <div class="head">
          <h3>- {{ categoryData.name }} 全部商品-</h3>
        </div>
        <div class="all-goods">
          <div
            class="ref-goods all-goods"
            v-for="item in categoryData.children"
            :key="item.id"
          >
            <GoodsItem
              v-for="good in item.goods"
              :goods="good"
              :key="good.id"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.top-category {
  h3 {
    font-size: 28px;
    color: #666;
    font-weight: normal;
    text-align: center;
    line-height: 100px;
  }

  .sub-list {
    margin-top: 20px;
    background-color: #fff;

    ul {
      display: flex;
      padding: 0 32px;
      flex-wrap: wrap;

      li {
        width: 168px;
        height: 160px;

        a {
          text-align: center;
          display: block;
          font-size: 16px;

          img {
            width: 100px;
            height: 100px;
          }

          p {
            line-height: 40px;
          }

          &:hover {
            color: $theme;
          }
        }
      }
    }
  }

  .ref-goods {
    background-color: #fff;
    margin-top: 20px;
    position: relative;

    .head {
      .xtx-more {
        position: absolute;
        top: 20px;
        right: 20px;
      }

      .tag {
        text-align: center;
        color: #999;
        font-size: 20px;
        position: relative;
        top: -20px;
      }
    }

    .body {
      display: flex;
      justify-content: space-around;
      padding: 0 40px 30px;
      overflow-x: auto; // 添加水平滚动
      white-space: nowrap; // 防止子元素换行
      flex-wrap: nowrap;
    }
  }
}

.bread-container {
  padding: 25px 0;
}

.home-banner {
  width: 1240px;
  height: 500px;
  margin: 0 auto;
  background-color: #fff;

  img {
    height: 100%;
    width: auto; // 让宽度自适应
    object-fit: cover; // 防止图片拉伸
    display: block; // 将图片设置为块级元素以便使用 margin 居中
    margin: 0 auto; // 水平居中
  }
}

.body {
  display: flex;
  justify-content: space-around;
  padding: 0 40px 30px;
  overflow-x: auto; // 添加水平滚动
  white-space: wrap;
  flex-wrap: wrap;
}

.all-goods {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  flex-direction: row-reverse;
}
</style>
