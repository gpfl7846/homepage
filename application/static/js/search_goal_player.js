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
				url: '/search_goaler',
				type: 'POST',
				data: {'result': result},

				success:function(response){
					console.log(response);
					$('#'+id).empty();
					
					
					var json = $.parseJSON(response);
					for (var i=0; i<json.length; i++) {
						var html = '<tr>'+'<td class="td_color">'+json[i].name+'</td>'+'<td class="td_color">'+json[i].major+'</td>'+'<td class="td_color">'+json[i].student_id+'</td>'+'<td class="td_color">'+'<button class="add_referee" value ="'+json[i].name+'"'+'type="button">'+'+'+'</button>'+'</td>'+'</tr>';
						var pk = '<input type="hidden" value="'+ json[i].pk+'">'
						$('#'+id).append(html);
						$('#'+id).append(pk);
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
	$('table').on('click', 'button', function(event){
		var name = event.target.value;
		var pk = $(this).parents('tbody').siblings('input').val();
		console.log(pk);
		$(this).parents('table').siblings('input').val(name);
		var id = $(this).parents('table').attr('id');
		$('#'+id).empty();
		var html = '<input type="hidden" name="'+name+'" value="'+pk+'">';
		$('#forhidden').append(html);
	});
});