<template>
    <div class="container mt-3">
        <h1>Sections</h1>
        <table class="table">
            <thead>
                <tr>
                    <th scope="col">CID</th>
                    <th scope="col">SID</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="section in trainer_sections" :key="[section.CID, section.start, section.SID]">
                    <td>{{section.CID}}</td>
                    <td>{{section.SID}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {

    data() {
        return {
            TID : 1,
            trainer_sections: []
        }
    },

    methods: {
        getTrainerSections() {
            fetch('http://localhost:5001/view_sections', {
                method: "POST",
                headers: {
                    "Content-Type" : "application/json"
                },
                body: JSON.stringify(
                    {
                        TID : this.TID
                    }
                )
            })
            .then(resp => resp.json())
            .then(data => {
                this.trainer_sections = data.data
            })
            .catch(error => {
                console.log(error)
            })
        }
    },

    created() {
        this.getTrainerSections()
    }
}
</script>

<style>

</style>