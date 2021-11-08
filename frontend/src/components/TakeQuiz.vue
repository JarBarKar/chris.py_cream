<template>
    <div class="container mt-3">
        <h1>Questions</h1>
        <div>{{timerCount}}</div>
        <div class="mb-3 row justify-content-center" >
            <form v-for="(question,  index) in questions" :key="[question.LID, question.CID, question.SID, question.start, question.question]">
                <label for="staticEmail" class="col-sm-2 col-form-label">
                    <strong>{{question.question}}</strong>
                    
                    
                </label>
                <br>
                <div class="form-check form-check-inline" v-for="option in (question.options.split('|'))" :key="option">
                    <input class="form-check-input" type="radio" id="inlineCheckbox1" :value="option" v-model="QAMarks[index].answer">
                    <label class="form-check-label" for="inlineCheckbox1">{{option}}</label>
                </div>
                {{QAMarks.answer}}
            </form>
        </div>
        <button type="button" class="btn btn-primary" v-on:click="checkAnswers();submitQuiz();unlockNextLesson()" >Submit</button>
        <br>
        
        <div v-if="passed == true & type == 'graded'" class="alert alert-success" role="alert">
            You passed!
        </div>

        <div v-else-if="passed == false & type == 'graded'" class="alert alert-danger" role="alert">
            You failed!
        </div>

        <div v-if="type == 'ungraded' & submitted == true" class="alert alert-success" role="alert">
            You may proceed onto the next class!
        </div>
        
    </div>
</template>

<script>
export default {

    data() {
        return{
            questions: [],
            timerCount: 120,
            type: null,
            QAMarks: [],
            correct_answers: [],
            passed: null,
            submitted : null
        }
    },

    watch: {
        timerCount: {
            handler(value) {
                if (value > 0) {
                    setTimeout(()=>{
                        this.timerCount--;
                    },1000)
                }
            },
            immediate: true
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
        readQuiz() {
			fetch('http://localhost:5001/read_quiz', {
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
                this.type = data.data[0].type
                for (let i = 0; i < data.data.length; i++){
                    this.QAMarks.push(
                        {
                            question: data.data[i].question,
                            answer: null,
                            marks: 0
                        }
                    );
                    this.correct_answers.push(data.data[i].answer)
                }
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},

        checkAnswers(){
            for (let i =0; i<this.QAMarks.length; i++){
                if (this.QAMarks[i].answer == this.correct_answers[i]){
                    this.QAMarks[i].marks = 1
                }
            }
        },

        submitQuiz() {
			fetch('http://localhost:5001/submit_quiz', {
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
                        EID: this.EID,
                        QAMarks: this.QAMarks,
                        type: this.type
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				console.log(data)
                this.submitted = true
                if (data.message.includes("passed")){
                    this.passed = true
                }
                else if (data.message.includes("failed")){
                    this.passed = false
                }
                else if (data.message.includes("successfully")){
                    this.passed = true
                }
                else {
                    this.passed = "error"
                }
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},

        unlockNextLesson() {
			fetch('http://localhost:5001/unlock_next_lesson', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start,
                        EID: this.EID,
                        
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				console.log(data)
                // this.questions = data.data
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		},

    },

    created(){
        this.readQuiz()
        
    }
}
</script>

<style>

</style>