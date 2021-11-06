<template>
  <div>
        <div class="container my-5">
            <h1>Trainer</h1>
        </div>

        <div class="container">
            <router-link type="button" class="btn btn-outline-primary" :to="{name: 'trainer_view_sections', params:{TID: this.TID}}">View my courses and sections</router-link>
        </div>
  </div>
</template>

<script>
export default {
    props: {
		TID: {
			type: [Number,String],
            required: true
		}
	}
}
</script>

<style>

</style>