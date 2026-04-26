import DefaultTheme from 'vitepress/theme'
import RecentCases from './components/RecentCases.vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('RecentCases', RecentCases)
  }
}
