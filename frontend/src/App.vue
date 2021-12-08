<template>
	<div>
		<Navbar/>
		<router-view/>
	</div>
</template>

<script>
import Navbar from './components/Navbar.vue'

export default {
	name: 'App',
	components: {
		Navbar
	},
	
	
}
</script>

<style>
*{
	text-align: center;
	
};

.bg {
        background-image: url('./assets/photo_2021-11-06_15-38-19.jpg');
    }



</style>
