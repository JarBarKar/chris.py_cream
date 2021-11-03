<template>
    <div>
        {{message}}
    </div>
</template>

<script>
export default {
    data(){
        return{
            message: ""
        }
    },

    props: {
        EID: {
            type: [Number,String],
            required: true
        },

        SID: {
			type: [Number, String],
			required: true
		},
		
		CID: {
			type: [Number, String],
			required: true
		},

		start: {
			type: [Number, String],
			required: true
		}
    },

    methods: {
		approveSignUp() {
			fetch('http://localhost:5001/hr_approve_signup', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        EID : this.EID,
                        SID : this.SID,
                        CID : this.CID,
                        start: this.start
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                this.message = data.message
				console.log(data)
            })
            .catch(error => {
                console.log(error)
            })
		}
	},

    created(){
        this.approveSignUp()
    }
}
</script>

<style>

</style>