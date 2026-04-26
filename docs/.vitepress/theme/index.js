import DefaultTheme from 'vitepress/theme'
import RecentCases from './components/RecentCases.vue'
import HomePage from './components/HomePage.vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('RecentCases', RecentCases)
    app.component('HomePage', HomePage)
  }
}
