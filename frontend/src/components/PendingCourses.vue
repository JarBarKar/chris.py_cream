<template>
    <div class="container mt-3">
        <h1>Pending Courses</h1>
        <div class="container">
            <!-- Nav tabs -->
            <ul class="nav nav-pills" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <router-link class="nav-link" type="button" role="tab" :to="{name: 'engineer_signup', params: {EID:this.EID}}">All Courses</router-link>
                </li>
                <li class="nav-item" role="presentation">
                    <router-link class="nav-link" type="button" role="tab" :to="{name: 'view_eligible_courses', params: {EID: this.EID}}">Eligible Courses</router-link>
                </li>
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="pending-tab" data-bs-toggle="tab" data-bs-target="#pending" type="button" role="tab" aria-controls="pending" aria-selected="true">Pending Courses</button>
                </li>
            </ul>

            <!-- Tab panes -->
            <div class="tab-content">
                <div class="tab-pane" id="home" role="tabpanel" aria-labelledby="home-tab">...</div>
                <div class="tab-pane" id="profile" role="tabpanel" aria-labelledby="profile-tab"></div>
                <div class="tab-pane active" id="pending" role="tabpanel" aria-labelledby="pending-tab">
                    <div class="container mt-5">
                        <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="course in pending" :key="course.CID">
                            <div>
                                {{course.course_name}}
                            </div>
                            <div>
                                <button type="button" class="btn btn-outline-primary" v-on:click="withdrawEngineer(course.CID,course.SID,course.start)">Withdraw</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="withdrawn == true" class="alert alert-success" role="alert">
            Engineer has withdrawn from the course
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            pending : [],
            withdrawn: null
        }
    },

    props:{
        EID: {
			type: [Number, String],
			required: true
        }
    },

    methods: {
        getPendingCourses() {
            fetch('http://18.118.224.235:5001/view_enrollment_by_EID', {
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
                console.log(data)
                this.pending = data.data
            })
            .catch(error => {
                console.log(error)
            })
        },

        withdrawEngineer(CID,SID,start) {
			fetch('http://18.118.224.235:5001/engineer_withdraw', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        CID : CID,
                        SID : SID,
                        start: start,
                        EID: this.EID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data)
                if (data.message.includes('successfully')){
                    this.withdrawn = true
                }
            })
            .catch(error => {
                console.log(error)
            })
		}
    },

    created() {
        this.getPendingCourses()
    }
}
</script>

<style>

</style>