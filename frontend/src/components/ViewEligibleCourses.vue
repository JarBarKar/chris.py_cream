<template>
    <div class="container mt-3">
        <h1>View Eligible Courses</h1>
        <div class="container">
            <!-- Nav tabs -->
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <router-link class="nav-link" type="button" role="tab" :to="{name: 'engineer_signup', params: {EID:this.EID}}">All Courses</router-link>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="true">Eligible Courses</button>
                </li>
                <li class="nav-item" role="presentation">
                    <router-link class="nav-link" type="button" role="tab" :to="{name: 'view_pending_courses', params: {EID: this.EID}}">Pending Courses</router-link>
                </li>
            </ul>

            <!-- Tab panes -->
            <div class="tab-content">
                <div class="tab-pane" id="home" role="tabpanel" aria-labelledby="home-tab">...</div>
                <div class="tab-pane active" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                    <div class="container mt-5">
                        <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="course in eligible_courses" :key="course.CID">
                            <div>
                                {{course.name}}
                            </div>
                            <div>
                                <router-link type="button" class="btn btn-outline-primary" :to="{name: 'sections', params:{CID:course.CID}}">View Section</router-link>
                            </div>
                        </div>
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
            
            eligible_courses : null,
            non_eligible_courses : null
        }
    },

    props:{
        EID: {
			type: [Number, String],
			required: true
        }
    },

    methods: {
        getEligibleCourses() {
            fetch('http://18.118.224.235:5001/view_eligible_courses', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        EID : this.EID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                this.eligible_courses = data.data.eligible
                this.non_eligible_courses = data.data.non_eligible
            })
            .catch(error => {
                console.log(error)
            })
        }
    },

    created() {
        this.getEligibleCourses()
    }
    
}
</script>

<style>

</style>