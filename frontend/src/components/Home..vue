<template>
    <div>
        <div class="container my-5">
            <h1>Login</h1>
        </div>

        <div class="container-fluid my-2">
            <router-link type="button" class="btn btn-outline-primary" to="/engineer">Log in as Engineer</router-link>
        </div>

        <div class="container-fluid my-2">
            <router-link type="button" class="btn btn-outline-primary" to="/hr">Log in as HR</router-link>
        </div>

        <div class="container-fluid my-2">
            <router-link type="button" class="btn btn-outline-primary" to="/trainer">Log in as Trainer</router-link>
        </div>
    </div>
</template>

<script>
export default {

}
</script>

<style>
    .bg {
        color: blue;
    }
</style>