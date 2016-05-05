	var direction=1;

	function sortName(clicked_id,team_id){
	// console.log(clicked_id);
	// console.log(team_id);
	// console.log(direction);

		$.ajax({

				url: '/sort_players',
				type: 'POST',
				data: {'data':clicked_id,
						'team_pk':team_id,
						'direction':direction
				},
				success:function(response){
				direction=direction*(-1);
				// console.log('success');
				var json=$.parseJSON(response);
				var myTable=document.getElementById('myTable');

					for(var i=0; i<json.length; i++){
						myTable.rows[i+1].cells[0].innerHTML=json[i].player_name;
						myTable.rows[i+1].cells[1].innerHTML=json[i].college;
						myTable.rows[i+1].cells[2].innerHTML=json[i].major;
						myTable.rows[i+1].cells[3].innerHTML=json[i].position;
						myTable.rows[i+1].cells[4].innerHTML=json[i].student_id;
						myTable.rows[i+1].cells[5].innerHTML=json[i].goal;
						myTable.rows[i+1].cells[6].innerHTML=json[i].assist;
						myTable.rows[i+1].cells[7].innerHTML=json[i].match_count;
						myTable.rows[i+1].cells[8].innerHTML=json[i].yellow_card_count;
						myTable.rows[i+1].cells[9].innerHTML=json[i].red_card_count;
						myTable.rows[i+1].cells[10].innerHTML=json[i].limit_of_participation;
						myTable.rows[i+1].cells[11].innerHTML=json[i].accumulate_limit_of_participation;
						//console.log(json[i].player_name);
					}
				},
				error:function(){
					//console.log('error');
				},
				complete:function(){
					//console.log('complete!');
				}
			});
		
	}
