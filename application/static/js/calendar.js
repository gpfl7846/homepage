$(document).ready(function() {
		var date= new Date();//현재한국시간
		var d = date.getDate();
		var m = date.getMonth();
		var y = date.getFullYear();

		$.ajax({
			url: '/match_list',
			type: 'POST',
			data: {'today':y},
			success:function(response){	
				if (response!="not exist"){
					var json=$.parseJSON(response);
				$('#calendar').fullCalendar({

				dragOpacity:{
					// month: .2,
					agenda: .2,
					agendaDay: .2,
					agendaWeek: .2,
					'default':.5
				},
				header: {
					left: 'prev,next today',
					center: 'title',
					right: 'month,agendaWeek,agendaDay'
				},
				defaultDate: date,
				editable: true,
				eventLimit: true // allow "more" link when too many events
				});

			
					var events=[];
					for(var i=0; i<json.length; i++){
						if (json[i].win_team_pk===""){
							var go='http://ryu.k-champsleague.appspot.com/before_match/'}
						else{
							var go='http://ryu.k-champsleague.appspot.com/after_match/'}
						events.push({
							title: json[i].match_team1+json[i].match_team1_goal+' '+'vs'+' '+json[i].match_team2_goal+json[i].match_team2,
							url: go+json[i].match_pk,
							allDay: false,
							start: json[i].start_time,
							end: json[i].end_time
						});
						// console.log(json[i].end_time);
					}
					// callback(events);
				$('#calendar').fullCalendar('addEventSource', events);
				$('#calendar').fullCalendar('changeView', agendaWeek);		
				$('#calendar').fullCalendar('changeView', agendaDay);		





				}//if

				else{
					// console.log('not exist');
				}
			},//success
			error:function(){
				// console.log('error');
			},
			complete:function(){
				// console.log('complete!');
			}
		});

	});