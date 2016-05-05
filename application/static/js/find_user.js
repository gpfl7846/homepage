$(document).ready(function(){
	var xhr;
	
	$("input").keyup(function(){
		if ($("input").val()!=""){
			if (xhr && xhr.readyState != 4){
				xhr.abort();

			}
			xhr=$.ajax({

				url: '/find',
				type: 'POST',
				data: {'text':$('input').val()},
				success:function(response){
					$('#users').empty()
					$('#users').append(response)
				},
				complete:function(){
					console.log('complete!');
				}
			});
		} else {
			$('#users').empty()
		}
	});

});
