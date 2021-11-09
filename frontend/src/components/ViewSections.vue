<template>
	<div class="container mt-3">
		<h1>{{CID}}</h1>
		<table class="table table-hover">
			<thead>
				<tr>
					<th scope="col">Section</th>
					<th scope="col">Vacancy</th>
					<th scope="col"></th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="section in sections" :key="[section.CID, section.start, section.SID]">
					<td>{{section.SID}}</td>
					<td>{{section.vacancy}}</td>
					<td>
						<router-link type="button" class="btn btn-outline-primary" :to="{name: 'engineer_sign_up_action', params: {EID: this.EID, CID: this.CID, SID: section.SID, start: section.start}}">Sign Up</router-link>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script>
export default {
	data() {
		return {
			sections: []
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
        }
	},

	methods: {
		getSections() {
			fetch('http://18.118.224.235:5001/query_section', {
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
                this.sections = data.data
            })
            .catch(error => {
                console.log(error)
            })
		}
	},

	created() {
		this.getSections()
	}
}
</script>

<style>

</style>