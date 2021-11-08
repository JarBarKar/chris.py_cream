<template>
    <div class="container mt-3">
        <h1>Questions</h1>
        <div>{{timerCount}}</div>
        <div class="mb-3 row justify-content-center" >
            <form v-for="question in questions" :key="[question.LID, question.CID, question.SID, question.start, question.question]">
                <label for="staticEmail" class="col-sm-2 col-form-label">
                    {{question.question}}
                </label>
                <br>
                <div class="form-check form-check-inline" v-for="option in (question.options.split('|'))" :key="option">
                    <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1">
                    <label class="form-check-label" for="inlineCheckbox1">{{option}}</label>
                </div>
            </form>
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
        
    </div>
</template>

<script>
export default {

    data() {
        return{
            questions: [],
            timerCount: 120
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