$(document).ready(function(){
	var lineup = [];
	var running = true;
	$('.player_list').on('click', 'button', function(event){
		if (lineup.length >= 11) {
			alert('11명이 모두 등록되었습니다.');
			running = false;
		}

		var player_id = event.target.value;
		var address = window.location.href.split('/');
		var match_pk = address[address.length-1];
		
		if (running === true) {
			$.ajax({
				url: '/register_lineup',
				type: 'POST',
				data: {'player_id': player_id,
						'match_pk': match_pk
				},

				success:function(response){
					if (response === 'None') {
						alert('11명이 모두 등록되었습니다.');
					}
					else if (response === 'Already') {
						alert('이미 등록된 선수입니다.');
					}
					else {
						var json = $.parseJSON(response);
						var html = '<tr>'+'<td>'+json[0].name+'</td>'+'<td>'+json[0].position+'</td>'+'</tr>';
						var pk = json[0].pk;
						var player_id = json[0].player_id;
						$('#'+pk+'lineup').append(html);
						lineup.push(player_id);
						console.log(lineup);
						console.log(pk);
					}
				},
				error:function(){
						console.log('error');
				},
				complete:function(){
						console.log('complete');
				}
			});
		}
	});
});