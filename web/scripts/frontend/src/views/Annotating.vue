<template>
  <div class="news">
    <h1>Annotating Page</h1>
    <el-table class="data-table" :data="tableData" stripe>
      <el-table-column prop="id" label="ID" width="80"></el-table-column>
      <el-table-column prop="created_at" label="Posted Date"></el-table-column>
      <el-table-column prop="og_site_name" label="サイト名"></el-table-column>
      <el-table-column prop="og_title" label="Title"></el-table-column>
      <el-table-column prop="og_description" label="text"></el-table-column>
      <el-table-column label="URL"  width="80">
        <template slot-scope="scope">
            <el-link :href="scope.row.url" target="_blank">link</el-link>
        </template>
      </el-table-column>
      <el-table-column label="カテゴリ">
        <template slot-scope="scope">
          <div v-for="(item, key) in scope.row.categories" :key="key">
            <el-checkbox v-model="scope.row.categories[key]" v-bind:label='key' v-on:change="checkUpdated(key, scope.row.id, scope.row.categories[key])" border size="mini"></el-checkbox>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <el-button type="primary" plain size="small" :loading="is_loading" :disabled="is_desabled" v-on:click="onClickLoadButton()">
          {{ is_loading ? 'Loading' : 'More' }}
    </el-button>
    <br>
  </div>
</template>

<script>

const axios = require('axios').create()
export default {
  name: 'annotate',
  data () {
    return {
      tableData: [],
      is_loading: false,
      is_desabled: false
    }
  },
  mounted () {
    this.updateTableData()
  },
  methods: {
    updateTableData: async function () {
      const response = await axios.get('api/news_data')
      this.tableData = response.data
    },
    checkUpdated: function (category, scrapeId, val) {
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
    },
    onClickLoadButton: async function () {
      this.is_loading = true

      const minScrapeId = this.tableData[this.tableData.length - 1].id
      var res = await axios.get('api/news_data?min_scrape_id=' + String(minScrapeId))

      if (res.data.length === 0) {
        this.is_desabled = true
      }
      this.tableData = this.tableData.concat(res.data)
      this.is_loading = false
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
