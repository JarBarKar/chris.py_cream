<template>
    <div class="container">
        <h1>{{CID}} Section {{SID}}</h1>
        <div>
            <table class="table">
                <thead>
                    <tr>
                        <th scope="col">TID</th>
                        <th scope="col">Name</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="trainer in trainers" :key="[trainer.TID]">
                        <td>{{trainer.TID}}</td>
                        <td>{{trainer.name}}</td>
                        <td>
                            <button type="button" class="btn btn-outline-primary" v-on:click="assignTrainer(trainer.TID)">Assign</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="assigned" class="alert alert-success" role="alert">
            Trainer has been assigned
        </div>

    </div>
</template>

<script>
export default {

    data() {
        return{
            trainers: [],
            assigned: null
        }
    },

    props: {
        CID: {
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
		getTrainers() {
			fetch('http://18.118.224.235:5001/view_trainers', {
                method: "GET",
                headers: {
                    "Content-Type" : "application/json"
                },
                
            })
            .then(resp => resp.json())
            .then(data => {
                this.trainers = data.data
            })
            .catch(error => {
                console.log(error)
            })
		},

        assignTrainer(TID) {
			fetch('http://18.118.224.235:5001/hr_assign_trainer', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        CID : this.CID,
                        SID : this.SID,
                        start: this.start,
                        TID: TID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data.data)
                this.assigned = data.data
            })
            .catch(error => {
                console.log(error)
            })
		}
	},

	created() {
		this.getTrainers()
	}
}
</script>

<style>

</style>