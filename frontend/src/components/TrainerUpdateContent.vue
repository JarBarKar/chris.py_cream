<template>
    <div>
        <h1>Update Content</h1>
        <form>
            <div class="form-group container mt-5">
                Content Name
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Lesson 1 slides" v-model="new_content_name">
            </div>

            <div class="form-group container mt-5">
                Content Type
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="pdf" v-model="new_content_type">
            </div>
                
            <div class="form-group container mt-5">
                Link
                <input type="text" class="form-control" id="formGroupExampleInput" placeholder="abc.com" v-model="new_link">
            </div>

            <div class="container mt-5">
                <button type="button" class="btn btn-primary" v-on:click="submitUpdate()">Submit</button>
            </div>
        </form>

        <div v-if="updated == true" class="alert alert-success mt-3" role="alert">
            Content has been updated
        </div>

        <div v-else-if="updated == false" class="alert alert-danger mt-3" role="alert">
            An error occurred
        </div>
    </div>
</template>

<script>
export default {

    data(){
        return{
            new_content_name: null,
            new_content_type: null,
            new_link: null,
            updated: null
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
        content_name: {
            type: [Number, String],
			required: true
        },
        content_type: {
            type: [Number, String],
			required: true
        },
        link: {
            type: [Number, String],
			required: true
        }
    },

    methods: {
        submitUpdate() {
			fetch('http://18.118.224.235:5001/update_content', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        old_LID: this.LID,
                        old_SID : this.SID,
                        old_CID : this.CID,
                        old_start: this.start,
                        old_content_name: this.content_name,
                        old_content_type: this.content_type,
                        old_link: this.link,
                        content_name: this.new_content_name,
                        content_type: this.new_content_type,
                        link: this.new_link
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
				console.log(data.message)
                if (data.message.includes('updated')){
                    this.updated = true
                }
                else{
                    this.updated = false
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