<template>
  <div>
        <h1>View Sign Ups</h1>
    
        <ul class="list-group">
            <li class="float-left list-group-item" v-for="signup in sign_ups" :key="[signup.EID, signup.SID, signup.CID]">
                {{signup.EID}} {{signup.CID}} {{signup.SID}}
                <span><button type="button" class="btn btn-outline-primary">Accept</button></span>
                <span class="float-right"><button type="button" class="btn btn-outline-primary">Reject</button></span>
            </li>
            
        </ul>
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