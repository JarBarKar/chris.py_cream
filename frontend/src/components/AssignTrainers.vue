<template>
    <div>
        <h1>Assign Trainers</h1>

        <ul class="list-group">
            <li class="list-group-item" v-for="course in courses" :key="course.CID">
                {{course.name}}
                <span>
                    <button type="button" class="btn btn-outline-primary">Assign Trainer</button>
                </span>
            </li>
        </ul>
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