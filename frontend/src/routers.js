import {createRouter, createWebHistory} from 'vue-router'
import Home from './components/Home..vue'
import Engineer from './components/Engineer.vue'
import SignUpCourses from './components/SignUpCourses.vue'
import HR from './components/HR.vue'
import ViewSignUps from './components/ViewSignUps.vue'
import AssignTrainers from './components/AssignTrainers.vue'
import ViewEligibleCourses from './components/ViewEligibleCourses.vue'
import ViewSections from './components/ViewSections.vue'
import AttendCourses from './components/AttendCourses.vue'
import Trainer from './components/Trainer.vue'
import TrainerViewSections from './components/TrainerViewSections.vue'
import HRSignUpApp from './components/HRSignUpApp.vue'

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
        path: '/engineer/attend_courses/:EID',
        name: 'attend_courses',
        component: AttendCourses,
        props: true
    },

    {
        path: '/engineer/view_eligible_courses',
        name: 'view_eligible_courses',
        component: ViewEligibleCourses
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
        path: '/hr/signup_approved/:EID/:CID/:SID/:start',
        name: 'hr_signup_approved',
        component: HRSignUpApp,
        props: true
    },

    {
        path: '/hr/assign_trainers',
        name: 'assign_trainers',
        component: AssignTrainers
    },

    {
        path: '/sections/:CID',
        name: 'sections',
        component: ViewSections,
        props: true
    },

    {
        path: '/trainer',
        name: 'trainer',
        component: Trainer
    },

    {
        path: '/trainer/view_sections',
        name: 'trainer_view_sections',
        component: TrainerViewSections
    }

    
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router