<template>
    <div >
        <div class="container mt-5">
            <h1>Login</h1>
        </div>

        <div class="container mt-5">
            <router-link type="button" class="btn btn-outline-primary" :to="{name: 'engineer', params: {EID: this.EID}}">Log in as Engineer</router-link>
        </div>

        <div class="container-fluid mt-2">
            <router-link type="button" class="btn btn-outline-primary" to="/hr">Log in as HR</router-link>
        </div>

        <div class="container-fluid my-2">
            <router-link type="button" class="btn btn-outline-primary" :to="{name: 'trainer', params: {TID: this.TID}}">Log in as Trainer</router-link>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            EID: 1,
            TID: 1
        }
    }

}
</script>

<style>
    .bg{
        background-image: url('../assets/photo_2021-11-06_15-38-19.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        height: 100vh;
    }
</style>