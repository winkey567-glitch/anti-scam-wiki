import DefaultTheme from 'vitepress/theme'
import RecentCases from './components/RecentCases.vue'
import HomePage from './components/HomePage.vue'
import EmergencyPage from './components/EmergencyPage.vue'
import QuizPage from './components/QuizPage.vue'
import ScenariosOverviewPage from './components/ScenariosOverviewPage.vue'
import ProfilesOverviewPage from './components/ProfilesOverviewPage.vue'
import CasesLandingPage from './components/CasesLandingPage.vue'
import ChecklistPage from './components/ChecklistPage.vue'

export default {
  ...DefaultTheme,
  enhanceApp({ app }) {
    app.component('RecentCases', RecentCases)
    app.component('HomePage', HomePage)
    app.component('EmergencyPage', EmergencyPage)
    app.component('QuizPage', QuizPage)
    app.component('ScenariosOverviewPage', ScenariosOverviewPage)
    app.component('ProfilesOverviewPage', ProfilesOverviewPage)
    app.component('CasesLandingPage', CasesLandingPage)
    app.component('ChecklistPage', ChecklistPage)
  }
}
