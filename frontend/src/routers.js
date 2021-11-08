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
import ViewLessons from './components/ViewLessons'
import HRViewSections from './components/HRViewSections'
import TrainerViewLessons from './components/TrainerViewLessons'
import TakeQuiz from './components/TakeQuiz'
import CheckQuizResults from './components/CheckQuizResults'
import ViewQuiz from './components/ViewQuiz'
import ViewLessonContent from './components/ViewLessonContent.vue'
import TrainerViewContent from './components/TrainerViewContent.vue'
import TrainerUpdateQuizQuestion from './components/TrainerUpdateQuizQuestion.vue'
import HRAvailableTrainers from './components/HRAvailableTrainers.vue'
import HRAssignEngineers from './components/HRAssignEngineers.vue'
import HRAssignEngineersSection from './components/HRAssignEngineersSection.vue'
import HRQualifiedLearners from './components/HRQualifiedLearners.vue'
import TrainerCreateQuizQuestion from './components/TrainerCreateQuizQuestion.vue'
import SubmitQuiz from './components/SubmitQuiz.vue'
import PendingCourses from './components/PendingCourses.vue'

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
        path: '/engineer/view_pending_courses/:EID',
        name: 'view_pending_courses',
        component: PendingCourses,
        props: true
    },

    {
        path: '/engineer/view_lessons/:EID/:CID/:SID/:start',
        name: 'view_lessons',
        component: ViewLessons,
        props: true
    },

    {
        path: '/engineer/view_lesson_content/:EID/:CID/:SID/:start/:LID',
        name: 'view_lesson_content',
        component: ViewLessonContent,
        props: true
    },

    {
        path: '/engineer/take_quiz/:EID/:CID/:SID/:LID/:start',
        name: 'take_quiz',
        component: TakeQuiz,
        props: true
    },

    {
        path: '/engineer/submit_quiz/:EID/:CID/:SID/:LID/:start',
        name: 'submit_quiz',
        component: SubmitQuiz,
        props: true
    },

    {
        path: '/engineer/check_quiz_results/:EID/:CID/:SID/:LID/:start',
        name: 'check_quiz_results',
        component: CheckQuizResults,
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
        path: '/hr/view_sections/:CID',
        name: 'hr_view_sections',
        component: HRViewSections,
        props: true
    },

    {
        path: '/hr/available_trainers/:CID/:SID',
        name: 'hr_available_trainers',
        component: HRAvailableTrainers,
        props: true
    },

    {
        path: '/hr/assign_engineers',
        name: 'hr_assign_engineers',
        component: HRAssignEngineers
    },

    {
        path: '/hr/assign_engineers/sections/:CID',
        name: 'hr_assign_engineers_sections',
        component: HRAssignEngineersSection,
        props: true
    },

    {
        path: '/hr/qualified_learners/:CID/:SID/:start',
        name: 'hr_qualified_learners',
        component: HRQualifiedLearners,
        props: true
    },

    {
        path: '/sections/:EID/:CID',
        name: 'sections',
        component: ViewSections,
        props: true
    },

    {
        path: '/trainer/:TID',
        name: 'trainer',
        component: Trainer,
        props: true
    },

    {
        path: '/trainer/view_sections/:TID',
        name: 'trainer_view_sections',
        component: TrainerViewSections,
        props: true
    },

    {
        path: '/trainer/view_lessons/:TID/:CID/:SID/:start',
        name: 'trainer_view_lessons',
        component: TrainerViewLessons,
        props: true
    },

    {
        path: '/trainer/view_content/:TID/:CID/:SID/:start/:LID',
        name: 'trainer_view_content',
        component: TrainerViewContent,
        props: true
    },

    {
        path: '/trainer/view_quiz/:TID/:CID/:SID/:LID/:start',
        name: 'trainer_view_quiz',
        component: ViewQuiz,
        props: true
    },

    {
        path: '/trainer/update_quiz_question/:TID/:CID/:SID/:LID/:start/:question',
        name: 'trainer_update_quiz_question',
        component: TrainerUpdateQuizQuestion,
        props: true
    },

    {
        path: '/trainer/create_quiz_question/:TID/:CID/:SID/:LID/:start/',
        name: 'trainer_create_quiz_question',
        component: TrainerCreateQuizQuestion,
        props: true
    }

    
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router