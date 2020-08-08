<template>
  <div class="home">
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
        <template>
            <el-checkbox v-model="checked1" label="Option1" border></el-checkbox>
            <el-checkbox v-model="checked2" label="Option2" border></el-checkbox>
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
      tableData: []
    }
  },
  mounted () {
    this.updateTableData()
  },
  methods: {
    updateTableData: async function () {
      const response = await axios.get('api/test2')
      console.log(response)
      this.tableData = response.data
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
