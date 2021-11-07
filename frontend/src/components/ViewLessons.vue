<template>
    <div class="container mt-3">
        <h1>{{this.CID}} Section {{this.SID}}</h1>
        <div class="container">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly h4">
                <div class="container"></div>
                <div class="container"></div>
            </div>
        </div>

        <div class="container">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly" v-for="lesson in lessons" :key="[lesson.SID, lessons.CID, lesson.LID, lesson.start]">
                <div class="container">Lesson {{lesson.LID}}</div>
                <div class="container">
                    <router-link type="button" class="btn btn-outline-primary" :to="{name:'view_lesson_content', params:{EID:this.EID,SID:lesson.SID,CID:lesson.CID,LID:lesson.LID,start:this.start}}">View Content</router-link>
                    
                </div>
            </div>
        </div>
        
    </div>
</template>

<script>
export default {

    data() {
        return{
            lessons: [],
            latest_lesson_reached : ""
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
			fetch('http://localhost:5001/query_lessons', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        
                        SID : this.SID,
                        CID : this.CID,
                    
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