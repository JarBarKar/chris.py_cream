<template>
    <div class="container mt-3">
		<h1>Ongoing Courses</h1>
		<table class="table">
			<thead>
				<tr>
					<th scope="col">Course</th>
					<th scope="col">Section</th>
					<th scope="col"></th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="course in ongoing_courses" :key="[course.EID, course.CID, course.SID, course.start]">
					<td>{{course.CID}}</td>
					<td>{{course.SID}}</td>
					<td>
						<button type="button" class="btn btn-outline-primary">View Content</button>
					</td>
				</tr>
			</tbody>
		</table>
    </div>
</template>

<script>
export default {

	data() {
		return{
			ongoing_courses : []
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
				console.log(data.data)
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