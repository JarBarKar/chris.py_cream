<template>
    <div>
        <h1>Sign Up for Courses</h1>

        <!-- Nav tabs -->
        <ul class="nav nav-tabs" id="myTab" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active" id="home-tab" data-bs-toggle="tab" data-bs-target="#home" type="button" role="tab" aria-controls="home" aria-selected="true">All Courses</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link" id="profile-tab" data-bs-toggle="tab" data-bs-target="#profile" type="button" role="tab" aria-controls="profile" aria-selected="false">Eligible Courses</button>
            </li>
        </ul>

<!-- Tab panes -->
        <div class="tab-content">
            <div class="tab-pane active" id="home" role="tabpanel" aria-labelledby="home-tab">
                <ul class="list-group">
                    <li class="list-group-item" v-for="course in courses" :key="course.CID">
                        {{course.name}}
                        <span>
                            <button type="button" class="btn btn-outline-primary">View Section</button>
                        </span>
                    </li>
                </ul>
            </div>
            <div class="tab-pane" id="profile" role="tabpanel" aria-labelledby="profile-tab">...</div>
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