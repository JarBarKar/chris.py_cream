<template>
    <div class="container mt-3">
		<h1>Ongoing Courses</h1>
		<div class="container">
            <!-- Nav tabs -->
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item" role="presentation">
                    <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true">Ongoing Courses</button>
                </li>
                <li class="nav-item" role="presentation">
                    <router-link class="nav-link" type="button" role="tab" :to="{name:'completed_courses', params:{EID:this.EID}}">Completed Courses</router-link>
                </li>
            </ul>

            <!-- Tab panes -->
            <div class="tab-content">
                <div class="tab-pane active" id="home" role="tabpanel" aria-labelledby="home-tab">
                    <div class="container mt-5">
                        <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="course in ongoing_courses" :key="[course.CID, course.SID, course.EID, course.start]">
                            <div>
                                {{course.CID}}
                            </div>
							<div>
								{{course.SID}}
							</div>
                            <div>
                                <router-link type="button" class="btn btn-outline-primary" :to="{name: 'sections', params:{CID:course.CID}}">View Section</router-link>
                            </div>
                        </div>

                        <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="course in non_eligible_courses" :key="course.CID">
                            <div>
                                {{course.name}}
                            </div>
                            
                            <div>
                                <button type="button" class="btn btn-outline-primary disabled">View Section</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="tab-pane" id="profile" role="tabpanel" aria-labelledby="profile-tab"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {

	data() {
		return{
			ongoing_courses : [],
			completed_courses: []
		}
	},

    props:{
        EID: {
			type: [Number, String],
			required: true
        }
    },

	methods: {
		getOngoingCourses() {
			fetch('http://localhost:5001/view_current_completed_courses', {
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
                this.ongoing_courses = data.data.ongoing_courses
				this.completed_courses = data.data.completed_courses
            })
            .catch(error => {
                console.log(error)
            })
		}
	},

	created() {
		this.getOngoingCourses()
	}
}
</script>

<style>

</style>