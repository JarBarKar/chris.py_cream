<template>
    <div>
        <div class="container my-5">
            <h1>Login</h1>
        </div>

        <div class="container-fluid my-2">
            <router-link type="button" class="btn btn-outline-primary" :to="{name: 'engineer', params: {EID: this.EID}}">Log in as Engineer</router-link>
        </div>

        <div class="container-fluid my-2">
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
    .bg {
        color: blue;
    }
</style>