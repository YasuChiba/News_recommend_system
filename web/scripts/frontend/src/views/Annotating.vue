<template>
  <div class="news">
    <h1>This is a annotating page</h1>
    <el-table class="data-table" :data="tableData" stripe>
      <el-table-column prop="id" label="ID" width="100"></el-table-column>
      <el-table-column prop="og_site_name" label="サイト名" width="140"></el-table-column>
      <el-table-column prop="og_title" label="Title"></el-table-column>
      <el-table-column prop="og_description" label="text"></el-table-column>
      <el-table-column label="URL">
        <template slot-scope="scope">
            <el-link :href="scope.row.url" target="_blank">link</el-link>
        </template>
      </el-table-column>
      <el-table-column label="カテゴリ">
        <template slot-scope="scope">
          <div v-for="(item, key) in scope.row.categories" :key="key">
            <el-checkbox v-model="scope.row.categories[key]" v-bind:label='key' v-on:change="checkUpdate(key, scope.row.id, scope.row.categories[key])" border size="mini"></el-checkbox>
          </div>
        </template>
      </el-table-column>

    </el-table>
  </div>
</template>

<script>

const axios = require('axios').create()
export default {
  name: 'annotate',
  data () {
    return {
      tableData: [],
      checkboxGroup2: ['Option1', 'Option2']
    }
  },
  mounted () {
    this.updateTableData()
  },
  methods: {
    updateTableData: async function () {
      const response = await axios.get('api/news_data')
      this.tableData = response.data.reverse()
      console.log(this.tableData[0].categories)
    },
    checkUpdate: function (category, scrapeId, val) {
      console.log(category)
      console.log(val)
      console.log(scrapeId)
      axios.post('api/annotation', {
        is_delete: val ? 'false' : 'true',
        scrape_id: scrapeId,
        category: category
      }, {
        headers: {
          'Content-Type': 'application/json',
          charset: 'utf-8'
        }
      })
    }
  }
}
</script>

<style scoped>
.data-table {
  width: 80%;
  margin: auto;
}
</style>
