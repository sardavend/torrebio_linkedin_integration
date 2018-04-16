var app = new Vue({
	el: '#app',
	data: {
		isActive:false,
	},
	methods: {
		showSidebar: () => this.isActive = true,
		getProfile: () => {
			window.location = '/integration'; 
		}
	}
})