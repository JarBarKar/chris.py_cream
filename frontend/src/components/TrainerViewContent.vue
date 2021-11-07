<template>
    <div>
        <div class="container mt-3">
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
            <router-link  type="button" class="btn btn-outline-primary" :to="{name:'trainer_view_quiz', params:{TID:this.TID,SID:this.SID,CID:this.CID,LID:this.LID,start:this.start}}">View Quiz</router-link>
            <button  type="button" class="btn btn-outline-primary" :to="{name:'take_quiz', params:{EID:this.EID,SID:this.SID,CID:this.CID,LID:this.LID,start:this.start}}">Delete Quiz</button>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            contents: []
        }
    },

    props: {
        CID: {
			type: [Number, String],
			required: true
		},
		TID: {
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
			fetch('http://localhost:5001/view_lesson_content', {
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
		}
    },

    created(){
        this.ViewLessonContent()
    }

        

}
</script>

<style>

</style>