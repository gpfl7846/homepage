$(document).ready(function(){
	$("input.pull-right.team_name.form-control").change(function () {
		if($(this).val()==""){
			$(this).css("border", "1px solid red");
		}
		else {
			$(this).css("border", "1px solid black");
		}
	}).trigger("change");



});