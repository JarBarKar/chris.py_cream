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
import CompletedCourses from './components/CompletedCourses.vue'
import EngineerSignUp from './components/EngineerSignUp'
import HRSignupRej from './components/HRRejectSignUp'

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },

    {
        path: '/engineer/:EID',
        name: 'engineer',
        component: Engineer,
        props:true
    },

    {
        path: '/engineer/signup/:EID',
        name: 'engineer_signup',
        component: SignUpCourses,
        props: true
    },

    {
        path: '/engineer/attend_courses/:EID',
        name: 'attend_courses',
        component: AttendCourses,
        props: true
    },

    {
        path: '/engineer/completed_courses/:EID',
        name: 'completed_courses',
        component: CompletedCourses,
        props: true
    },

    {
        path: '/engineer/view_eligible_courses/:EID',
        name: 'view_eligible_courses',
        component: ViewEligibleCourses,
        props: true
    },

    {
        path: '/engineer/sign_up/:EID/:CID/:SID/',
        name: 'engineer_sign_up_action',
        component: EngineerSignUp,
        props: true
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
        path: '/hr/signup_rejected/:EID/:CID/:SID/:start',
        name: 'hr_signup_rejected',
        component: HRSignupRej,
        props: true
    },
    
    {
        path: '/hr/assign_trainers',
        name: 'assign_trainers',
        component: AssignTrainers
    },

    {
        path: '/sections/:EID/:CID',
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