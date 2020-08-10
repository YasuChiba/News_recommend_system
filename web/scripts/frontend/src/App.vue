<template>
  <div id="app">
    <el-menu :default-active="activeIndex" mode="horizontal" router>
      <el-menu-item index="home" :route="{ name:'home' }">Home</el-menu-item>
      <el-menu-item index="annotate" :route="{ name:'annotate' }">Annotation</el-menu-item>
      <el-menu-item index="annotated_news" :route="{ name:'annotated_news' }">Annotated News</el-menu-item>
      <el-menu-item index="predicted_news" :route="{ name:'predicted_news' }">Predicted News</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      activeIndex: this.$route.name
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
a {
  text-decoration: none;
}
</style>
