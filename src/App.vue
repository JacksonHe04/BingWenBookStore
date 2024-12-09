<script setup>
</script>

<template>
  <!-- 一级路由出口组件 -->
  <RouterView />
</template>

<!-- 这个style标签定义了当前组件的样式，这些样式是私有的，仅在当前组件中生效 -->
<style scoped lang="scss">


/* 样式定义，使页眉的文本行高保持一致性，限制最大高度以适应视口 */
header {
  line-height: 1.5;
  max-height: 100vh;
}

/* 使logo在水平方向居中显示，并且与下方元素保持一定的间距 */
.logo {
  display: block;
  margin: 0 auto 2rem;
}

/* 导航栏设计，覆盖整个宽度，字体大小设置，居中对齐，且在顶部有一定边距 */
nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

/* 当导航链接为激活状态时，改变其文本颜色 */
nav a.router-link-exact-active {
  color: var(--color-text);
}

/* 当鼠标悬停在激活状态的导航链接上时，保持背景透明 */
nav a.router-link-exact-active:hover {
  background-color: transparent;
}

/* 导航链接样式，设置为行内块元素，有内边距和左边框 */
nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

/* 对首个导航链接不显示边框 */
nav a:first-of-type {
  border: 0;
}


// 当屏幕宽度至少为1024px时应用以下样式
@media (min-width: 1024px) {
  // 样式用于页面的头部区域
  header {
    /* 使用弹性盒子布局使头部内容在水平和垂直方向上居中 */
    display: flex;
    place-items: center;
    /* 右内边距设置为变量--section-gap的一半 */
    padding-right: calc(var(--section-gap) / 2);
  }

  // “.logo”类的样式
  .logo {
    /* 设置logo的右外边距，用于控制logo与其它内容的间距 */
    margin: 0 2rem 0 0;
  }

  // “header .wrapper”选择器用于header内的特定内容包装器
  header .wrapper {
    /* 使用弹性盒子布局，并将项目放置在起始位置，允许换行 */
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  // 导航栏的样式
  nav {
    /* 设置文本对齐方式为左对齐 */
    text-align: left;
    /* 减少左侧外边距，以调整导航栏的位置 */
    margin-left: -1rem;
    /* 设置字体大小 */
    font-size: 1rem;

    /* 设置上下内边距，增加导航栏的垂直空间 */
    padding: 1rem 0;
    /* 设置上边距，以调整导航栏与顶部的间距 */
    margin-top: 1rem;
  }
}
</style>