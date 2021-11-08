<template>
    <div class="container mt-3">
        <h1>View Sign Ups</h1>
        <div class="container">
            <div class="container mt-5">
                <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="signup in sign_ups" :key="[signup.EID, signup.SID, signup.CID,signup.start]">
                    <div class="container">
                        <strong>EID</strong>
                    </div>
                    <div class="container">
                        <strong>CID</strong>
                    </div>
                    <div class="container">
                        <strong>SID</strong>
                    </div>
                    <div class="container">
                        
                    </div>
                    
                </div>

                <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="signup in sign_ups" :key="[signup.EID, signup.SID, signup.CID,signup.start]">
                    <div class="container">
                        {{signup.EID}}  
                    </div>

                    <div class="container">
                        {{signup.CID}}
                    </div>

                    <div class="container">
                        {{signup.SID}}
                    </div>

                    <div class="container">
                        <router-link type="button" class="btn btn-outline-primary" :to="{name: 'hr_signup_approved', params:{EID:signup.EID, SID:signup.SID, CID:signup.CID, start:signup.start}}">Accept</router-link>
                        <span class="float-right"><router-link type="button" class="btn btn-outline-primary" :to="{name: 'hr_signup_rejected', params:{EID:signup.EID, SID:signup.SID, CID:signup.CID, start:signup.start}}">Reject</router-link></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return {
            sign_ups : [],
        }
    },

    methods: {
        viewSignUps() {
            fetch('http://18.118.224.235:5001/hr_view_signup', {
                method: "GET",
                headers: {
                    "Content-Type" : "application/json"
                }
            })
            .then(resp => resp.json())
            .then(data => {
                this.sign_ups.push(...data.data);
            })
            .catch(error => {
                console.log(error)
            })
        }
    },

    created() {
        this.viewSignUps()
    }
}
</script>

<style>

</style>