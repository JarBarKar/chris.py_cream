<template>
    <div>
        <div class="container mt-3" v-if="this.LID <= this.latest_lesson_reached">
            <h1>Materials for Lesson {{this.LID}}</h1>
            <div class="container">
                <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly h4">
                    <div class="container">Name</div>
                    <div class="container">Link</div>
                    
                    
                </div>
            </div>

            <div class="container">
                <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly" v-for="content in contents" :key="[content.SID, content.CID, content.LID, content.start, content.content_name]">
                    <div class="container">{{content.content_name}}</div>
                    <div class="container">
                        <a href="https://docs.google.com/presentation/d/1z5DzoSjp4CL6VMfxIvHFlkTPUr8QoJxs/edit#slide=id.p1" class="link-primary">Click me</a>
                    </div>    
                </div>
            </div>
            <router-link v-if="taken_quiz" type="button" class="btn btn-outline-primary" :to="{name:'check_quiz_results', params:{EID:this.EID,SID:this.SID,CID:this.CID,LID:this.LID,start:this.start}}">View Quiz Result</router-link>
            <router-link v-else type="button" class="btn btn-outline-primary" :to="{name:'take_quiz', params:{EID:this.EID,SID:this.SID,CID:this.CID,LID:this.LID,start:this.start}}">Take Quiz</router-link>
        </div>

        <div class="container mt-3" v-else>
            <div class="alert alert-danger" role="alert">
                You have not unlocked this yet.
            </div>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            contents: [],
            // start: "2021-04-01 09:15:00",
            latest_lesson_reached: "",
            taken_quiz: false
        }
    },

    props: {
        CID: {
			type: [Number, String],
			required: true
		},
		EID: {
			type: [Number, String],
			required: true
        },
        SID: {
            type: [Number, String],
			required: true
        },
        start: {
            type: [Number, String],
			required: true
        },
        LID: {
            type: [Number, String],
			required: true
        }
    },

    methods: {
        ViewLessonContent() {
			fetch('http://18.118.224.235:5001/view_lesson_content', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        LID: this.LID,
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start
                    
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				this.contents = data.data
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},

        LatestContentAccessed() {
			fetch('http://18.118.224.235:5001/view_latest_content_accessed', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        content_name: "",
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start,
                        EID: this.EID
                    
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				this.latest_lesson_reached = data.data.latest_lesson_reached
                // console.log(this.latest_lesson_reached)
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},

        takenQuiz() {
			fetch('http://18.118.224.235:5001/check_quiz_result', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        LID: this.LID,
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start,
                        EID: this.EID
                    
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				this.taken_quiz = data.data
                console.log(this.taken_quiz)
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},
    },

    created(){
        this.ViewLessonContent(),
        this.LatestContentAccessed(),
        this.takenQuiz()
    }
}
</script>

<style>

</style>