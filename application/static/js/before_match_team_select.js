$(document).ready(function(){
	$('.pickteam').click(function(){
		var team_pk = event.target.value;
		$.ajax({
			url: '/show_lineup',
			type: 'POST',
			data: {'team_pk': team_pk},

			success: function(response){
				console.log(team_pk);
				var json = $.parseJSON(response);
				$('#'+team_pk+'player_list').empty();
				for (var i=0; i<json.length; i++) {
					var html = '<tr>'+'<td>'+json[i].name+'</td>'+'<td>'+json[i].major+'</td>'+'<td>'+json[i].position+'</td>'+'<td>'+json[i].student_id+'</td>'+'<td>'+'<button class="addplayer blue-button" value="'+json[i].pk+'">'+'+'+'</button>'+'</tr>';
					$('#'+team_pk+'player_list').append(html);
				}
			},
			error: function(){
				console.log('error');
			},
			complete: function(){
				console.log('complete');
			}
		});
	});
});