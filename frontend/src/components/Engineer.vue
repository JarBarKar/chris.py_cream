<template>
    <div>
        <div class="container my-5">
            <h1>Engineer</h1>
        </div>

        <div class="container my-2">
            <router-link type="button" class="btn btn-outline-primary" to="/engineer/signup">Sign Up for Courses</router-link>
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
            "EID" : 1
        }
    }
}
</script>

<style>

</style>