<template>
    <div class="container mt-3">
        <h1>Create a Question</h1>
        <form>
            <div class="form-group container mt-5">
                Question
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Yes" v-model="question">
            </div>
            
            <div class="form-group container mt-5">
                Answer
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Yes" v-model="answer">
            </div>

            <div class="form-group container mt-5">
                Option
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Yes|No" v-model="options">
            </div>
            {{options}}
                
            <div class="form-group container mt-5">
                Duration
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="0" v-model="duration">
            </div>
                
            <div class="container mt-5">
                Type
                <br>
                <input type="radio" id="one" value="ungraded" v-model="type">
                <label for="one">Ungraded</label>
                <br>
                <input type="radio" id="two" value="graded" v-model="type">
                <label for="two">Graded</label>
                
            </div>

            <div class="container mt-5">
                <button type="button" class="btn btn-primary" v-on:click="submitQuestion()">Submit</button>
            </div>
        </form>

        <div v-if="created" class="alert alert-success mt-3" role="alert">
            Question has been added
        </div>

        <div v-else-if="created == false" class="alert alert-danger mt-3" role="alert">
            An error occurred
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            question: null,
            answer: null,
            options: null,
            duration: null,
            type: null,
            error_message: null,
            created: null
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
        },
        // question: {
        //     type: [Number, String],
		// 	required: true
        // }
    },

    methods: {
        submitQuestion() {
			fetch('http://18.118.224.235:5001/create_quiz_question', {
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
                        question: this.question,
                        answer: this.answer,
                        options: this.options,
                        duration: this.duration,
                        type: this.type
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data)
				if (data.data) {
                    this.created = true
                }
                else{
                    this.created = false
                }
                
            })
            .catch(error => {
                this.error_message = error
                console.error("There was an error!", error)
            })
		}
    }
}
</script>

<style>

</style>