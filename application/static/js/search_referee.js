var xhr;

$(document).ready(function(){
	$('.search_player').keyup(function(){
		var result = $(this).val();
		var id = $(this).siblings('table').attr('id');
		console.log(result);
		console.log(id);
		if (xhr) {
			xhr.abort();
		}

		if (result === '') {
			console.log('None');
			$('#'+id).empty();
		}

		else {
			xhr = $.ajax({
				url: '/search_player',
				type: 'POST',
				data: {'result': result},

				success:function(response){
					console.log(response);
					$('#'+id).empty();
					
					
					var json = $.parseJSON(response);
					for (var i=0; i<json.length; i++) {
						var html = '<tr>'+'<td>'+json[i].name+'</td>'+'<td>'+json[i].major+'</td>'+'<td>'+json[i].student_id+'</td>'+'<td>'+'<button class="add_referee" value ="'+json[i].pk+'"'+'type="button">'+'+'+'</button>'+'</td>'+'</tr>';
						console.log(html);
						$('#'+id).append(html);
						console.log('#'+id);
					}
					
				},
				Error:function(){
					console.log('error');
				},
				Complete:function(){
					console.log('complete');
				}
			});
		}
	});	
	// $('.add_referee').click(function(){
	// 	var referee_id = event.target.value;
	// 	var referee_kind = $(this).parents('table').attr('id');
	// 	console.log(referee_id);
	// 	console.log(referee_kind);
	// 	$.ajax({
	// 		url: '/add_referee',
	// 		type: 'POST',
	// 		data: {
	// 			'referee_id': referee_id,
	// 			'referee_kind': referee_kind
	// 		},

	// 		success:function(response) {
	// 			console.log('ok');
	// 		},
	// 		error:function(){
	// 			console.log('error');
	// 		},
	// 		complete:function(){
	// 			console.log('complete');
	// 		}
	// 	});
	// });
});