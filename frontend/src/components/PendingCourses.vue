<template>
    <div class="container mt-3">
        <h1>Pending Courses</h1>
        <div class="container">
            <!-- Nav tabs -->
            <ul class="nav nav-tabs" id="myTab" role="tablist">
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
    props:{
        EID: {
			type: [Number, String],
			required: true
        }
    },
}
</script>

<style>

</style>