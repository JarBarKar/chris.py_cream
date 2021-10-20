import {createRouter, createWebHistory} from 'vue-router'
import Home from './components/Home..vue'
import Engineer from './components/Engineer.vue'
import SignUpCourses from './components/SignUpCourses.vue'
import HR from './components/HR.vue'
import ViewSignUps from './components/ViewSignUps.vue'
import AssignTrainers from './components/AssignTrainers.vue'

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },

    {
        path: '/engineer',
        name: 'engineer',
        component: Engineer
    },

    {
        path: '/engineer/signup',
        name: 'engineer_signup',
        component: SignUpCourses
    },

    {
        path: '/hr',
        name: 'hr',
        component: HR
    },

    {
        path: '/hr/viewsignup',
        name: 'hr_viewsignup',
        component: ViewSignUps
    },

    {
        path: '/hr/assign_trainers',
        name: 'assign_trainers',
        component: AssignTrainers
    }
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router