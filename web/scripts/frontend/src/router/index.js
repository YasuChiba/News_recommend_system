import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Annotating from '../views/Annotating.vue'
import AnnotatedNews from '../views/AnnotatedNews.vue'
import PredictedNews from '../views/PredictedNews.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/annotate',
    name: 'annotate',
    component: Annotating
  },
  {
    path: '/annotated_news',
    name: 'annotated_news',
    component: AnnotatedNews
  },
  {
    path: '/predicted_news',
    name: 'predicted_news',
    component: PredictedNews
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
