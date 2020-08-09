<template>
  <div class="news">
    <h1>News List</h1>
    <div v-for="item in categories" :key="item.category_id">
        <div>
            <h2>
            カテゴリー: {{ item.category_name }}
            </h2>
        </div>
        <el-table class="data-table" :data="news_by_categories[item.category_id]" stripe>
            <el-table-column prop="id" label="ID" width="100"></el-table-column>
            <el-table-column prop="og_site_name" label="サイト名" width="140"></el-table-column>
            <el-table-column prop="og_title" label="Title"></el-table-column>
            <el-table-column prop="og_description" label="text"></el-table-column>
        </el-table>
    </div>
  </div>
</template>

<script>

const axios = require('axios').create()
export default {
  name: 'news',
  data () {
    return {
      categories: [],
      news_by_categories: {}
    }
  },
  mounted () {
    this.updateTableData()
  },
  methods: {
    updateTableData: async function () {
      const response = await axios.get('api/categories')
      this.categories = response.data
      for (var key in this.categories) {
        var tmp = this.categories[key]
        var res = await axios.get('api/news_data/category?category_id=' + tmp.category_id)
        this.$set(this.news_by_categories, tmp.category_id, res.data)
      }
    }
  }
}
</script>

<style scoped>
.data-table {
  width: 80%;
  margin: auto;
}
.categor-title {
  font-weight:bold;
  font-size: 30px;
}
</style>
