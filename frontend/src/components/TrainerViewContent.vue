<template>
    <div>
        <div class="container mt-3">
            <h1>Materials for Lesson {{this.LID}}</h1>
            
            <div class="container">
                <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly h4">
                    <div class="container">Name</div>
                    <div class="container">Link</div>
                    <div class="container"></div>
                    <div class="container"></div>
                    
                    
                </div>
            </div>

            <div class="container">
                <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly" v-for="content in contents" :key="[content.SID, content.CID, content.LID, content.start, content.content_name]">
                    <div class="container">{{content.content_name}}</div>
                    <div class="container">
                        <a :href="content.link" class="link-primary">Click me</a>
                    </div>    
                    <div class="container">
                        <router-link type="button" class="btn btn-outline-primary" :to="{name: 'trainer_update_content', params:{TID:this.TID,SID:this.SID,CID:this.CID,LID:this.LID,start:this.start, content_name: content.content_name, content_type: content.content_type, link: content.link}}">Update Content</router-link>
                    </div>
                    <div class="container">
                        <button type="button" class="btn btn-outline-primary" v-on:click="deleteContent(content.content_name)">Delete Content</button>
                    </div>
                </div>
            </div>
            <router-link  type="button" class="btn btn-outline-primary" :to="{name:'trainer_view_quiz', params:{TID:this.TID,SID:this.SID,CID:this.CID,LID:this.LID,start:this.start}}">View Quiz</router-link>
            
        </div>

        <div v-if="deleted == true" class="alert alert-success mt-3" role="alert">
            Content has been deleted
        </div>

        <div v-else-if="deleted == false" class="alert alert-danger mt-3" role="alert">
            An error occurred
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            contents: [],
            deleted: null
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

        deleteContent(content_name) {
			fetch('http://18.118.224.235:5001/delete_content', {
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
                        content_name: content_name
                    
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				if(data.message.includes('deleted successfully')){
                    this.deleted = true
                }
                else{
                    this.deleted = false
                }
                
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