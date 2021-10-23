<template>
    <div>
        <h1>Assign Trainers</h1>

        <div class="container mt-5">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-between" v-for="course in courses" :key="course.CID">
                <div>
                    {{course.name}}
                </div>
                <div>
                    <button type="button" class="btn btn-outline-primary">Assign Trainer</button>
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
            fetch('http://localhost:5001/view_courses', {
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