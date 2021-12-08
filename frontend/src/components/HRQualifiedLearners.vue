<template>
    <div class="container">
        
        <div v-if="learners">
            <h1>Qualified</h1>
            <table class="container table " >
                <thead>
                    <tr>
                        <th scope="col">EID</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr  v-for="learner in learners" :key="learner">
                        <th scope="row">{{learner}}</th>
                        <th scope="row">
                            <button type="button" class="btn btn-outline-primary" v-on:click="assignEngineer(learner)">Assign</button>
                        </th>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="ongoing">
            <h1>Ongoing</h1>
            <table class="table container ">
                <thead>
                    <tr>
                        <th scope="col">EID</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="learner in ongoing" :key="learner">
                        <th scope="row container" >{{learner}}</th>
                        <th scope="row container">
                            <button type="button" class="btn btn-outline-primary" v-on:click="withdrawEngineer(learner)">Withdraw</button>
                        </th>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="completed">
            <h1>Completed</h1>
            <table class="table container">
                <thead>
                    <tr>
                        <th scope="col">EID</th>
                        
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="learner in completed" :key="learner">
                        <th scope="row container" >{{learner}}</th>
                        
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="assigned" class="alert alert-success" role="alert">
            Engineer was assigned
        </div>
        <div v-if="withdrawn" class="alert alert-success" role="alert">
            Engineer was withdrawn
        </div>
    </div>
</template>

<script>
export default {

    data() {
        return{
            learners: null,
            ongoing: null,
            completed: null,
            assigned: null,
            withdrawn: null
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
		getQualifiedLearners() {
			fetch('http://18.118.224.235:5001/view_qualified_learner', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        CID : this.CID
                        
                    }
                )
                
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data.data)
                if (data.data.eligible.length != 0) {
                this.learners = data.data.eligible
                }
                if (data.data.ongoing.length != 0) {
                this.ongoing = data.data.ongoing
                }
                if (data.data.completed.length != 0){
                this.completed = data.data.completed
                }
            })
            .catch(error => {
                console.log(error)
            })
		},

        assignEngineer(EID) {
			fetch('http://18.118.224.235:5001/hr_assign_engineer', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        CID : this.CID,
                        SID : this.SID,
                        start: this.start,
                        EID: EID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data)
                this.assigned = data.data
            })
            .catch(error => {
                console.log(error)
            })
		},

        withdrawEngineer(EID) {
			fetch('http://18.118.224.235:5001/hr_withdraw_engineer', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        CID : this.CID,
                        SID : this.SID,
                        start: this.start,
                        EID: EID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                console.log(data)
                this.withdrawn = data
            })
            .catch(error => {
                console.log(error)
            })
		}
	},

	created() {
		this.getQualifiedLearners()
	}

}
</script>

<style>

</style>