var radarChartData = {
	labels: ["슈팅","패스", "드리블", "크로스", "볼 컨트롤", "체력", "주력", "해딩"],
	datasets: [
	
	{	
		label: "My Second dataset",
		fillColor: "rgba(151,187,205,0.2)",
		strokeColor: "rgba(151,187,205,1)",
		pointColor: "rgba(151,187,205,1)",
		pointStrokeColor: "#fff",
		pointHighlightFill: "#fff",
		pointHighlightStroke: "rgba(151,187,205,1)",
		data: [20,40,30,10,20,15,20,23]
	}
	]
};


window.onload = function(){
	$(document).on('slid.bs.carousel', function(e){
		if (typeof window.myRadar !== 'undefined') $(document).unbind('slid.bs.carousel'); 
		else if ($(e.relatedTarget).hasClass('chart-area')) {
			window.myRadar = new Chart(document.getElementById("canvas").getContext("2d")).Radar(radarChartData, {
				responsive: true
			});


			var ctx = document.getElementById("chart-area").getContext("2d");
			window.myDoughnut = new Chart(ctx).Doughnut(doughnutData, {responsive : true});
		}

	});
};