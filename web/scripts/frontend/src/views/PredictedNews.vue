<template>
  <div class="predicted_news">
    <h1>Predicted News List</h1>
    <el-button type="primary" v-on:click="startPrediction">予測開始</el-button>
    <br>
    <br>
    <div v-for="item in categories" :key="item.category_id">
        <div>
            <h2>
            カテゴリー: {{ item.category_name }}
            </h2>
        </div>
        <el-table class="data-table" :data="news_by_categories[item.category_id]" stripe>
            <el-table-column prop="id" label="ID" width="100"></el-table-column>
            <el-table-column prop="created_at" label="Posted Date"></el-table-column>
            <el-table-column prop="og_site_name" label="サイト名" width="140"></el-table-column>
            <el-table-column prop="og_title" label="Title"></el-table-column>
            <el-table-column prop="og_description" label="text"></el-table-column>
            <el-table-column label="URL">
              <template slot-scope="scope">
                <el-link :href="scope.row.url" target="_blank">link</el-link>
              </template>
            </el-table-column>
            <el-table-column prop="probability" label="Probability"></el-table-column>
        </el-table>
        <br>
        <el-button type="primary" plain size="small" :loading="is_loading_by_categories[item.category_id]" :disabled="is_desabled_by_categories[item.category_id]" v-on:click="onClickLoadButton(item.category_id)">
          {{ is_loading_by_categories[item.category_id] ? 'Loading' : 'More' }}
        </el-button>
        <br>
        <br>
        <br>
    </div>
    <div id="overlay" v-show="showPopUp">
        <div id="content">
          <p>文書分類してます。数分後にリロードしてみてね</p>
          <el-button type="primary" v-on:click="closeModal" size="small">Close</el-button>
        </div>
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
      news_by_categories: {},
      is_loading_by_categories: {},
      is_desabled_by_categories: {},
      showPopUp: false
    }
  },
  mounted () {
    this.updateTableData()
  },
  methods: {
    updateTableData: async function () {
      const response = await axios.get('api/categories')
      this.categories = response.data

      for (var cat in this.categories) {
        var t = this.categories[cat]
        this.$set(this.is_loading_by_categories, t.category_id, false)
        this.$set(this.is_desabled_by_categories, t.category_id, false)
      }

      for (var key in this.categories) {
        var tmp = this.categories[key]
        var res = await axios.get('api/news_data/predicted_category?category_id=' + tmp.category_id)
        this.$set(this.news_by_categories, tmp.category_id, res.data)
      }
    },
    onClickLoadButton: async function (categoryId) {
      this.$set(this.is_loading_by_categories, categoryId, true)

      const minScrapeId = this.news_by_categories[categoryId][this.news_by_categories[categoryId].length - 1].id
      var res = await axios.get('api/news_data/predicted_category?category_id=' + categoryId + '&min_scrape_id=' + String(minScrapeId))

      if (res.data.length === 0) {
        this.$set(this.is_desabled_by_categories, categoryId, true)
      }
      var tmparray = this.news_by_categories[categoryId].concat(res.data)
      this.$set(this.news_by_categories, categoryId, tmparray)
      this.$set(this.is_loading_by_categories, categoryId, false)
    },
    startPrediction: async function () {
      this.openModal()
      await axios.get('api/start_processing')
    },
    openModal: function () {
      this.showPopUp = true
    },
    closeModal: function () {
      this.showPopUp = false
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
#overlay{
  z-index:1;
  position:fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background-color:rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
#content{
  z-index:2;
  width:50%;
  padding: 1em;
  background:#fff;
}
</style>
