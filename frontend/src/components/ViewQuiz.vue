<template>
    <div>
        <table class="table">
			<thead>
				<tr>
					<th scope="col">Question</th>
					<th scope="col"></th>
                    <th scope="col"></th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="question in questions" :key="[question.LID, question.CID, question.SID, question.start, question.question]">
					<td>{{question.question}}</td>
					<td>
                        <router-link type="button" class="btn btn-outline-primary" :to="{name:'trainer_update_quiz_question', params:{TID: this.TID, CID: question.CID, SID: question.SID, start: question.start, question: question.question, LID: question.LID}}">Update</router-link>
                    </td>
                    <td>
                        <button type="button" class="btn btn-outline-primary" v-on:click="deleteQuestion(question.question)">Delete</button>
                    </td>
				</tr>
			</tbody>
		</table>
        
        <div>
            <router-link type="button" class="btn btn-outline-primary" :to="{name:'trainer_create_quiz_question', params:{TID: this.TID, CID: this.CID, SID: this.SID, start: this.start, LID: this.LID}}">
                Create Question
            </router-link>
        </div>
        <div class="container mt-3">
            <button type="button" class="btn btn-outline-primary" v-on:click="deleteQuiz()">
                Delete Quiz
            </button>
        </div>
        
        <div v-if="qn_deleted" class="alert alert-success mt-3" role="alert">
            Question was deleted
        </div>

        <div v-if="quiz_deleted" class="alert alert-success mt-3" role="alert">
            Quiz was deleted
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            questions: [],
            qn_deleted: null,
            quiz_deleted: null
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
        readQuiz() {
			fetch('http://18.118.224.235:5001/read_quiz', {
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
				console.log(data)
                this.questions = data.data
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},

        deleteQuestion(question){
            fetch('http://18.118.224.235:5001/delete_quiz_question', {
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
                        question: question
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				console.log(data)
                this.qn_deleted = true
                
            })
            .catch(error => {
                
                console.error("There was an error!", error)
            })
        },

        deleteQuiz(){
            fetch('http://18.118.224.235:5001/delete_quiz', {
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
				console.log(data)
                this.quiz_deleted = true
                
            })
            .catch(error => {
                
                console.error("There was an error!", error)
            })
        }

        
    },

    created(){
        this.readQuiz()
    }
}
</script>

<style>

</style>