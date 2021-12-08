<template>
    <div class="container mt-3">
        <h1>Assign Engineers</h1>

        <div class="container mt-5">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="course in courses" :key="course.CID">
                <div>
                    {{course.name}}
                </div>
                <div>
                    <router-link type="button" class="btn btn-outline-primary" :to="{name:'hr_assign_engineers_sections', params:{CID:course.CID}}">View Sections</router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return {
            courses : [],
        }
    },
    
    methods: {
        getCourses() {
            fetch('http://18.118.224.235:5001/view_courses', {
                method: "GET",
                headers: {
                    "Content-Type" : "application/json"
                }
            })
            .then(resp => resp.json())
            .then(data => {
                this.courses.push(...data.data);
            })
            .catch(error => {
                console.log(error)
            })
        }
    },

    created() {
        this.getCourses()
    }
}
</script>

<style>

</style>