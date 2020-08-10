<template>
  <div class="home">
    <h2>カテゴリ</h2>

    <el-table class="data-table" :data="categories" stripe>
            <el-table-column prop="category_id" label="id"></el-table-column>
            <el-table-column prop="category_name" label="カテゴリ名"></el-table-column>
            <el-table-column label="削除">
              <template slot-scope="scope">
                  <el-button type="danger" plain size="small" v-on:click="deleteCategory(scope.row.category_id)">削除</el-button>
              </template>
            </el-table-column>
    </el-table>
    <br>
    <h2>カテゴリ追加</h2>
    <el-input class="add_category_input" placeholder="category name" v-model="adding_category_name"></el-input>
    <el-button type="primary" plain size="small" :disabled="is_disabled_add_category_button" v-on:click="onClickAddCategiryButton()">追加</el-button>
  </div>
</template>

<script>

const axios = require('axios').create()
export default {
  name: 'home',
  data () {
    return {
      categories: [],
      adding_category_name: '',
      is_disabled_add_category_button: false
    }
  },
  mounted () {
    this.updateTableData()
  },
  methods: {
    updateTableData: async function () {
      const response = await axios.get('api/categories')
      this.categories = response.data
    },
    deleteCategory: async function (categoryId) {
      console.log(categoryId)
      this.is_disabled_add_category_button = true
      const response = await axios.get('api/delete_cateogry?category_id=' + categoryId)
      this.categories = response.data
      this.is_disabled_add_category_button = false
    },
    onClickAddCategiryButton: async function () {
      this.is_disabled_add_category_button = true

      var categoryName = this.adding_category_name
      console.log(categoryName)
      if (!categoryName.length) {
        return
      }
      const response = await axios.get('api/add_cateogry?category_name=' + categoryName)

      this.categories = response.data
      this.is_disabled_add_category_button = false
    }
  }
}
</script>

<style scoped>
.data-table {
  width: 80%;
  margin: auto;
}
.add_category_input {
  width: 20%;
  margin: auto;
}
</style>
