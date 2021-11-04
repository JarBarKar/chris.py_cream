<template>
    <div>
        <div class="container my-5">
            <h1>Engineer</h1>
        </div>

        <div class="container my-2">
            <router-link type="button" class="btn btn-outline-primary" :to="{name: 'engineer_signup', params: {EID:this.EID}}">Sign Up for Courses</router-link>
        </div>

        <div class="container my-2">
            <router-link type="button" class="btn btn-outline-primary" :to="{name: 'attend_courses', params: {EID:this.EID}}">Attend Courses</router-link>
        </div>

    </div>
</template>

<script>
export default {

    data() {
        return{
            
        }
    },

    props: {
        EID : {
            type: [Number, String],
			required: true
        }
    }
}
</script>

<style>

</style>