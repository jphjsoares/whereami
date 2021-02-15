let mly = new Mapillary.Viewer({
	apiClient:"MGNWR1hFdWVhb3FQTTJxcDZPUExHZzo2NTE4YmM3NmY0YWYyNGYy",
	component: {
		cover: false,
	},
	container:'mly',
	imageKey: keys[0],
});

window.addEventListener("resize", function() { mly.resize(); });