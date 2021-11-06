<template>
    <div class="container mt-3">
        <h1>Lessons</h1>
        <div class="container">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly h4">
                <div class="container">CID</div>
                <div class="container">SID</div>
                <div class="container">LID</div>
                <div class="container">Content</div>
                <div class="container">Link</div>
                <div class="container"></div>
                <div class="container"></div>
            </div>
        </div>

        <div class="container">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly" v-for="lesson in lessons" :key="[lesson.SID, lessons.CID, lesson.LID, lesson.start, lesson.content_name]">
                <div class="container">{{lesson.CID}}</div>
                <div class="container">{{lesson.SID}}</div>
                <div class="container">{{lesson.LID}}</div>
                <div class="container">{{lesson.content_name}}</div>
                <div class="container">
                    <a v-bind:href="lesson.link">View</a>
                </div>
                <div class="container">
                    <router-link type="button" class="btn btn-outline-primary" :to="{name:'take_quiz', params:{EID:this.EID, CID:lesson.CID,SID:lesson.SID,LID:lesson.LID}}">Take Quiz</router-link>
                </div>
                <div class="container">
                    <router-link type="button" class="btn btn-outline-primary" :to="{name:'check_quiz_results', params:{EID:this.EID, CID:lesson.CID,SID:lesson.SID,LID:lesson.LID,start:lesson.start}}">View Results</router-link>
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
export default {

    data() {
        return{
            lessons: []
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
        }
    },

    methods: {
        ViewLessons() {
			fetch('http://localhost:5001/view_all_section_content', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				this.lessons = data.data
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		}
    },

    created(){
        this.ViewLessons()
    }

    
}
</script>

<style>

</style>