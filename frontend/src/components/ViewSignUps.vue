<template>
    <div class="container mt-3">
        <h1>View Sign Ups</h1>
        <div class="container">
            <div class="container mt-5">
                <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="signup in sign_ups" :key="[signup.EID, signup.SID, signup.CID]">
                    <div>
                        {{signup.EID}} {{signup.CID}} {{signup.SID}}
                    </div>

                    <div><button type="button" class="btn btn-outline-primary">Accept</button>
                    <span class="float-right"><button type="button" class="btn btn-outline-primary">Reject</button></span></div>
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
            fetch('http://localhost:5001//hr_view_signup', {
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