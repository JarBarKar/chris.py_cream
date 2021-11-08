<template>
    <div>
        {{QAMarks}}
    </div>
</template>

<script>
export default {
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
        },
        QAMarks: {
            type: [Array, Object],
            required: true,
            default() { 
                [
                    {
                        question: null,
                        answer: null,
                        marks: 0
                    }
                ]

            }
        },
        type: {
            type: [Number, String],
			required: true
        }
    },
}
</script>

<style>

</style>