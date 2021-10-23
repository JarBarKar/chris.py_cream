<template>
	<div>
		<h1>{{CID}}</h1>
		<table class="table">
			<thead>
				<tr>
					<th scope="col">Section</th>
					<th scope="col">Vacancy</th>
					<th scope="col"></th>
				</tr>
			</thead>
			<tbody>
				<tr v-for="section in sections" :key="[section.CID, section.start]">
					<td>{{section.SID}}</td>
					<td>{{section.vacancy}}</td>
					<td>
						<button type="button" class="btn btn-outline-primary">Sign Up</button>
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
		}
	},

	methods: {
		getSections() {
			fetch('http://localhost:5001/query_section', {
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