	var doughnutData = [
				{
					value: 800,
					color:"#F7464A",
					highlight: "#FF5A5E",
					label: "패"
				},
			
				{
					value: 200,
					color: "#4D5360",
					highlight: "#616774",
					label: "승"
				}

			];

			window.onload = function(){
				var ctx = document.getElementById("chart-area").getContext("2d");
				window.myDoughnut = new Chart(ctx).Doughnut(doughnutData, {responsive : true});
			};
 	
