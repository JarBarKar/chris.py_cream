<template>
    <div>
        <div class="container my-3">
        <h1>Results</h1>
        <div class="container my-3">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly h4">
                <div class="container">Question</div>
                <div class="container">Answer Given</div>
                <div class="container">Correct Answer</div>
                <div class="container">Marks</div>
            </div>
        </div>

        <div class="container">
            <div class="d-flex flex-row bd-highlight mb-3 justify-content-evenly" v-for="result in results" :key="[result.SID, result.CID, result.LID, result.start, result.EID, result.question]">
                <div class="container">{{result.question}}</div>
                <div class="container">{{result.answer_given}}</div>
                <div class="container">{{result.correct_answer}}</div>
                <div class="container">{{result.marks}}</div>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            results: []
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
        ViewLessons() {
			fetch('http://localhost:5001/check_quiz_result', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        EID: this.EID,
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start,
                        LID: this.LID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				console.log(data.data)
                this.results = data.data
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