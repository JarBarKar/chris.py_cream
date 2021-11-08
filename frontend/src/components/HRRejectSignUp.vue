<template>
    <div class="alert alert-success d-flex align-items-center" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
        <div>
            {{message}}
        </div>
    </div>
    <!-- <div v-else class="alert alert-danger d-flex align-items-center" role="alert">
        <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
        <div>
            An error occurred! ):
        </div>
    </div> -->
</template>

<script>
export default {
    data(){
        return{
            data : [],
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
		rejectSignUp() {
			fetch('http://18.118.224.235:5001/hr_reject_signup', {
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
                this.data = data.data
                this.message = data.message
				console.log(data)
            })
            .catch(error => {
                console.log(error)
            })
		}
	},

    created(){
        this.rejectSignUp()
    }
}
</script>

<style>

</style>